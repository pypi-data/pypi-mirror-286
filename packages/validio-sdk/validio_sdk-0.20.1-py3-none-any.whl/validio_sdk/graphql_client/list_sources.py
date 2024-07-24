from datetime import datetime
from typing import Annotated, Any, List, Literal, Optional, Union

from pydantic import Field

from validio_sdk.scalars import (
    CredentialId,
    CronExpression,
    JsonTypeDefinition,
    SegmentationId,
    SourceId,
    WindowId,
)

from .base_model import BaseModel
from .enums import (
    CatalogAssetType,
    FileFormat,
    SourceState,
    StreamingSourceMessageFormat,
)


class ListSources(BaseModel):
    sources_list: List[
        Annotated[
            Union[
                "ListSourcesSourcesListSource",
                "ListSourcesSourcesListAwsAthenaSource",
                "ListSourcesSourcesListAwsKinesisSource",
                "ListSourcesSourcesListAwsRedshiftSource",
                "ListSourcesSourcesListAwsS3Source",
                "ListSourcesSourcesListAzureSynapseSource",
                "ListSourcesSourcesListClickHouseSource",
                "ListSourcesSourcesListDatabricksSource",
                "ListSourcesSourcesListDbtModelRunSource",
                "ListSourcesSourcesListDbtTestResultSource",
                "ListSourcesSourcesListGcpBigQuerySource",
                "ListSourcesSourcesListGcpPubSubLiteSource",
                "ListSourcesSourcesListGcpPubSubSource",
                "ListSourcesSourcesListGcpStorageSource",
                "ListSourcesSourcesListKafkaSource",
                "ListSourcesSourcesListPostgreSqlSource",
                "ListSourcesSourcesListSnowflakeSource",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourcesList")


class ListSourcesSourcesListSource(BaseModel):
    typename__: Literal["DemoSource", "Source"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "ListSourcesSourcesListSourceCredential"
    windows: List["ListSourcesSourcesListSourceWindows"]
    segmentations: List["ListSourcesSourcesListSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["ListSourcesSourcesListSourceTags"]


class ListSourcesSourcesListSourceCatalogAsset(BaseModel):
    typename__: Literal[
        "AwsAthenaCatalogAsset",
        "AwsKinesisCatalogAsset",
        "AwsRedshiftCatalogAsset",
        "AwsS3CatalogAsset",
        "AzureSynapseCatalogAsset",
        "CatalogAsset",
        "ClickHouseCatalogAsset",
        "DatabricksCatalogAsset",
        "DemoCatalogAsset",
        "GcpBigQueryCatalogAsset",
        "GcpPubSubCatalogAsset",
        "GcpPubSubLiteCatalogAsset",
        "GcpStorageCatalogAsset",
        "KafkaCatalogAsset",
        "LookerDashboardCatalogAsset",
        "LookerLookCatalogAsset",
        "PostgreSqlCatalogAsset",
        "SnowflakeCatalogAsset",
        "TableauCustomSQLTableCatalogAsset",
        "TableauDashboardCatalogAsset",
        "TableauDatasourceCatalogAsset",
        "TableauFlowCatalogAsset",
        "TableauWorkbookCatalogAsset",
        "TableauWorksheetCatalogAsset",
    ] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class ListSourcesSourcesListSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListSourceTags(BaseModel):
    key: str
    value: str


class ListSourcesSourcesListAwsAthenaSource(BaseModel):
    typename__: Literal["AwsAthenaSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListAwsAthenaSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "ListSourcesSourcesListAwsAthenaSourceCredential"
    windows: List["ListSourcesSourcesListAwsAthenaSourceWindows"]
    segmentations: List["ListSourcesSourcesListAwsAthenaSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["ListSourcesSourcesListAwsAthenaSourceTags"]
    config: "ListSourcesSourcesListAwsAthenaSourceConfig"


class ListSourcesSourcesListAwsAthenaSourceCatalogAsset(BaseModel):
    typename__: Literal["AwsAthenaCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class ListSourcesSourcesListAwsAthenaSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListAwsAthenaSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListAwsAthenaSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListAwsAthenaSourceTags(BaseModel):
    key: str
    value: str


class ListSourcesSourcesListAwsAthenaSourceConfig(BaseModel):
    catalog: str
    database: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class ListSourcesSourcesListAwsKinesisSource(BaseModel):
    typename__: Literal["AwsKinesisSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListAwsKinesisSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "ListSourcesSourcesListAwsKinesisSourceCredential"
    windows: List["ListSourcesSourcesListAwsKinesisSourceWindows"]
    segmentations: List["ListSourcesSourcesListAwsKinesisSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["ListSourcesSourcesListAwsKinesisSourceTags"]
    config: "ListSourcesSourcesListAwsKinesisSourceConfig"


class ListSourcesSourcesListAwsKinesisSourceCatalogAsset(BaseModel):
    typename__: Literal["AwsKinesisCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class ListSourcesSourcesListAwsKinesisSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListAwsKinesisSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListAwsKinesisSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListAwsKinesisSourceTags(BaseModel):
    key: str
    value: str


class ListSourcesSourcesListAwsKinesisSourceConfig(BaseModel):
    region: str
    stream_name: str = Field(alias="streamName")
    message_format: Optional[
        "ListSourcesSourcesListAwsKinesisSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class ListSourcesSourcesListAwsKinesisSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class ListSourcesSourcesListAwsRedshiftSource(BaseModel):
    typename__: Literal["AwsRedshiftSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListAwsRedshiftSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "ListSourcesSourcesListAwsRedshiftSourceCredential"
    windows: List["ListSourcesSourcesListAwsRedshiftSourceWindows"]
    segmentations: List["ListSourcesSourcesListAwsRedshiftSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["ListSourcesSourcesListAwsRedshiftSourceTags"]
    config: "ListSourcesSourcesListAwsRedshiftSourceConfig"


class ListSourcesSourcesListAwsRedshiftSourceCatalogAsset(BaseModel):
    typename__: Literal["AwsRedshiftCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class ListSourcesSourcesListAwsRedshiftSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListAwsRedshiftSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListAwsRedshiftSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListAwsRedshiftSourceTags(BaseModel):
    key: str
    value: str


class ListSourcesSourcesListAwsRedshiftSourceConfig(BaseModel):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class ListSourcesSourcesListAwsS3Source(BaseModel):
    typename__: Literal["AwsS3Source"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListAwsS3SourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "ListSourcesSourcesListAwsS3SourceCredential"
    windows: List["ListSourcesSourcesListAwsS3SourceWindows"]
    segmentations: List["ListSourcesSourcesListAwsS3SourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["ListSourcesSourcesListAwsS3SourceTags"]
    config: "ListSourcesSourcesListAwsS3SourceConfig"


class ListSourcesSourcesListAwsS3SourceCatalogAsset(BaseModel):
    typename__: Literal["AwsS3CatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class ListSourcesSourcesListAwsS3SourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListAwsS3SourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListAwsS3SourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListAwsS3SourceTags(BaseModel):
    key: str
    value: str


class ListSourcesSourcesListAwsS3SourceConfig(BaseModel):
    bucket: str
    prefix: str
    csv: Optional["ListSourcesSourcesListAwsS3SourceConfigCsv"]
    schedule: Optional[CronExpression]
    file_pattern: Optional[str] = Field(alias="filePattern")
    file_format: Optional[FileFormat] = Field(alias="fileFormat")


class ListSourcesSourcesListAwsS3SourceConfigCsv(BaseModel):
    null_marker: Optional[str] = Field(alias="nullMarker")
    delimiter: str


class ListSourcesSourcesListAzureSynapseSource(BaseModel):
    typename__: Literal["AzureSynapseSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListAzureSynapseSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "ListSourcesSourcesListAzureSynapseSourceCredential"
    windows: List["ListSourcesSourcesListAzureSynapseSourceWindows"]
    segmentations: List["ListSourcesSourcesListAzureSynapseSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["ListSourcesSourcesListAzureSynapseSourceTags"]
    config: "ListSourcesSourcesListAzureSynapseSourceConfig"


class ListSourcesSourcesListAzureSynapseSourceCatalogAsset(BaseModel):
    typename__: Literal["GcpBigQueryCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class ListSourcesSourcesListAzureSynapseSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListAzureSynapseSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListAzureSynapseSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListAzureSynapseSourceTags(BaseModel):
    key: str
    value: str


class ListSourcesSourcesListAzureSynapseSourceConfig(BaseModel):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class ListSourcesSourcesListClickHouseSource(BaseModel):
    typename__: Literal["ClickHouseSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListClickHouseSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "ListSourcesSourcesListClickHouseSourceCredential"
    windows: List["ListSourcesSourcesListClickHouseSourceWindows"]
    segmentations: List["ListSourcesSourcesListClickHouseSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["ListSourcesSourcesListClickHouseSourceTags"]
    config: "ListSourcesSourcesListClickHouseSourceConfig"


class ListSourcesSourcesListClickHouseSourceCatalogAsset(BaseModel):
    typename__: Literal["ClickHouseCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class ListSourcesSourcesListClickHouseSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListClickHouseSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListClickHouseSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListClickHouseSourceTags(BaseModel):
    key: str
    value: str


class ListSourcesSourcesListClickHouseSourceConfig(BaseModel):
    database: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class ListSourcesSourcesListDatabricksSource(BaseModel):
    typename__: Literal["DatabricksSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListDatabricksSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "ListSourcesSourcesListDatabricksSourceCredential"
    windows: List["ListSourcesSourcesListDatabricksSourceWindows"]
    segmentations: List["ListSourcesSourcesListDatabricksSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["ListSourcesSourcesListDatabricksSourceTags"]
    config: "ListSourcesSourcesListDatabricksSourceConfig"


class ListSourcesSourcesListDatabricksSourceCatalogAsset(BaseModel):
    typename__: Literal["DatabricksCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class ListSourcesSourcesListDatabricksSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListDatabricksSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListDatabricksSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListDatabricksSourceTags(BaseModel):
    key: str
    value: str


class ListSourcesSourcesListDatabricksSourceConfig(BaseModel):
    catalog: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]
    http_path: Optional[str] = Field(alias="httpPath")


class ListSourcesSourcesListDbtModelRunSource(BaseModel):
    typename__: Literal["DbtModelRunSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListDbtModelRunSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "ListSourcesSourcesListDbtModelRunSourceCredential"
    windows: List["ListSourcesSourcesListDbtModelRunSourceWindows"]
    segmentations: List["ListSourcesSourcesListDbtModelRunSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["ListSourcesSourcesListDbtModelRunSourceTags"]
    config: "ListSourcesSourcesListDbtModelRunSourceConfig"


class ListSourcesSourcesListDbtModelRunSourceCatalogAsset(BaseModel):
    typename__: Literal[
        "AwsAthenaCatalogAsset",
        "AwsKinesisCatalogAsset",
        "AwsRedshiftCatalogAsset",
        "AwsS3CatalogAsset",
        "AzureSynapseCatalogAsset",
        "CatalogAsset",
        "ClickHouseCatalogAsset",
        "DatabricksCatalogAsset",
        "DemoCatalogAsset",
        "GcpBigQueryCatalogAsset",
        "GcpPubSubCatalogAsset",
        "GcpPubSubLiteCatalogAsset",
        "GcpStorageCatalogAsset",
        "KafkaCatalogAsset",
        "LookerDashboardCatalogAsset",
        "LookerLookCatalogAsset",
        "PostgreSqlCatalogAsset",
        "SnowflakeCatalogAsset",
        "TableauCustomSQLTableCatalogAsset",
        "TableauDashboardCatalogAsset",
        "TableauDatasourceCatalogAsset",
        "TableauFlowCatalogAsset",
        "TableauWorkbookCatalogAsset",
        "TableauWorksheetCatalogAsset",
    ] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class ListSourcesSourcesListDbtModelRunSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListDbtModelRunSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListDbtModelRunSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListDbtModelRunSourceTags(BaseModel):
    key: str
    value: str


class ListSourcesSourcesListDbtModelRunSourceConfig(BaseModel):
    job_name: str = Field(alias="jobName")
    project_name: str = Field(alias="projectName")
    schedule: Optional[CronExpression]


class ListSourcesSourcesListDbtTestResultSource(BaseModel):
    typename__: Literal["DbtTestResultSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListDbtTestResultSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "ListSourcesSourcesListDbtTestResultSourceCredential"
    windows: List["ListSourcesSourcesListDbtTestResultSourceWindows"]
    segmentations: List["ListSourcesSourcesListDbtTestResultSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["ListSourcesSourcesListDbtTestResultSourceTags"]
    config: "ListSourcesSourcesListDbtTestResultSourceConfig"


class ListSourcesSourcesListDbtTestResultSourceCatalogAsset(BaseModel):
    typename__: Literal[
        "AwsAthenaCatalogAsset",
        "AwsKinesisCatalogAsset",
        "AwsRedshiftCatalogAsset",
        "AwsS3CatalogAsset",
        "AzureSynapseCatalogAsset",
        "CatalogAsset",
        "ClickHouseCatalogAsset",
        "DatabricksCatalogAsset",
        "DemoCatalogAsset",
        "GcpBigQueryCatalogAsset",
        "GcpPubSubCatalogAsset",
        "GcpPubSubLiteCatalogAsset",
        "GcpStorageCatalogAsset",
        "KafkaCatalogAsset",
        "LookerDashboardCatalogAsset",
        "LookerLookCatalogAsset",
        "PostgreSqlCatalogAsset",
        "SnowflakeCatalogAsset",
        "TableauCustomSQLTableCatalogAsset",
        "TableauDashboardCatalogAsset",
        "TableauDatasourceCatalogAsset",
        "TableauFlowCatalogAsset",
        "TableauWorkbookCatalogAsset",
        "TableauWorksheetCatalogAsset",
    ] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class ListSourcesSourcesListDbtTestResultSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListDbtTestResultSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListDbtTestResultSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListDbtTestResultSourceTags(BaseModel):
    key: str
    value: str


class ListSourcesSourcesListDbtTestResultSourceConfig(BaseModel):
    job_name: str = Field(alias="jobName")
    project_name: str = Field(alias="projectName")
    schedule: Optional[CronExpression]


class ListSourcesSourcesListGcpBigQuerySource(BaseModel):
    typename__: Literal["GcpBigQuerySource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListGcpBigQuerySourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "ListSourcesSourcesListGcpBigQuerySourceCredential"
    windows: List["ListSourcesSourcesListGcpBigQuerySourceWindows"]
    segmentations: List["ListSourcesSourcesListGcpBigQuerySourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["ListSourcesSourcesListGcpBigQuerySourceTags"]
    config: "ListSourcesSourcesListGcpBigQuerySourceConfig"


class ListSourcesSourcesListGcpBigQuerySourceCatalogAsset(BaseModel):
    typename__: Literal["GcpBigQueryCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class ListSourcesSourcesListGcpBigQuerySourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListGcpBigQuerySourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListGcpBigQuerySourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListGcpBigQuerySourceTags(BaseModel):
    key: str
    value: str


class ListSourcesSourcesListGcpBigQuerySourceConfig(BaseModel):
    project: str
    dataset: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class ListSourcesSourcesListGcpPubSubLiteSource(BaseModel):
    typename__: Literal["GcpPubSubLiteSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListGcpPubSubLiteSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "ListSourcesSourcesListGcpPubSubLiteSourceCredential"
    windows: List["ListSourcesSourcesListGcpPubSubLiteSourceWindows"]
    segmentations: List["ListSourcesSourcesListGcpPubSubLiteSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["ListSourcesSourcesListGcpPubSubLiteSourceTags"]
    config: "ListSourcesSourcesListGcpPubSubLiteSourceConfig"


class ListSourcesSourcesListGcpPubSubLiteSourceCatalogAsset(BaseModel):
    typename__: Literal["GcpPubSubLiteCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class ListSourcesSourcesListGcpPubSubLiteSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListGcpPubSubLiteSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListGcpPubSubLiteSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListGcpPubSubLiteSourceTags(BaseModel):
    key: str
    value: str


class ListSourcesSourcesListGcpPubSubLiteSourceConfig(BaseModel):
    location: str
    project: str
    subscription_id: str = Field(alias="subscriptionId")
    message_format: Optional[
        "ListSourcesSourcesListGcpPubSubLiteSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class ListSourcesSourcesListGcpPubSubLiteSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class ListSourcesSourcesListGcpPubSubSource(BaseModel):
    typename__: Literal["GcpPubSubSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListGcpPubSubSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "ListSourcesSourcesListGcpPubSubSourceCredential"
    windows: List["ListSourcesSourcesListGcpPubSubSourceWindows"]
    segmentations: List["ListSourcesSourcesListGcpPubSubSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["ListSourcesSourcesListGcpPubSubSourceTags"]
    config: "ListSourcesSourcesListGcpPubSubSourceConfig"


class ListSourcesSourcesListGcpPubSubSourceCatalogAsset(BaseModel):
    typename__: Literal["GcpPubSubCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class ListSourcesSourcesListGcpPubSubSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListGcpPubSubSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListGcpPubSubSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListGcpPubSubSourceTags(BaseModel):
    key: str
    value: str


class ListSourcesSourcesListGcpPubSubSourceConfig(BaseModel):
    project: str
    subscription_id: str = Field(alias="subscriptionId")
    message_format: Optional[
        "ListSourcesSourcesListGcpPubSubSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class ListSourcesSourcesListGcpPubSubSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class ListSourcesSourcesListGcpStorageSource(BaseModel):
    typename__: Literal["GcpStorageSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListGcpStorageSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "ListSourcesSourcesListGcpStorageSourceCredential"
    windows: List["ListSourcesSourcesListGcpStorageSourceWindows"]
    segmentations: List["ListSourcesSourcesListGcpStorageSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["ListSourcesSourcesListGcpStorageSourceTags"]
    config: "ListSourcesSourcesListGcpStorageSourceConfig"


class ListSourcesSourcesListGcpStorageSourceCatalogAsset(BaseModel):
    typename__: Literal["GcpStorageCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class ListSourcesSourcesListGcpStorageSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListGcpStorageSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListGcpStorageSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListGcpStorageSourceTags(BaseModel):
    key: str
    value: str


class ListSourcesSourcesListGcpStorageSourceConfig(BaseModel):
    project: str
    bucket: str
    folder: str
    csv: Optional["ListSourcesSourcesListGcpStorageSourceConfigCsv"]
    schedule: Optional[CronExpression]
    file_pattern: Optional[str] = Field(alias="filePattern")
    file_format: Optional[FileFormat] = Field(alias="fileFormat")


class ListSourcesSourcesListGcpStorageSourceConfigCsv(BaseModel):
    null_marker: Optional[str] = Field(alias="nullMarker")
    delimiter: str


class ListSourcesSourcesListKafkaSource(BaseModel):
    typename__: Literal["KafkaSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListKafkaSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "ListSourcesSourcesListKafkaSourceCredential"
    windows: List["ListSourcesSourcesListKafkaSourceWindows"]
    segmentations: List["ListSourcesSourcesListKafkaSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["ListSourcesSourcesListKafkaSourceTags"]
    config: "ListSourcesSourcesListKafkaSourceConfig"


class ListSourcesSourcesListKafkaSourceCatalogAsset(BaseModel):
    typename__: Literal["KafkaCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class ListSourcesSourcesListKafkaSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListKafkaSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListKafkaSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListKafkaSourceTags(BaseModel):
    key: str
    value: str


class ListSourcesSourcesListKafkaSourceConfig(BaseModel):
    topic: str
    message_format: Optional["ListSourcesSourcesListKafkaSourceConfigMessageFormat"] = (
        Field(alias="messageFormat")
    )


class ListSourcesSourcesListKafkaSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class ListSourcesSourcesListPostgreSqlSource(BaseModel):
    typename__: Literal["PostgreSqlSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListPostgreSqlSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "ListSourcesSourcesListPostgreSqlSourceCredential"
    windows: List["ListSourcesSourcesListPostgreSqlSourceWindows"]
    segmentations: List["ListSourcesSourcesListPostgreSqlSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["ListSourcesSourcesListPostgreSqlSourceTags"]
    config: "ListSourcesSourcesListPostgreSqlSourceConfig"


class ListSourcesSourcesListPostgreSqlSourceCatalogAsset(BaseModel):
    typename__: Literal["PostgreSqlCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class ListSourcesSourcesListPostgreSqlSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListPostgreSqlSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListPostgreSqlSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListPostgreSqlSourceTags(BaseModel):
    key: str
    value: str


class ListSourcesSourcesListPostgreSqlSourceConfig(BaseModel):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class ListSourcesSourcesListSnowflakeSource(BaseModel):
    typename__: Literal["SnowflakeSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["ListSourcesSourcesListSnowflakeSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "ListSourcesSourcesListSnowflakeSourceCredential"
    windows: List["ListSourcesSourcesListSnowflakeSourceWindows"]
    segmentations: List["ListSourcesSourcesListSnowflakeSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["ListSourcesSourcesListSnowflakeSourceTags"]
    config: "ListSourcesSourcesListSnowflakeSourceConfig"


class ListSourcesSourcesListSnowflakeSourceCatalogAsset(BaseModel):
    typename__: Literal["SnowflakeCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class ListSourcesSourcesListSnowflakeSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListSnowflakeSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListSnowflakeSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class ListSourcesSourcesListSnowflakeSourceTags(BaseModel):
    key: str
    value: str


class ListSourcesSourcesListSnowflakeSourceConfig(BaseModel):
    role: Optional[str]
    warehouse: Optional[str]
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


ListSources.model_rebuild()
ListSourcesSourcesListSource.model_rebuild()
ListSourcesSourcesListAwsAthenaSource.model_rebuild()
ListSourcesSourcesListAwsKinesisSource.model_rebuild()
ListSourcesSourcesListAwsKinesisSourceConfig.model_rebuild()
ListSourcesSourcesListAwsRedshiftSource.model_rebuild()
ListSourcesSourcesListAwsS3Source.model_rebuild()
ListSourcesSourcesListAwsS3SourceConfig.model_rebuild()
ListSourcesSourcesListAzureSynapseSource.model_rebuild()
ListSourcesSourcesListClickHouseSource.model_rebuild()
ListSourcesSourcesListDatabricksSource.model_rebuild()
ListSourcesSourcesListDbtModelRunSource.model_rebuild()
ListSourcesSourcesListDbtTestResultSource.model_rebuild()
ListSourcesSourcesListGcpBigQuerySource.model_rebuild()
ListSourcesSourcesListGcpPubSubLiteSource.model_rebuild()
ListSourcesSourcesListGcpPubSubLiteSourceConfig.model_rebuild()
ListSourcesSourcesListGcpPubSubSource.model_rebuild()
ListSourcesSourcesListGcpPubSubSourceConfig.model_rebuild()
ListSourcesSourcesListGcpStorageSource.model_rebuild()
ListSourcesSourcesListGcpStorageSourceConfig.model_rebuild()
ListSourcesSourcesListKafkaSource.model_rebuild()
ListSourcesSourcesListKafkaSourceConfig.model_rebuild()
ListSourcesSourcesListPostgreSqlSource.model_rebuild()
ListSourcesSourcesListSnowflakeSource.model_rebuild()
