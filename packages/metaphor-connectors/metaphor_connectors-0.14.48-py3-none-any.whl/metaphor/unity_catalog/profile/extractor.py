import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Collection, List, Optional, Tuple

from metaphor.unity_catalog.config import UnityCatalogRunConfig
from metaphor.unity_catalog.extractor import DEFAULT_FILTER
from metaphor.unity_catalog.utils import (
    create_api,
    create_connection_pool,
    escape_special_characters,
)

try:
    from databricks.sdk.service.catalog import ColumnTypeName, TableInfo, TableType
except ImportError:
    print("Please install metaphor[unity_catalog] extra\n")
    raise


from metaphor.common.base_extractor import BaseExtractor
from metaphor.common.entity_id import normalize_full_dataset_name
from metaphor.common.event_util import ENTITY_TYPES
from metaphor.common.logger import get_logger
from metaphor.models.crawler_run_metadata import Platform
from metaphor.models.metadata_change_event import (
    DataPlatform,
    Dataset,
    DatasetFieldStatistics,
    DatasetLogicalID,
    DatasetStatistics,
    FieldStatistics,
)

logger = get_logger()

NON_MODIFICATION_OPERATIONS = {
    "SET TBLPROPERTIES",
    "ADD CONSTRAINT",
}
"""These are the operations that do not count as modifications."""

NUMERIC_TYPES = {
    ColumnTypeName.DECIMAL,
    ColumnTypeName.DOUBLE,
    ColumnTypeName.FLOAT,
    ColumnTypeName.INT,
    ColumnTypeName.LONG,
    ColumnTypeName.SHORT,
}


class UnityCatalogProfileExtractor(BaseExtractor):
    """Unity Catalog data profile extractor"""

    _description = "Unity Catalog data profile crawler"
    _platform = Platform.UNITY_CATALOG

    @staticmethod
    def from_config_file(config_file: str) -> "UnityCatalogProfileExtractor":
        return UnityCatalogProfileExtractor(
            UnityCatalogRunConfig.from_yaml_file(config_file)
        )

    def __init__(self, config: UnityCatalogRunConfig):
        super().__init__(config)
        self._api = create_api(f"https://{config.hostname}", config.token)

        self._connection_pool = create_connection_pool(
            config.token, config.hostname, config.http_path, config.max_concurrency
        )

        self._filter = config.filter.normalize().merge(DEFAULT_FILTER)

    async def extract(self) -> Collection[ENTITY_TYPES]:
        logger.info("Fetching data profile from Unity Catalog")

        tables = self._get_tables()
        return self._profile(tables)

    def _profile(self, tables: List[TableInfo]) -> List[Dataset]:
        def profile(table_info: TableInfo):
            dataset = self._init_dataset(table_info)

            connection = self._connection_pool.get()

            dataset_statistics, field_statistics = self._get_statistics(
                connection, table_info
            )

            self._connection_pool.put(connection)

            dataset.statistics = dataset_statistics
            dataset.field_statistics = field_statistics

            logger.info(f"Fetched {table_info.table_type}: {table_info.full_name}")
            return dataset

        logger.info(f"Profiling {len(tables)} tables")

        entities = []
        with ThreadPoolExecutor(max_workers=self._connection_pool.maxsize) as executor:
            futures = [executor.submit(profile, table) for table in tables]

            for future in as_completed(futures):
                entities.append(future.result())

        return entities

    def _get_tables(self) -> List[TableInfo]:
        catalogs = [
            catalog_info.name
            for catalog_info in self._api.catalogs.list()
            if catalog_info.name and self._filter.include_database(catalog_info.name)
        ]

        tables: List[TableInfo] = []
        for catalog in catalogs:
            schemas = [
                schema_info.name
                for schema_info in self._api.schemas.list(catalog)
                if schema_info.name
                and self._filter.include_schema(catalog, schema_info.name)
            ]
            for schema in schemas:
                table_infos = [
                    table_info
                    for table_info in self._api.tables.list(catalog, schema)
                    if table_info.name
                    and self._filter.include_table(catalog, schema, table_info.name)
                ]
                for table_info in table_infos:
                    table_type = table_info.table_type
                    if table_type is None or table_type in (
                        TableType.VIEW,
                        TableType.MATERIALIZED_VIEW,
                    ):
                        continue
                    tables.append(table_info)
        return tables

    def _init_dataset(self, table_info: TableInfo) -> Dataset:
        assert table_info.full_name
        return Dataset(
            logical_id=DatasetLogicalID(
                name=normalize_full_dataset_name(table_info.full_name),
                platform=DataPlatform.UNITY_CATALOG,
            ),
        )

    def _get_statistics(
        self, connection, table_info: TableInfo
    ) -> Tuple[Optional[DatasetStatistics], Optional[DatasetFieldStatistics]]:
        assert table_info.full_name
        dataset_statistics = DatasetStatistics()

        # Gather this first, if this is nonempty in the end then we actually save
        # this to `Dataset`.
        field_statistics = DatasetFieldStatistics(field_statistics=[])
        assert field_statistics.field_statistics is not None

        with connection.cursor() as cursor:
            escaped_name = escape_special_characters(table_info.full_name)
            # Gather numeric columns
            numeric_columns = [
                column.name
                for column in (table_info.columns or [])
                if column.type_name in NUMERIC_TYPES and column.name
            ]

            analyze_query = f"ANALYZE TABLE {escaped_name} COMPUTE STATISTICS"
            if numeric_columns:
                analyze_query += f" FOR COLUMNS {', '.join(numeric_columns)}"

            try:
                # This can take a while
                cursor.execute(analyze_query)
                cursor.execute(f"DESCRIBE TABLE EXTENDED {escaped_name}")
                rows = cursor.fetchall()
            except Exception:
                logger.exception(f"not able to get statistics for {escaped_name}")
                return None, None

            statistics = next(
                (row for row in rows if row.col_name == "Statistics"), None
            )
            if statistics:
                # `statistics.data_type` looks like "X bytes, Y rows"
                bytes_count, row_count = [
                    float(x) for x in re.findall(r"(\d+)", statistics.data_type)
                ]
                dataset_statistics.data_size_bytes = bytes_count
                dataset_statistics.record_count = row_count

            for numeric_column in numeric_columns:
                # Parse numeric column stats
                try:
                    cursor.execute(f"DESCRIBE EXTENDED {escaped_name} {numeric_column}")
                    column_details = cursor.fetchall()
                except Exception:
                    logger.exception(
                        f"not able to get column stat for {escaped_name}.{numeric_column}"
                    )
                    continue

                def get_value_from_row(key: str) -> Optional[float]:
                    value = next(
                        (
                            row.info_value
                            for row in column_details
                            if row.info_name == key
                        ),
                        None,
                    )
                    if value:
                        if value == "NULL":
                            return None
                        return float(value)
                    return value

                stats = FieldStatistics(
                    distinct_value_count=get_value_from_row("distinct_count"),
                    field_path=numeric_column,
                    max_value=get_value_from_row("max"),
                    min_value=get_value_from_row("min"),
                    null_value_count=get_value_from_row("num_nulls"),
                )
                field_statistics.field_statistics.append(stats)

        return (
            dataset_statistics,
            None if not field_statistics.field_statistics else field_statistics,
        )
