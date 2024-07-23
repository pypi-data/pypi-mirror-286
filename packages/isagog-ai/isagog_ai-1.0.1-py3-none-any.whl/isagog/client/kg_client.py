"""
Interface to the Isagog Knoledge Graph service
(c) Isagog S.r.l. 2024, MIT License
"""
import logging
import os
import time
from typing import Type, TypeVar

# import requests
import httpx
from dotenv import load_dotenv

from isagog.model.kg_model import Individual, Entity, Assertion, Attribute, Concept, Relation, Reference
from isagog.model.kg_query import UnarySelectQuery, DisjunctiveClause, AtomicClause, Comparison, Value
from isagog.model.ontology import Ontology

load_dotenv()

KG_DEFAULT_TIMEOUT = int(os.getenv('KG_DEFAULT_TIMEOUT', 120))

# Type variable for the Entity hierarchy
E = TypeVar('E', bound='Entity')

AUTH_TOKEN_KEY = os.getenv('ISAGOG_AUTH_TOKEN_KEY', 'X-Isagog-API-Token')
AUTH_TOKEN_VALUE = os.getenv('ISAGOG_AUTH_TOKEN_VALUE')


class KnowledgeBase(object):
    """
    Interface to knowledge base service
    """

    def __init__(self,
                 route: str,
                 ontology: Ontology = None,
                 dataset: str = None,
                 version: str = None,
                 logger=None):
        """

        :param route: the service's endpoint route
        :param ontology: the kb ontology
        :param dataset: the dataset name; if None, uses the service's default
        :param version: the service's version identifier
        """
        assert route
        self.route = route
        self.dataset = dataset
        self.ontology = ontology
        self.version = version if version else "latest"
        self.logger = logger if logger else logging.getLogger()
        self.logger.info("Isagog KG client (%s) initialized on route %s", hex(id(self)), route)

    def get_entity(self,
                   _id: Reference,
                   expand: bool = True,
                   entity_type: Type[E] = Entity,
                   **kwargs
                   ) -> E | None:
        """
        Gets the entity by its identifier
        :param _id: the entity identifier
        :param expand: whether to return entity attributes
        :param entity_type: the entity type (default: Entity)
        """

        assert _id

        self.logger.debug("Fetching %s", _id)

        if not issubclass(entity_type, Entity):
            raise ValueError(f"{entity_type} not an Entity")

        expand = "true" if expand else "false"

        params = f"id={_id}&expand={expand}"

        headers = {"Accept": "application/json"}

        if AUTH_TOKEN_VALUE:
            headers[AUTH_TOKEN_KEY] = AUTH_TOKEN_VALUE

        if self.dataset:
            params += f"&dataset={self.dataset}"
        try:
            res = httpx.get(
                url=self.route,
                params=params,
                headers=headers,
            )
            res.raise_for_status()
            self.logger.debug("Fetched %s", _id)
            return entity_type(id=_id, **res.json())
        except httpx.ConnectError:
            self.logger.error("Failed to connect to the host %s.", self.route)
            return None
        except httpx.RequestError as exc:
            self.logger.error(f"An error occurred while requesting {exc.request.url!r}.")
            return None
        except httpx.TimeoutException:
            self.logger.error("The request timed out from %s.", self.route)
            return None
        except httpx.HTTPStatusError as exc:
            self.logger.error(
                f"HTTP error from occurred from {self.route}: {exc.response.status_code} - {exc.response.text}")
            return None
        except Exception as exc:
            self.logger.error(f"An unexpected error occurred on {self.route}: {exc}")
            return None

    def query_assertions(self,
                         subject: Individual,
                         properties: list[Attribute | Relation],
                         **kwargs
                         ) -> list[Assertion]:
        """
        Returns specific entity properties

        :param timeout:
        :param subject:
        :param properties: the queried properties
        :return: a list of dictionaries { property: values }
        """
        assert (subject and properties)

        if not isinstance(subject, Individual):
            raise ValueError(f"{subject} not an Individual")

        if not all(isinstance(prop, (Attribute, Relation)) for prop in properties):
            raise ValueError(f"{properties} not all Attributes or Relations")

        self.logger.debug("Querying assertions for %s", subject)

        query = UnarySelectQuery(subject=subject.id)

        for prop in properties:
            query.add_fetch_clause(predicate=str(prop.id))

        headers = {"Accept": "application/json"}

        if AUTH_TOKEN_VALUE:
            headers[AUTH_TOKEN_KEY] = AUTH_TOKEN_VALUE

        query_dict = query.to_dict(version=self.version)

        timeout = kwargs.get('timeout', KG_DEFAULT_TIMEOUT)

        try:
            res = httpx.post(
                url=self.route,
                json=query_dict,
                headers=headers,
                timeout=timeout
            )
            res.raise_for_status()

            res_list = res.json()
            if len(res_list) == 0:
                self.logger.warning("Void attribute query")
                return []
            else:
                res_attrib_list = res_list[0].get('attributes', OSError("malformed response"))

                def __get_values(_prop: str) -> str:
                    try:
                        record = next(item for item in res_attrib_list if item['id'] == _prop)
                        return record.get('values', OSError("malformed response"))
                    except StopIteration:
                        # raise OSError("incomplete response: %s not found", _prop)
                        return None

                return [Assertion(predicate=prop, values=__get_values(prop)) for prop in properties]

        except httpx.ConnectError:
            self.logger.error("Failed to connect to the host %s.", self.route)
            return []
        except httpx.RequestError as exc:
            self.logger.error(f"An error occurred while requesting {exc.request.url!r}.")
            return []
        except httpx.TimeoutException:
            self.logger.error("The request timed out from %s.", self.route)
            return []
        except httpx.HTTPStatusError as exc:
            self.logger.error(
                f"HTTP error from occurred from {self.route}: {exc.response.status_code} - {exc.response.text}")
            return []
        except Exception as exc:
            self.logger.error(f"An unexpected error occurred on {self.route}: {exc}")
            return []

    def search_individuals(self,
                           kinds: list[Concept] = None,
                           constraints: dict[Attribute, Value] = None,
                           **kwargs
                           ) -> list[Individual]:
        """
        Retrieves individuals by string search
        :param kinds: the kinds to search for
        :param constraints: the search constraints
        :return: a list of matching individuals
        """
        assert (kinds or (constraints and len(constraints) > 0))
        self.logger.debug("Searching individuals")
        entities = []
        query = UnarySelectQuery()
        if kinds:
            query.add_kinds(kinds)
        if len(constraints) == 1:
            attribute, value = next(iter(constraints.items()))
            search_clause = AtomicClause(property=attribute, argument=value, method=Comparison.REGEX)
        else:
            search_clause = DisjunctiveClause()
            for attribute, value in constraints.items():
                search_clause.add_atom(property=attribute, argument=value, method=Comparison.REGEX)

        query.add(search_clause)

        headers = {"Accept": "application/json"}
        if 'auth_token' in kwargs:
            headers[AUTH_TOKEN_KEY] = kwargs.get('auth_token')

        timeout = kwargs.get('timeout', KG_DEFAULT_TIMEOUT)

        try:
            res = httpx.post(
                url=self.route,
                json=query.to_dict(version=self.version),
                headers=headers,
                timeout=timeout
            )
            res.raise_for_status()
            if res.status_code == 200:
                entities.extend([Individual(id=r.get('id'), **r) for r in res.json()])
            else:
                self.logger.error("Search individuals failed: code %d, reason %s", res.status_code, res.text)
            return entities
        except httpx.ConnectError:
            self.logger.error("Failed to connect to the host %s.", self.route)
            return []
        except httpx.RequestError as exc:
            self.logger.error(f"An error occurred while requesting {exc.request.url!r}.")
            return []
        except httpx.TimeoutException:
            self.logger.error("The request timed out from %s.", self.route)
            return []
        except httpx.HTTPStatusError as exc:
            self.logger.error(
                f"HTTP error from occurred from {self.route}: {exc.response.status_code} - {exc.response.text}")
            return []
        except Exception as exc:
            self.logger.error(f"An unexpected error occurred on {self.route}: {exc}")
            return []

    def query_individuals(self,
                          query: UnarySelectQuery,
                          kind: Type[E] = Individual,
                          **kwargs
                          ) -> list[E]:
        """


        :param query: the query
        :param kind: the kind of individuals to return
        :return: a list of individuals of the specified kind
        """
        start_time = time.time()

        req = query.to_dict(version=self.version)

        if self.dataset and (self.version == "latest" or self.version > "v1.0.0"):
            req['dataset'] = self.dataset

        headers = {"Accept": "application/json"}

        if AUTH_TOKEN_VALUE:
            headers[AUTH_TOKEN_KEY] = AUTH_TOKEN_VALUE

        timeout = kwargs.get('timeout', KG_DEFAULT_TIMEOUT)

        try:
            res = httpx.post(
                url=self.route,
                json=req,
                headers=headers,
                timeout=timeout
            )
            res.raise_for_status()
            self.logger.debug("Query individuals done in %d seconds", time.time() - start_time)
            return [kind(r.get('id'), **r) for r in res.json()]

        except httpx.ConnectError:
            self.logger.error("Failed to connect to the host %s.", self.route)
            return []
        except httpx.RequestError as exc:
            self.logger.error(f"An error occurred while requesting {exc.request.url!r}.")
            return []
        except httpx.TimeoutException:
            self.logger.error("The request timed out from %s.", self.route)
            return []
        except httpx.HTTPStatusError as exc:
            self.logger.error(
                f"HTTP error from occurred from {self.route}: {exc.response.status_code} - {exc.response.text}")
            return []
        except Exception as exc:
            self.logger.error(f"An unexpected error occurred on {self.route}: {exc}")
            return []

    def upsert_individual(self, individual: Individual, **kwargs) -> bool:
        """
        Updates an individual or insert it if not present; existing properties are preserved

        :param individual: the individual

        :return:
        """
        if individual.need_update():

            self.logger.debug("Updating individual %s", individual.id)

            params = {'id': individual.id}
            if self.dataset:
                params['dataset'] = self.dataset

            req = [ass.to_dict() for ass in individual.get_assertions()]

            headers = {"Accept": "application/json"}

            if AUTH_TOKEN_VALUE:
                headers[AUTH_TOKEN_KEY] = AUTH_TOKEN_VALUE

            try:
                res = httpx.patch(
                    url=self.route,
                    params=params,
                    json=req,
                    headers=headers
                )
                res.raise_for_status()
                individual.updated()
                return True
            except httpx.ConnectError:
                self.logger.error("Failed to connect to the host %s.", self.route)
                return False
            except httpx.RequestError as exc:
                self.logger.error(f"An error occurred while requesting {exc.request.url!r}.")
                return False
            except httpx.TimeoutException:
                self.logger.error("The request timed out from %s.", self.route)
                return False
            except httpx.HTTPStatusError as exc:
                self.logger.error(
                    f"HTTP error from occurred from {self.route}: {exc.response.status_code} - {exc.response.text}")
                return False
            except Exception as exc:
                self.logger.error(f"An unexpected error occurred on {self.route}: {exc}")
                return False

        else:
            self.logger.warning("Individual %s doesn't need update", individual.id)

    def delete_individual(self, _id: Reference, **kwargs):
        pass
