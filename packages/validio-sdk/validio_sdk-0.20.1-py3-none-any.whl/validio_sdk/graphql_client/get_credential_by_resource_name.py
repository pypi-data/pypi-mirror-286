from datetime import datetime
from typing import Annotated, List, Literal, Optional, Union

from pydantic import Field

from validio_sdk.scalars import CredentialId

from .base_model import BaseModel
from .enums import AzureSynapseBackendType, ClickHouseProtocol
from .fragments import CredentialBase


class GetCredentialByResourceName(BaseModel):
    credential_by_resource_name: Optional[
        Annotated[
            Union[
                "GetCredentialByResourceNameCredentialByResourceNameCredential",
                "GetCredentialByResourceNameCredentialByResourceNameAwsAthenaCredential",
                "GetCredentialByResourceNameCredentialByResourceNameAwsCredential",
                "GetCredentialByResourceNameCredentialByResourceNameAwsRedshiftCredential",
                "GetCredentialByResourceNameCredentialByResourceNameAzureSynapseEntraIdCredential",
                "GetCredentialByResourceNameCredentialByResourceNameAzureSynapseSqlCredential",
                "GetCredentialByResourceNameCredentialByResourceNameClickHouseCredential",
                "GetCredentialByResourceNameCredentialByResourceNameDatabricksCredential",
                "GetCredentialByResourceNameCredentialByResourceNameDbtCloudCredential",
                "GetCredentialByResourceNameCredentialByResourceNameDbtCoreCredential",
                "GetCredentialByResourceNameCredentialByResourceNameGcpCredential",
                "GetCredentialByResourceNameCredentialByResourceNameKafkaSaslSslPlainCredential",
                "GetCredentialByResourceNameCredentialByResourceNameKafkaSslCredential",
                "GetCredentialByResourceNameCredentialByResourceNameLookerCredential",
                "GetCredentialByResourceNameCredentialByResourceNamePostgreSqlCredential",
                "GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredential",
                "GetCredentialByResourceNameCredentialByResourceNameTableauConnectedAppCredential",
                "GetCredentialByResourceNameCredentialByResourceNameTableauPersonalAccessTokenCredential",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="credentialByResourceName")


class GetCredentialByResourceNameCredentialByResourceNameCredential(BaseModel):
    typename__: Literal["Credential", "DemoCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetCredentialByResourceNameCredentialByResourceNameAwsAthenaCredential(BaseModel):
    typename__: Literal["AwsAthenaCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: (
        "GetCredentialByResourceNameCredentialByResourceNameAwsAthenaCredentialConfig"
    )
    enable_catalog: bool = Field(alias="enableCatalog")


class GetCredentialByResourceNameCredentialByResourceNameAwsAthenaCredentialConfig(
    BaseModel
):
    access_key: str = Field(alias="accessKey")
    region: str
    query_result_location: str = Field(alias="queryResultLocation")


class GetCredentialByResourceNameCredentialByResourceNameAwsCredential(BaseModel):
    typename__: Literal["AwsCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetCredentialByResourceNameCredentialByResourceNameAwsCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class GetCredentialByResourceNameCredentialByResourceNameAwsCredentialConfig(BaseModel):
    access_key: str = Field(alias="accessKey")


class GetCredentialByResourceNameCredentialByResourceNameAwsRedshiftCredential(
    BaseModel
):
    typename__: Literal["AwsRedshiftCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: (
        "GetCredentialByResourceNameCredentialByResourceNameAwsRedshiftCredentialConfig"
    )
    enable_catalog: bool = Field(alias="enableCatalog")


class GetCredentialByResourceNameCredentialByResourceNameAwsRedshiftCredentialConfig(
    BaseModel
):
    host: str
    port: int
    user: str
    default_database: str = Field(alias="defaultDatabase")


class GetCredentialByResourceNameCredentialByResourceNameAzureSynapseEntraIdCredential(
    BaseModel
):
    typename__: Literal["AzureSynapseEntraIdCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetCredentialByResourceNameCredentialByResourceNameAzureSynapseEntraIdCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class GetCredentialByResourceNameCredentialByResourceNameAzureSynapseEntraIdCredentialConfig(
    BaseModel
):
    client_id: str = Field(alias="clientId")
    host: str
    port: int
    database: Optional[str]
    backend_type: AzureSynapseBackendType = Field(alias="backendType")


class GetCredentialByResourceNameCredentialByResourceNameAzureSynapseSqlCredential(
    BaseModel
):
    typename__: Literal["AzureSynapseSqlCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetCredentialByResourceNameCredentialByResourceNameAzureSynapseSqlCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class GetCredentialByResourceNameCredentialByResourceNameAzureSynapseSqlCredentialConfig(
    BaseModel
):
    username: str
    host: str
    port: int
    database: Optional[str]
    backend_type: AzureSynapseBackendType = Field(alias="backendType")


class GetCredentialByResourceNameCredentialByResourceNameClickHouseCredential(
    BaseModel
):
    typename__: Literal["ClickHouseCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: (
        "GetCredentialByResourceNameCredentialByResourceNameClickHouseCredentialConfig"
    )
    enable_catalog: bool = Field(alias="enableCatalog")


class GetCredentialByResourceNameCredentialByResourceNameClickHouseCredentialConfig(
    BaseModel
):
    protocol: ClickHouseProtocol
    host: str
    port: int
    username: str
    default_database: str = Field(alias="defaultDatabase")


class GetCredentialByResourceNameCredentialByResourceNameDatabricksCredential(
    BaseModel
):
    typename__: Literal["DatabricksCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: (
        "GetCredentialByResourceNameCredentialByResourceNameDatabricksCredentialConfig"
    )
    enable_catalog: bool = Field(alias="enableCatalog")


class GetCredentialByResourceNameCredentialByResourceNameDatabricksCredentialConfig(
    BaseModel
):
    host: str
    port: int
    http_path: str = Field(alias="httpPath")


class GetCredentialByResourceNameCredentialByResourceNameDbtCloudCredential(BaseModel):
    typename__: Literal["DbtCloudCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: (
        "GetCredentialByResourceNameCredentialByResourceNameDbtCloudCredentialConfig"
    )


class GetCredentialByResourceNameCredentialByResourceNameDbtCloudCredentialConfig(
    BaseModel
):
    warehouse_credential: (
        "GetCredentialByResourceNameCredentialByResourceNameDbtCloudCredentialConfigWarehouseCredential"
    ) = Field(alias="warehouseCredential")
    account_id: str = Field(alias="accountId")
    api_base_url: Optional[str] = Field(alias="apiBaseUrl")


class GetCredentialByResourceNameCredentialByResourceNameDbtCloudCredentialConfigWarehouseCredential(
    CredentialBase
):
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


class GetCredentialByResourceNameCredentialByResourceNameDbtCoreCredential(BaseModel):
    typename__: Literal["DbtCoreCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetCredentialByResourceNameCredentialByResourceNameDbtCoreCredentialConfig"


class GetCredentialByResourceNameCredentialByResourceNameDbtCoreCredentialConfig(
    BaseModel
):
    warehouse_credential: (
        "GetCredentialByResourceNameCredentialByResourceNameDbtCoreCredentialConfigWarehouseCredential"
    ) = Field(alias="warehouseCredential")


class GetCredentialByResourceNameCredentialByResourceNameDbtCoreCredentialConfigWarehouseCredential(
    CredentialBase
):
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


class GetCredentialByResourceNameCredentialByResourceNameGcpCredential(BaseModel):
    typename__: Literal["GcpCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    enable_catalog: bool = Field(alias="enableCatalog")


class GetCredentialByResourceNameCredentialByResourceNameKafkaSaslSslPlainCredential(
    BaseModel
):
    typename__: Literal["KafkaSaslSslPlainCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetCredentialByResourceNameCredentialByResourceNameKafkaSaslSslPlainCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class GetCredentialByResourceNameCredentialByResourceNameKafkaSaslSslPlainCredentialConfig(
    BaseModel
):
    bootstrap_servers: List[str] = Field(alias="bootstrapServers")
    username: str


class GetCredentialByResourceNameCredentialByResourceNameKafkaSslCredential(BaseModel):
    typename__: Literal["KafkaSslCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: (
        "GetCredentialByResourceNameCredentialByResourceNameKafkaSslCredentialConfig"
    )
    enable_catalog: bool = Field(alias="enableCatalog")


class GetCredentialByResourceNameCredentialByResourceNameKafkaSslCredentialConfig(
    BaseModel
):
    bootstrap_servers: List[str] = Field(alias="bootstrapServers")
    ca_certificate: str = Field(alias="caCertificate")


class GetCredentialByResourceNameCredentialByResourceNameLookerCredential(BaseModel):
    typename__: Literal["LookerCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetCredentialByResourceNameCredentialByResourceNameLookerCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class GetCredentialByResourceNameCredentialByResourceNameLookerCredentialConfig(
    BaseModel
):
    base_url: str = Field(alias="baseUrl")
    client_id: str = Field(alias="clientId")


class GetCredentialByResourceNameCredentialByResourceNamePostgreSqlCredential(
    BaseModel
):
    typename__: Literal["PostgreSqlCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: (
        "GetCredentialByResourceNameCredentialByResourceNamePostgreSqlCredentialConfig"
    )
    enable_catalog: bool = Field(alias="enableCatalog")


class GetCredentialByResourceNameCredentialByResourceNamePostgreSqlCredentialConfig(
    BaseModel
):
    host: str
    port: int
    user: str
    default_database: str = Field(alias="defaultDatabase")


class GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredential(BaseModel):
    typename__: Literal["SnowflakeCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: (
        "GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredentialConfig"
    )
    enable_catalog: bool = Field(alias="enableCatalog")


class GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredentialConfig(
    BaseModel
):
    account: str
    user: str
    role: Optional[str]
    warehouse: Optional[str]


class GetCredentialByResourceNameCredentialByResourceNameTableauConnectedAppCredential(
    BaseModel
):
    typename__: Literal["TableauConnectedAppCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetCredentialByResourceNameCredentialByResourceNameTableauConnectedAppCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class GetCredentialByResourceNameCredentialByResourceNameTableauConnectedAppCredentialConfig(
    BaseModel
):
    host: str
    site: str
    user: str
    client_id: str = Field(alias="clientId")
    secret_id: str = Field(alias="secretId")


class GetCredentialByResourceNameCredentialByResourceNameTableauPersonalAccessTokenCredential(
    BaseModel
):
    typename__: Literal["TableauPersonalAccessTokenCredential"] = Field(
        alias="__typename"
    )
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetCredentialByResourceNameCredentialByResourceNameTableauPersonalAccessTokenCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class GetCredentialByResourceNameCredentialByResourceNameTableauPersonalAccessTokenCredentialConfig(
    BaseModel
):
    host: str
    site: str
    token_name: str = Field(alias="tokenName")


GetCredentialByResourceName.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameAwsAthenaCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameAwsCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameAwsRedshiftCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameAzureSynapseEntraIdCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameAzureSynapseSqlCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameClickHouseCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameDatabricksCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameDbtCloudCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameDbtCloudCredentialConfig.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameDbtCoreCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameDbtCoreCredentialConfig.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameKafkaSaslSslPlainCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameKafkaSslCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameLookerCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNamePostgreSqlCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameTableauConnectedAppCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameTableauPersonalAccessTokenCredential.model_rebuild()
