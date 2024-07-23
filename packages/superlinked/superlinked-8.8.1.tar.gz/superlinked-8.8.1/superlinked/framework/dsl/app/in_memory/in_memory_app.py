# Copyright 2024 Superlinked, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from beartype.typing import Any, Sequence

from superlinked.framework.common.dag.context import ExecutionContext
from superlinked.framework.common.exception import QueryException
from superlinked.framework.common.storage_manager.storage_manager import StorageManager
from superlinked.framework.common.util.type_validator import TypeValidator
from superlinked.framework.dsl.app.app import App
from superlinked.framework.dsl.executor.query.query_executor import QueryExecutor
from superlinked.framework.dsl.index.index import Index
from superlinked.framework.dsl.query.query import QueryObj
from superlinked.framework.dsl.query.query_vector_factory import QueryVectorFactory
from superlinked.framework.dsl.query.result import Result
from superlinked.framework.dsl.source.in_memory_source import InMemorySource
from superlinked.framework.dsl.storage.vector_database import VectorDatabase
from superlinked.framework.evaluator.online_dag_evaluator import OnlineDagEvaluator
from superlinked.framework.online.source.in_memory_data_processor import (
    InMemoryDataProcessor,
)
from superlinked.framework.online.source.in_memory_object_writer import (
    InMemoryObjectWriter,
)
from superlinked.framework.storage.in_memory.object_serializer import ObjectSerializer


@TypeValidator.wrap
class InMemoryApp(App[InMemorySource]):
    """
    In-memory implementation of the App class.
    """

    def __init__(
        self,
        sources: Sequence[InMemorySource],
        indices: Sequence[Index],
        vector_database: VectorDatabase,
        context: ExecutionContext,
    ) -> None:
        """
        Initialize the InMemoryApp from an InMemoryExecutor.
        Args:
            sources (list[InMemorySource]): List of in-memory sources.
            indices (list[Index]): List of indices.
            vector_database (VectorDatabase | None): Vector database instance. Defaults to InMemory.
            context (Mapping[str, Mapping[str, Any]]): Context mapping.
        """
        super().__init__(sources, indices, vector_database, context)
        self._init_search_indices()
        self._object_writer = InMemoryObjectWriter(self._storage_manager)
        self._index_online_dag_evaluator_map = {
            index: OnlineDagEvaluator(
                index._dag,
                set(index._space_schemas).union(index._effect_schemas),
                self.storage_manager,
            )
            for index in self._indices
        }
        self._index_query_vector_factory_map = {
            index: QueryVectorFactory(
                index._dag, set(index._space_schemas), self._storage_manager
            )
            for index in self._indices
        }
        self._data_processors = [
            InMemoryDataProcessor(
                self._index_online_dag_evaluator_map[index],
                self._storage_manager,
                context,
                index,
            )
            for index in self._indices
        ]
        for data_processor, index in zip(self._data_processors, self._indices):
            for source in self.__filter_index_sources(index, self._sources):
                source._source.register(data_processor)
        for source in self._sources:
            source._source.register(self._object_writer)

    def restore(self, serializer: ObjectSerializer) -> None:
        node_ids = [index._node_id for index in self._indices]
        app_identifier = "_".join(node_ids)
        self._vector_database._vdb_connector.restore(serializer, app_identifier)

    def persist(self, serializer: ObjectSerializer) -> None:
        node_ids = [index._node_id for index in self._indices]
        app_identifier = "_".join(node_ids)
        self._vector_database._vdb_connector.persist(serializer, app_identifier)

    def query(self, query_obj: QueryObj, **params: Any) -> Result:
        """
        Execute a query. Example:
        ```
        query = (
            Query(relevance_index, weights=[{"relevance_space": Param("relevance_weight")}])
            .find(paragraph)
            .with_vector(user, Param("user_id"))
            .similar(relevance_space.text, Param("query_text"), weight=Param("query_weight"))
        )
        result = app.query(
            query, query_text="Pear", user_id="some_user", relevance_weight=1, query_weight=2
        )
        ```
        Args:
            query_obj (QueryObj): The query object.
            **params: Additional parameters.
        Returns:
            Result:  The result of the query.
        Raises:
            QueryException: If the query index is not amongst the executor's indices.
        """
        if query_vector_factory := self._index_query_vector_factory_map.get(
            query_obj.index
        ):
            return QueryExecutor(self, query_obj, query_vector_factory).query(**params)

        raise QueryException(
            (
                f"Query index {query_obj.index} is not amongst the executor's indices: ",
                f" {list(self._index_query_vector_factory_map.keys())}",
            )
        )

    def _init_storage_manager(self) -> StorageManager:
        return StorageManager(self._vector_database._vdb_connector)

    @staticmethod
    def __filter_index_sources(
        index: Index, sources: Sequence[InMemorySource]
    ) -> list[InMemorySource]:
        return [source for source in sources if index.has_schema(source._schema)]
