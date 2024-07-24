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


class GetSource(BaseModel):
    source: Optional[
        Annotated[
            Union[
                "GetSourceSourceSource",
                "GetSourceSourceAwsAthenaSource",
                "GetSourceSourceAwsKinesisSource",
                "GetSourceSourceAwsRedshiftSource",
                "GetSourceSourceAwsS3Source",
                "GetSourceSourceAzureSynapseSource",
                "GetSourceSourceClickHouseSource",
                "GetSourceSourceDatabricksSource",
                "GetSourceSourceDbtModelRunSource",
                "GetSourceSourceDbtTestResultSource",
                "GetSourceSourceGcpBigQuerySource",
                "GetSourceSourceGcpPubSubLiteSource",
                "GetSourceSourceGcpPubSubSource",
                "GetSourceSourceGcpStorageSource",
                "GetSourceSourceKafkaSource",
                "GetSourceSourcePostgreSqlSource",
                "GetSourceSourceSnowflakeSource",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class GetSourceSourceSource(BaseModel):
    typename__: Literal["DemoSource", "Source"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourceSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourceSourceCredential"
    windows: List["GetSourceSourceSourceWindows"]
    segmentations: List["GetSourceSourceSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["GetSourceSourceSourceTags"]


class GetSourceSourceSourceCatalogAsset(BaseModel):
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


class GetSourceSourceSourceCredential(BaseModel):
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


class GetSourceSourceSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourceSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourceSourceTags(BaseModel):
    key: str
    value: str


class GetSourceSourceAwsAthenaSource(BaseModel):
    typename__: Literal["AwsAthenaSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourceAwsAthenaSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourceAwsAthenaSourceCredential"
    windows: List["GetSourceSourceAwsAthenaSourceWindows"]
    segmentations: List["GetSourceSourceAwsAthenaSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["GetSourceSourceAwsAthenaSourceTags"]
    config: "GetSourceSourceAwsAthenaSourceConfig"


class GetSourceSourceAwsAthenaSourceCatalogAsset(BaseModel):
    typename__: Literal["AwsAthenaCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceSourceAwsAthenaSourceCredential(BaseModel):
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


class GetSourceSourceAwsAthenaSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourceAwsAthenaSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourceAwsAthenaSourceTags(BaseModel):
    key: str
    value: str


class GetSourceSourceAwsAthenaSourceConfig(BaseModel):
    catalog: str
    database: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceSourceAwsKinesisSource(BaseModel):
    typename__: Literal["AwsKinesisSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourceAwsKinesisSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourceAwsKinesisSourceCredential"
    windows: List["GetSourceSourceAwsKinesisSourceWindows"]
    segmentations: List["GetSourceSourceAwsKinesisSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["GetSourceSourceAwsKinesisSourceTags"]
    config: "GetSourceSourceAwsKinesisSourceConfig"


class GetSourceSourceAwsKinesisSourceCatalogAsset(BaseModel):
    typename__: Literal["AwsKinesisCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceSourceAwsKinesisSourceCredential(BaseModel):
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


class GetSourceSourceAwsKinesisSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourceAwsKinesisSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourceAwsKinesisSourceTags(BaseModel):
    key: str
    value: str


class GetSourceSourceAwsKinesisSourceConfig(BaseModel):
    region: str
    stream_name: str = Field(alias="streamName")
    message_format: Optional["GetSourceSourceAwsKinesisSourceConfigMessageFormat"] = (
        Field(alias="messageFormat")
    )


class GetSourceSourceAwsKinesisSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class GetSourceSourceAwsRedshiftSource(BaseModel):
    typename__: Literal["AwsRedshiftSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourceAwsRedshiftSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourceAwsRedshiftSourceCredential"
    windows: List["GetSourceSourceAwsRedshiftSourceWindows"]
    segmentations: List["GetSourceSourceAwsRedshiftSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["GetSourceSourceAwsRedshiftSourceTags"]
    config: "GetSourceSourceAwsRedshiftSourceConfig"


class GetSourceSourceAwsRedshiftSourceCatalogAsset(BaseModel):
    typename__: Literal["AwsRedshiftCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceSourceAwsRedshiftSourceCredential(BaseModel):
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


class GetSourceSourceAwsRedshiftSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourceAwsRedshiftSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourceAwsRedshiftSourceTags(BaseModel):
    key: str
    value: str


class GetSourceSourceAwsRedshiftSourceConfig(BaseModel):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceSourceAwsS3Source(BaseModel):
    typename__: Literal["AwsS3Source"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourceAwsS3SourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourceAwsS3SourceCredential"
    windows: List["GetSourceSourceAwsS3SourceWindows"]
    segmentations: List["GetSourceSourceAwsS3SourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["GetSourceSourceAwsS3SourceTags"]
    config: "GetSourceSourceAwsS3SourceConfig"


class GetSourceSourceAwsS3SourceCatalogAsset(BaseModel):
    typename__: Literal["AwsS3CatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceSourceAwsS3SourceCredential(BaseModel):
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


class GetSourceSourceAwsS3SourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourceAwsS3SourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourceAwsS3SourceTags(BaseModel):
    key: str
    value: str


class GetSourceSourceAwsS3SourceConfig(BaseModel):
    bucket: str
    prefix: str
    csv: Optional["GetSourceSourceAwsS3SourceConfigCsv"]
    schedule: Optional[CronExpression]
    file_pattern: Optional[str] = Field(alias="filePattern")
    file_format: Optional[FileFormat] = Field(alias="fileFormat")


class GetSourceSourceAwsS3SourceConfigCsv(BaseModel):
    null_marker: Optional[str] = Field(alias="nullMarker")
    delimiter: str


class GetSourceSourceAzureSynapseSource(BaseModel):
    typename__: Literal["AzureSynapseSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourceAzureSynapseSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourceAzureSynapseSourceCredential"
    windows: List["GetSourceSourceAzureSynapseSourceWindows"]
    segmentations: List["GetSourceSourceAzureSynapseSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["GetSourceSourceAzureSynapseSourceTags"]
    config: "GetSourceSourceAzureSynapseSourceConfig"


class GetSourceSourceAzureSynapseSourceCatalogAsset(BaseModel):
    typename__: Literal["GcpBigQueryCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceSourceAzureSynapseSourceCredential(BaseModel):
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


class GetSourceSourceAzureSynapseSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourceAzureSynapseSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourceAzureSynapseSourceTags(BaseModel):
    key: str
    value: str


class GetSourceSourceAzureSynapseSourceConfig(BaseModel):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceSourceClickHouseSource(BaseModel):
    typename__: Literal["ClickHouseSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourceClickHouseSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourceClickHouseSourceCredential"
    windows: List["GetSourceSourceClickHouseSourceWindows"]
    segmentations: List["GetSourceSourceClickHouseSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["GetSourceSourceClickHouseSourceTags"]
    config: "GetSourceSourceClickHouseSourceConfig"


class GetSourceSourceClickHouseSourceCatalogAsset(BaseModel):
    typename__: Literal["ClickHouseCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceSourceClickHouseSourceCredential(BaseModel):
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


class GetSourceSourceClickHouseSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourceClickHouseSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourceClickHouseSourceTags(BaseModel):
    key: str
    value: str


class GetSourceSourceClickHouseSourceConfig(BaseModel):
    database: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceSourceDatabricksSource(BaseModel):
    typename__: Literal["DatabricksSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourceDatabricksSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourceDatabricksSourceCredential"
    windows: List["GetSourceSourceDatabricksSourceWindows"]
    segmentations: List["GetSourceSourceDatabricksSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["GetSourceSourceDatabricksSourceTags"]
    config: "GetSourceSourceDatabricksSourceConfig"


class GetSourceSourceDatabricksSourceCatalogAsset(BaseModel):
    typename__: Literal["DatabricksCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceSourceDatabricksSourceCredential(BaseModel):
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


class GetSourceSourceDatabricksSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourceDatabricksSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourceDatabricksSourceTags(BaseModel):
    key: str
    value: str


class GetSourceSourceDatabricksSourceConfig(BaseModel):
    catalog: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]
    http_path: Optional[str] = Field(alias="httpPath")


class GetSourceSourceDbtModelRunSource(BaseModel):
    typename__: Literal["DbtModelRunSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourceDbtModelRunSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourceDbtModelRunSourceCredential"
    windows: List["GetSourceSourceDbtModelRunSourceWindows"]
    segmentations: List["GetSourceSourceDbtModelRunSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["GetSourceSourceDbtModelRunSourceTags"]
    config: "GetSourceSourceDbtModelRunSourceConfig"


class GetSourceSourceDbtModelRunSourceCatalogAsset(BaseModel):
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


class GetSourceSourceDbtModelRunSourceCredential(BaseModel):
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


class GetSourceSourceDbtModelRunSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourceDbtModelRunSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourceDbtModelRunSourceTags(BaseModel):
    key: str
    value: str


class GetSourceSourceDbtModelRunSourceConfig(BaseModel):
    job_name: str = Field(alias="jobName")
    project_name: str = Field(alias="projectName")
    schedule: Optional[CronExpression]


class GetSourceSourceDbtTestResultSource(BaseModel):
    typename__: Literal["DbtTestResultSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourceDbtTestResultSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourceDbtTestResultSourceCredential"
    windows: List["GetSourceSourceDbtTestResultSourceWindows"]
    segmentations: List["GetSourceSourceDbtTestResultSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["GetSourceSourceDbtTestResultSourceTags"]
    config: "GetSourceSourceDbtTestResultSourceConfig"


class GetSourceSourceDbtTestResultSourceCatalogAsset(BaseModel):
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


class GetSourceSourceDbtTestResultSourceCredential(BaseModel):
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


class GetSourceSourceDbtTestResultSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourceDbtTestResultSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourceDbtTestResultSourceTags(BaseModel):
    key: str
    value: str


class GetSourceSourceDbtTestResultSourceConfig(BaseModel):
    job_name: str = Field(alias="jobName")
    project_name: str = Field(alias="projectName")
    schedule: Optional[CronExpression]


class GetSourceSourceGcpBigQuerySource(BaseModel):
    typename__: Literal["GcpBigQuerySource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourceGcpBigQuerySourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourceGcpBigQuerySourceCredential"
    windows: List["GetSourceSourceGcpBigQuerySourceWindows"]
    segmentations: List["GetSourceSourceGcpBigQuerySourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["GetSourceSourceGcpBigQuerySourceTags"]
    config: "GetSourceSourceGcpBigQuerySourceConfig"


class GetSourceSourceGcpBigQuerySourceCatalogAsset(BaseModel):
    typename__: Literal["GcpBigQueryCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceSourceGcpBigQuerySourceCredential(BaseModel):
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


class GetSourceSourceGcpBigQuerySourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourceGcpBigQuerySourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourceGcpBigQuerySourceTags(BaseModel):
    key: str
    value: str


class GetSourceSourceGcpBigQuerySourceConfig(BaseModel):
    project: str
    dataset: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceSourceGcpPubSubLiteSource(BaseModel):
    typename__: Literal["GcpPubSubLiteSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourceGcpPubSubLiteSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourceGcpPubSubLiteSourceCredential"
    windows: List["GetSourceSourceGcpPubSubLiteSourceWindows"]
    segmentations: List["GetSourceSourceGcpPubSubLiteSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["GetSourceSourceGcpPubSubLiteSourceTags"]
    config: "GetSourceSourceGcpPubSubLiteSourceConfig"


class GetSourceSourceGcpPubSubLiteSourceCatalogAsset(BaseModel):
    typename__: Literal["GcpPubSubLiteCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceSourceGcpPubSubLiteSourceCredential(BaseModel):
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


class GetSourceSourceGcpPubSubLiteSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourceGcpPubSubLiteSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourceGcpPubSubLiteSourceTags(BaseModel):
    key: str
    value: str


class GetSourceSourceGcpPubSubLiteSourceConfig(BaseModel):
    location: str
    project: str
    subscription_id: str = Field(alias="subscriptionId")
    message_format: Optional[
        "GetSourceSourceGcpPubSubLiteSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class GetSourceSourceGcpPubSubLiteSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class GetSourceSourceGcpPubSubSource(BaseModel):
    typename__: Literal["GcpPubSubSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourceGcpPubSubSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourceGcpPubSubSourceCredential"
    windows: List["GetSourceSourceGcpPubSubSourceWindows"]
    segmentations: List["GetSourceSourceGcpPubSubSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["GetSourceSourceGcpPubSubSourceTags"]
    config: "GetSourceSourceGcpPubSubSourceConfig"


class GetSourceSourceGcpPubSubSourceCatalogAsset(BaseModel):
    typename__: Literal["GcpPubSubCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceSourceGcpPubSubSourceCredential(BaseModel):
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


class GetSourceSourceGcpPubSubSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourceGcpPubSubSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourceGcpPubSubSourceTags(BaseModel):
    key: str
    value: str


class GetSourceSourceGcpPubSubSourceConfig(BaseModel):
    project: str
    subscription_id: str = Field(alias="subscriptionId")
    message_format: Optional["GetSourceSourceGcpPubSubSourceConfigMessageFormat"] = (
        Field(alias="messageFormat")
    )


class GetSourceSourceGcpPubSubSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class GetSourceSourceGcpStorageSource(BaseModel):
    typename__: Literal["GcpStorageSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourceGcpStorageSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourceGcpStorageSourceCredential"
    windows: List["GetSourceSourceGcpStorageSourceWindows"]
    segmentations: List["GetSourceSourceGcpStorageSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["GetSourceSourceGcpStorageSourceTags"]
    config: "GetSourceSourceGcpStorageSourceConfig"


class GetSourceSourceGcpStorageSourceCatalogAsset(BaseModel):
    typename__: Literal["GcpStorageCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceSourceGcpStorageSourceCredential(BaseModel):
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


class GetSourceSourceGcpStorageSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourceGcpStorageSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourceGcpStorageSourceTags(BaseModel):
    key: str
    value: str


class GetSourceSourceGcpStorageSourceConfig(BaseModel):
    project: str
    bucket: str
    folder: str
    csv: Optional["GetSourceSourceGcpStorageSourceConfigCsv"]
    schedule: Optional[CronExpression]
    file_pattern: Optional[str] = Field(alias="filePattern")
    file_format: Optional[FileFormat] = Field(alias="fileFormat")


class GetSourceSourceGcpStorageSourceConfigCsv(BaseModel):
    null_marker: Optional[str] = Field(alias="nullMarker")
    delimiter: str


class GetSourceSourceKafkaSource(BaseModel):
    typename__: Literal["KafkaSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourceKafkaSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourceKafkaSourceCredential"
    windows: List["GetSourceSourceKafkaSourceWindows"]
    segmentations: List["GetSourceSourceKafkaSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["GetSourceSourceKafkaSourceTags"]
    config: "GetSourceSourceKafkaSourceConfig"


class GetSourceSourceKafkaSourceCatalogAsset(BaseModel):
    typename__: Literal["KafkaCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceSourceKafkaSourceCredential(BaseModel):
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


class GetSourceSourceKafkaSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourceKafkaSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourceKafkaSourceTags(BaseModel):
    key: str
    value: str


class GetSourceSourceKafkaSourceConfig(BaseModel):
    topic: str
    message_format: Optional["GetSourceSourceKafkaSourceConfigMessageFormat"] = Field(
        alias="messageFormat"
    )


class GetSourceSourceKafkaSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class GetSourceSourcePostgreSqlSource(BaseModel):
    typename__: Literal["PostgreSqlSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourcePostgreSqlSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourcePostgreSqlSourceCredential"
    windows: List["GetSourceSourcePostgreSqlSourceWindows"]
    segmentations: List["GetSourceSourcePostgreSqlSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["GetSourceSourcePostgreSqlSourceTags"]
    config: "GetSourceSourcePostgreSqlSourceConfig"


class GetSourceSourcePostgreSqlSourceCatalogAsset(BaseModel):
    typename__: Literal["PostgreSqlCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceSourcePostgreSqlSourceCredential(BaseModel):
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


class GetSourceSourcePostgreSqlSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourcePostgreSqlSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourcePostgreSqlSourceTags(BaseModel):
    key: str
    value: str


class GetSourceSourcePostgreSqlSourceConfig(BaseModel):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceSourceSnowflakeSource(BaseModel):
    typename__: Literal["SnowflakeSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["GetSourceSourceSnowflakeSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "GetSourceSourceSnowflakeSourceCredential"
    windows: List["GetSourceSourceSnowflakeSourceWindows"]
    segmentations: List["GetSourceSourceSnowflakeSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    tags: List["GetSourceSourceSnowflakeSourceTags"]
    config: "GetSourceSourceSnowflakeSourceConfig"


class GetSourceSourceSnowflakeSourceCatalogAsset(BaseModel):
    typename__: Literal["SnowflakeCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceSourceSnowflakeSourceCredential(BaseModel):
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


class GetSourceSourceSnowflakeSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourceSnowflakeSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")


class GetSourceSourceSnowflakeSourceTags(BaseModel):
    key: str
    value: str


class GetSourceSourceSnowflakeSourceConfig(BaseModel):
    role: Optional[str]
    warehouse: Optional[str]
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


GetSource.model_rebuild()
GetSourceSourceSource.model_rebuild()
GetSourceSourceAwsAthenaSource.model_rebuild()
GetSourceSourceAwsKinesisSource.model_rebuild()
GetSourceSourceAwsKinesisSourceConfig.model_rebuild()
GetSourceSourceAwsRedshiftSource.model_rebuild()
GetSourceSourceAwsS3Source.model_rebuild()
GetSourceSourceAwsS3SourceConfig.model_rebuild()
GetSourceSourceAzureSynapseSource.model_rebuild()
GetSourceSourceClickHouseSource.model_rebuild()
GetSourceSourceDatabricksSource.model_rebuild()
GetSourceSourceDbtModelRunSource.model_rebuild()
GetSourceSourceDbtTestResultSource.model_rebuild()
GetSourceSourceGcpBigQuerySource.model_rebuild()
GetSourceSourceGcpPubSubLiteSource.model_rebuild()
GetSourceSourceGcpPubSubLiteSourceConfig.model_rebuild()
GetSourceSourceGcpPubSubSource.model_rebuild()
GetSourceSourceGcpPubSubSourceConfig.model_rebuild()
GetSourceSourceGcpStorageSource.model_rebuild()
GetSourceSourceGcpStorageSourceConfig.model_rebuild()
GetSourceSourceKafkaSource.model_rebuild()
GetSourceSourceKafkaSourceConfig.model_rebuild()
GetSourceSourcePostgreSqlSource.model_rebuild()
GetSourceSourceSnowflakeSource.model_rebuild()
