import configparser
import json
import os
import re
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Union

import click
import requests
import yaml

from morph.task.constant.project_config import ProjectConfig


class CONNECTION_TYPE(Enum):
    postgres = "postgres"
    mysql = "mysql"
    redshift = "redshift"
    snowflake = "snowflake"
    bigquery = "bigquery"


class CONNECTION_DETAIL_TYPE(Enum):
    postgres = "postgres"
    mysql = "mysql"
    redshift = "redshift"
    snowflake_user_password = "snowflake_user_password"
    snowflake_key_pair = "snowflake_key_pair"
    snowflake_key_pair_file = "snowflake_key_pair_file"
    snowflake_oauth = "snowflake_oauth"
    bigquery_oauth = "bigquery_oauth"
    bigquery_service_account = "bigquery_service_account"
    bigquery_service_account_json = "bigquery_service_account_json"


class CONNECTION_METHOD(Enum):
    user_password = "user_password"
    oauth = "oauth"
    key_pair = "key_pair"
    key_pair_file = "key_pair_file"
    service_account = "service_account"
    service_account_json = "service_account_json"


@dataclass
class PostgresqlConnection:
    type: Literal[CONNECTION_TYPE.postgres]
    host: str
    user: str
    password: str
    port: int
    dbname: str
    schema: Optional[str] = None
    ssh_host: Optional[str] = None
    ssh_port: Optional[int] = None
    ssh_user: Optional[str] = None
    ssh_password: Optional[str] = None
    ssh_private_key: Optional[str] = None


@dataclass
class MysqlConnection:
    type: Literal[CONNECTION_TYPE.mysql]
    host: str
    user: str
    password: str
    port: int
    dbname: str
    ssh_host: Optional[str] = None
    ssh_port: Optional[int] = None
    ssh_user: Optional[str] = None
    ssh_password: Optional[str] = None
    ssh_private_key: Optional[str] = None


@dataclass
class RedshiftConnection:
    type: Literal[CONNECTION_TYPE.redshift]
    host: str
    user: str
    password: str
    port: int
    dbname: str
    schema: Optional[str] = None
    ssh_host: Optional[str] = None
    ssh_port: Optional[int] = None
    ssh_user: Optional[str] = None
    ssh_password: Optional[str] = None
    ssh_private_key: Optional[str] = None


@dataclass
class SnowflakeConnectionUserPassword:
    type: Literal[CONNECTION_TYPE.snowflake]
    method: Literal[CONNECTION_DETAIL_TYPE.snowflake_user_password]
    account: str
    database: str
    user: str
    password: str
    role: str
    schema: str
    warehouse: str


@dataclass
class SnowflakeConnectionOAuth:
    type: Literal[CONNECTION_TYPE.snowflake]
    method: Literal[CONNECTION_DETAIL_TYPE.snowflake_oauth]
    account: str
    database: str
    refresh_token: str
    client_id: str
    client_secret: str
    redirect_uri: str
    role: str
    schema: str
    warehouse: str
    code_verifier: str
    access_token: Optional[str] = None


@dataclass
class SnowflakeConnectionKeyPair:
    type: Literal[CONNECTION_TYPE.snowflake]
    method: Literal[CONNECTION_DETAIL_TYPE.snowflake_key_pair]
    account: str
    username: str
    database: str
    key_pair: str
    role: str
    schema: str
    warehouse: str
    passphrase: Optional[str] = None
    access_token: Optional[str] = None


@dataclass
class SnowflakeConnectionKeyPairFile:
    type: Literal[CONNECTION_TYPE.snowflake]
    method: Literal[CONNECTION_DETAIL_TYPE.snowflake_key_pair_file]
    account: str
    username: str
    database: str
    key_pair_path: str
    role: str
    schema: str
    warehouse: str
    passphrase: Optional[str] = None


@dataclass
class BigqueryConnectionOAuth:
    type: Literal[CONNECTION_TYPE.bigquery]
    method: Literal[CONNECTION_DETAIL_TYPE.bigquery_oauth]
    project: str
    dataset: str
    refresh_token: str
    client_id: str
    client_secret: str
    redirect_uri: str
    location: Optional[str] = None
    access_token: Optional[str] = None


@dataclass
class BigqueryConnectionServiceAccount:
    type: Literal[CONNECTION_TYPE.bigquery]
    method: Literal[CONNECTION_DETAIL_TYPE.bigquery_service_account]
    project: str
    dataset: str
    keyfile: str
    location: Optional[str] = None


@dataclass
class BigqueryConnectionServiceAccountJsonKeyFile:
    project_id: str
    private_key_id: str
    private_key: str
    client_email: str
    client_id: str
    auth_uri: str
    token_uri: str
    auth_provider_x509_cert_url: str
    client_x509_cert_url: str
    location: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BigqueryConnectionServiceAccountJson:
    type: Literal[CONNECTION_TYPE.bigquery]
    method: Literal[CONNECTION_DETAIL_TYPE.bigquery_service_account_json]
    project: str
    dataset: str
    keyfile_json: BigqueryConnectionServiceAccountJsonKeyFile
    location: Optional[str] = None
    access_token: Optional[str] = None


@dataclass
class ExternalConnectionAuth:
    authType: str
    data: Optional[Dict[str, Any]] = None

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "ExternalConnectionAuth":
        return ExternalConnectionAuth(
            authType=data["authType"], data=data.get("data", {})
        )


@dataclass
class ExternalConnection:
    connectionId: str
    connectionSlug: str
    connectionType: str
    data: Dict[str, Any]
    createdAt: str
    connectionAuth: Optional[ExternalConnectionAuth] = None
    databaseIds: List[str] = field(default_factory=list)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "ExternalConnection":
        connectionAuth = data.get("connectionAuth", None)
        if connectionAuth and isinstance(connectionAuth, dict):
            connectionAuth = ExternalConnectionAuth.from_dict(connectionAuth)
        return ExternalConnection(
            connectionId=data["connectionId"],
            connectionSlug=data["connectionSlug"],
            connectionType=data["connectionType"],
            data=data["data"],
            createdAt=data["createdAt"],
            connectionAuth=connectionAuth,
            databaseIds=data.get("databaseIds", []),
        )


@dataclass
class ExternalConnectionListResponse:
    items: List[ExternalConnection]
    count: int

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "ExternalConnectionListResponse":
        items = [ExternalConnection.from_dict(item) for item in data["items"]]
        return ExternalConnectionListResponse(items=items, count=data["count"])


@dataclass
class ProfileYaml:
    """
    connections:
        slug:
            each connection info...
    """

    connections: Dict[
        str,
        Union[
            PostgresqlConnection,
            MysqlConnection,
            RedshiftConnection,
            SnowflakeConnectionUserPassword,
            SnowflakeConnectionOAuth,
            SnowflakeConnectionKeyPair,
            SnowflakeConnectionKeyPairFile,
            BigqueryConnectionOAuth,
            BigqueryConnectionServiceAccount,
            BigqueryConnectionServiceAccountJson,
        ],
    ] = field(default_factory=dict)

    @staticmethod
    def is_file_exits() -> bool:
        return os.path.isfile(ProjectConfig.MORPH_PROFILE_PATH)

    @staticmethod
    def from_dict(data: dict) -> "ProfileYaml":
        connections_data = data.get("connections", {})
        if isinstance(connections_data, dict):
            connections = {
                slug: connection_info
                for slug, connection_info in connections_data.items()
            }
        elif isinstance(connections_data, list):
            connections = {
                str(index): item for index, item in enumerate(connections_data)
            }
        else:
            connections = {}
        return ProfileYaml(connections=connections)

    @staticmethod
    def load_yaml() -> "ProfileYaml":
        if not ProfileYaml.is_file_exits():
            with open(ProjectConfig.MORPH_PROFILE_PATH, "w") as file:
                yaml.dump({"connections": []}, file)

        with open(ProjectConfig.MORPH_PROFILE_PATH, "r") as file:
            data = yaml.safe_load(file)

        return ProfileYaml.from_dict(data if data is not None else {})

    @staticmethod
    def find_connection(
        connection_slug: str,
    ) -> Optional[
        Union[
            PostgresqlConnection,
            MysqlConnection,
            RedshiftConnection,
            SnowflakeConnectionUserPassword,
            SnowflakeConnectionOAuth,
            SnowflakeConnectionKeyPair,
            SnowflakeConnectionKeyPairFile,
            BigqueryConnectionOAuth,
            BigqueryConnectionServiceAccount,
            BigqueryConnectionServiceAccountJson,
        ]
    ]:
        profile_yaml = ProfileYaml.load_yaml()
        if len(profile_yaml.connections.keys()) < 1:
            ProfileYaml.sync_cloud_connection(override=True)
            profile_yaml = ProfileYaml.load_yaml()

        return profile_yaml.connections.get(connection_slug)

    @staticmethod
    def find_connection_detail_type(
        connection: Union[
            PostgresqlConnection,
            MysqlConnection,
            RedshiftConnection,
            SnowflakeConnectionUserPassword,
            SnowflakeConnectionOAuth,
            SnowflakeConnectionKeyPair,
            SnowflakeConnectionKeyPairFile,
            BigqueryConnectionOAuth,
            BigqueryConnectionServiceAccount,
            BigqueryConnectionServiceAccountJson,
        ]
    ) -> str:
        if isinstance(connection, PostgresqlConnection):
            return CONNECTION_DETAIL_TYPE.postgres.value
        elif isinstance(connection, MysqlConnection):
            return CONNECTION_DETAIL_TYPE.mysql.value
        elif isinstance(connection, RedshiftConnection):
            return CONNECTION_DETAIL_TYPE.redshift.value
        elif isinstance(connection, SnowflakeConnectionUserPassword):
            return CONNECTION_DETAIL_TYPE.snowflake_user_password.value
        elif isinstance(connection, SnowflakeConnectionOAuth):
            return CONNECTION_DETAIL_TYPE.snowflake_oauth.value
        elif isinstance(connection, SnowflakeConnectionKeyPair):
            return CONNECTION_DETAIL_TYPE.snowflake_key_pair.value
        elif isinstance(connection, SnowflakeConnectionKeyPairFile):
            return CONNECTION_DETAIL_TYPE.snowflake_key_pair_file.value
        elif isinstance(connection, BigqueryConnectionOAuth):
            return CONNECTION_DETAIL_TYPE.bigquery_oauth.value
        elif isinstance(connection, BigqueryConnectionServiceAccount):
            return CONNECTION_DETAIL_TYPE.bigquery_service_account.value
        elif isinstance(connection, BigqueryConnectionServiceAccountJson):
            return CONNECTION_DETAIL_TYPE.bigquery_service_account_json.value

    @staticmethod
    def find_builtin_db_connection() -> Union[
        PostgresqlConnection,
        MysqlConnection,
        RedshiftConnection,
        SnowflakeConnectionOAuth,
        SnowflakeConnectionKeyPair,
        BigqueryConnectionOAuth,
        BigqueryConnectionServiceAccountJson,
    ]:
        config_path = ProjectConfig.MORPH_CRED_PATH
        if not os.path.exists(config_path):
            click.echo(
                click.style(
                    f"Error: No credentials found in {config_path}.",
                    fg="red",
                )
            )
            raise FileNotFoundError(f"No credentials found in {config_path}.")

        config = configparser.ConfigParser()
        config.read(config_path)
        if not config.sections():
            click.echo(
                click.style(
                    f"Error: No credentials entries found in {config_path}.",
                    fg="red",
                )
            )
            raise FileNotFoundError(f"No credentials entries found in {config_path}.")

        app_url: str = config.get("default", "app_url")
        api_key: str = config.get("default", "api_key")
        database_id: str = config.get("default", "database_id")

        url = f"{app_url}/database/{database_id}/connection"
        headers = {
            "x-api-key": api_key,
        }

        retry_cnt = 0
        while True:
            response = requests.get(url=url, headers=headers, verify=True)
            if response.status_code > 500:
                click.echo(
                    click.style(
                        "Error: Unable to fetch builtin db from cloud.",
                        fg="red",
                    )
                )
                raise SystemError("Unable to fetch builtin db from cloud.")
            else:
                if response.status_code == 500:
                    if retry_cnt < 3:
                        retry_cnt += 1
                        time.sleep(1)
                        continue
                    click.echo(
                        click.style(
                            "Error: Unable to fetch builtin db from cloud.",
                            fg="red",
                        )
                    )
                    raise SystemError("Unable to fetch builtin db from cloud.")

                response_json = response.json()
                if (
                    "error" in response_json
                    and "subCode" in response_json
                    and "message" in response_json
                ):
                    click.echo(
                        click.style(
                            "Error: Unable to fetch builtin db from cloud.",
                            fg="red",
                        )
                    )
                    raise SystemError("Unable to fetch builtin db from cloud.")

                connection_string = response_json["maskedUrl"]
                password = response_json["password"]

                pattern = re.compile(
                    r"postgresql://(?P<username>[^:]+):(?P<password>[^@]+)@(?P<host>[^/]+)/(?P<database>[^?]+)\?sslmode=require"
                )
                match = pattern.search(connection_string)
                if match is None:
                    raise SystemError(
                        "Unable to fetch builtin db from cloud. invalid connection string."
                    )
                username = match.group("username")
                host = match.group("host")
                database = match.group("database")

                return PostgresqlConnection(
                    type=CONNECTION_TYPE.postgres,
                    host=host,
                    user=username,
                    password=password,
                    port=5432,
                    dbname=database,
                    schema="public",
                )

    @staticmethod
    def find_cloud_connection(
        connection_slug: str,
    ) -> Union[
        PostgresqlConnection,
        MysqlConnection,
        RedshiftConnection,
        SnowflakeConnectionOAuth,
        SnowflakeConnectionKeyPair,
        BigqueryConnectionOAuth,
        BigqueryConnectionServiceAccountJson,
    ]:
        config_path = ProjectConfig.MORPH_CRED_PATH
        if not os.path.exists(config_path):
            click.echo(
                click.style(
                    f"Error: No credentials found in {config_path}.",
                    fg="red",
                )
            )
            raise FileNotFoundError(f"No credentials found in {config_path}.")

        config = configparser.ConfigParser()
        config.read(config_path)
        if not config.sections():
            click.echo(
                click.style(
                    f"Error: No credentials entries found in {config_path}.",
                    fg="red",
                )
            )
            raise FileNotFoundError(f"No credentials entries found in {config_path}.")

        app_url: str = config.get("default", "app_url")
        api_key: str = config.get("default", "api_key")

        try:
            url = f"{app_url}/external-connection/{connection_slug}"
            headers = {
                "x-api-key": api_key,
            }
            response = requests.get(url=url, headers=headers, verify=True)

            if response.status_code > 500:
                click.echo(
                    click.style(
                        "Error: Unable to fetch connections from cloud.",
                        fg="red",
                    )
                )
                raise SystemError("Unable to fetch connection from cloud.")
            else:
                response_json = response.json()
                if (
                    "error" in response_json
                    and "subCode" in response_json
                    and "message" in response_json
                ):
                    click.echo(
                        click.style(
                            "Error: Unable to fetch connection from cloud.",
                            fg="red",
                        )
                    )
                    raise SystemError("Unable to fetch connection from cloud.")

                connection_type = response_json["connectionType"]
                auth_type = response_json["authType"]
                data = response_json["data"]
                connection: Optional[
                    Union[
                        PostgresqlConnection,
                        MysqlConnection,
                        RedshiftConnection,
                        SnowflakeConnectionOAuth,
                        SnowflakeConnectionKeyPair,
                        BigqueryConnectionOAuth,
                        BigqueryConnectionServiceAccountJson,
                    ]
                ] = None
                if connection_type == "postgres":
                    connection = PostgresqlConnection(
                        type=CONNECTION_TYPE.postgres,
                        host=data.get("host", ""),
                        user=data.get("username", ""),
                        password=data.get("password", ""),
                        port=data.get("port", 5432),
                        dbname=data.get("database", ""),
                        schema=data.get("schema", ""),
                        ssh_host=data.get("bastionHost"),
                        ssh_port=data.get("bastionPort"),
                        ssh_user=data.get("bastionUsername"),
                        ssh_password=data.get("bastionPassword"),
                        ssh_private_key=data.get("bastionPrivateKey"),
                    )
                elif connection_type == "mysql":
                    connection = MysqlConnection(
                        type=CONNECTION_TYPE.mysql,
                        host=data.get("host", ""),
                        user=data.get("username", ""),
                        password=data.get("password", ""),
                        port=data.get("port", 3306),
                        dbname=data.get("database", ""),
                        ssh_host=data.get("bastionHost"),
                        ssh_port=data.get("bastionPort"),
                        ssh_user=data.get("bastionUsername"),
                        ssh_password=data.get("bastionPassword"),
                        ssh_private_key=data.get("bastionPrivateKey"),
                    )
                elif connection_type == "redshift":
                    connection = RedshiftConnection(
                        type=CONNECTION_TYPE.redshift,
                        host=data.get("host", ""),
                        user=data.get("username", ""),
                        password=data.get("password", ""),
                        port=data.get("port", 5439),
                        dbname=data.get("database", ""),
                        schema=data.get("schema", ""),
                        ssh_host=data.get("bastionHost"),
                        ssh_port=data.get("bastionPort"),
                        ssh_user=data.get("bastionUsername"),
                        ssh_password=data.get("bastionPassword"),
                        ssh_private_key=data.get("bastionPrivateKey"),
                    )
                elif connection_type == "snowflake" and auth_type == "oauth":
                    connection = SnowflakeConnectionOAuth(
                        type=CONNECTION_TYPE.snowflake,
                        method=CONNECTION_DETAIL_TYPE.snowflake_oauth,
                        account=data.get("server", ""),
                        database=data.get("database", ""),
                        refresh_token=data.get("refreshToken", ""),
                        client_id=data.get("clientId", ""),
                        client_secret=data.get("clientSecret", ""),
                        redirect_uri=data.get("redirectUrl", ""),
                        role=data.get("role", ""),
                        schema=data.get("schema", ""),
                        warehouse=data.get("warehouse", ""),
                        code_verifier="",
                        access_token=data.get("accessToken", ""),
                    )
                elif connection_type == "snowflake" and auth_type == "keyPair":
                    connection = SnowflakeConnectionKeyPair(
                        type=CONNECTION_TYPE.snowflake,
                        method=CONNECTION_DETAIL_TYPE.snowflake_key_pair,
                        account=data.get("server", ""),
                        username=data.get("username", ""),
                        database=data.get("database", ""),
                        key_pair=data.get("privateKey", ""),
                        role=data.get("role", ""),
                        schema=data.get("schema", ""),
                        warehouse=data.get("warehouse", ""),
                        passphrase=data.get("passphrase"),
                        access_token=data.get("accessToken", ""),
                    )
                elif connection_type == "bigquery" and auth_type == "oauth":
                    connection = BigqueryConnectionOAuth(
                        type=CONNECTION_TYPE.bigquery,
                        method=CONNECTION_DETAIL_TYPE.bigquery_oauth,
                        project=data.get("projectId", ""),
                        dataset=data.get("dataset", ""),
                        refresh_token=data.get("refreshToken", ""),
                        client_id=data.get("clientId", ""),
                        client_secret=data.get("clientSecret", ""),
                        redirect_uri=data.get("redirectUrl", ""),
                        location=data.get("location"),
                        access_token=data.get("accessToken", ""),
                    )
                elif connection_type == "bigquery" and auth_type == "serviceAccount":
                    credentials = (
                        json.loads(data.get("credentials", "{}"))
                        if type(data.get("credentials")) == str
                        else data.get("credentials", {})
                    )
                    connection = BigqueryConnectionServiceAccountJson(
                        type=CONNECTION_TYPE.bigquery,
                        method=CONNECTION_DETAIL_TYPE.bigquery_service_account_json,
                        project=data.get("projectId", ""),
                        dataset=data.get("dataset", ""),
                        keyfile_json=BigqueryConnectionServiceAccountJsonKeyFile(
                            project_id=credentials.get("project_id", ""),
                            private_key_id=credentials.get("private_key_id", ""),
                            private_key=credentials.get("private_key", ""),
                            client_email=credentials.get("client_email", ""),
                            client_id=credentials.get("client_id", ""),
                            auth_uri=credentials.get("auth_uri", ""),
                            token_uri=credentials.get("token_uri", ""),
                            auth_provider_x509_cert_url=credentials.get(
                                "auth_provider_x509_cert_url", ""
                            ),
                            client_x509_cert_url=credentials.get(
                                "client_x509_cert_url", ""
                            ),
                        ),
                        location=data.get("location"),
                        access_token=data.get("accessToken", ""),
                    )
                else:
                    raise NotImplementedError(
                        f"connection type not implemented {connection_type} {auth_type}"
                    )
            return connection
        except Exception as e:
            raise SystemError(f"Unable to fetch connection from cloud. {e}")

    @staticmethod
    def sync_cloud_connection(override: Optional[bool] = False) -> None:
        config_path = ProjectConfig.MORPH_CRED_PATH
        if not os.path.exists(config_path):
            click.echo(
                click.style(
                    f"Error: No credentials found in {config_path}.",
                    fg="red",
                )
            )
            raise FileNotFoundError(f"No credentials found in {config_path}.")

        config = configparser.ConfigParser()
        config.read(config_path)
        if not config.sections():
            click.echo(
                click.style(
                    f"Error: No credentials entries found in {config_path}.",
                    fg="red",
                )
            )
            raise FileNotFoundError(f"No credentials entries found in {config_path}.")

        app_url: str = config.get("default", "app_url")
        api_key: str = config.get("default", "api_key")

        try:
            url = f"{app_url}/external-connection?withAuth=true"
            headers = {
                "x-api-key": api_key,
            }
            response = requests.get(url=url, headers=headers, verify=True)

            if response.status_code > 500:
                click.echo(
                    click.style(
                        "Error: Unable to fetch connections from cloud.",
                        fg="red",
                    )
                )
                return
            else:
                response_json = response.json()
                if (
                    "error" in response_json
                    and "subCode" in response_json
                    and "message" in response_json
                ):
                    click.echo(
                        click.style(
                            "Error: Unable to fetch connections from cloud.",
                            fg="red",
                        )
                    )
                    return

                connections: Dict[
                    str,
                    Union[
                        PostgresqlConnection,
                        MysqlConnection,
                        RedshiftConnection,
                        SnowflakeConnectionUserPassword,
                        SnowflakeConnectionOAuth,
                        SnowflakeConnectionKeyPair,
                        SnowflakeConnectionKeyPairFile,
                        BigqueryConnectionOAuth,
                        BigqueryConnectionServiceAccount,
                        BigqueryConnectionServiceAccountJson,
                    ],
                ] = {}

                items = ExternalConnectionListResponse.from_dict(response_json).items

                for item in items:
                    connection_slug = item.connectionSlug
                    connection_type = item.connectionType
                    data = item.data
                    connection_auth = item.connectionAuth
                    auth_type = None
                    auth_data = None
                    if connection_auth is not None and connection_auth != "":
                        auth_type = connection_auth.authType
                        auth_data = connection_auth.data

                    if data is None or (
                        connection_type == "snowflake"
                        and connection_type == "bigquery"
                        and auth_data is None
                    ):
                        continue

                    connection: Optional[
                        Union[
                            PostgresqlConnection,
                            MysqlConnection,
                            RedshiftConnection,
                            SnowflakeConnectionUserPassword,
                            SnowflakeConnectionOAuth,
                            SnowflakeConnectionKeyPair,
                            SnowflakeConnectionKeyPairFile,
                            BigqueryConnectionOAuth,
                            BigqueryConnectionServiceAccount,
                            BigqueryConnectionServiceAccountJson,
                        ]
                    ] = None
                    if connection_type == "postgres":
                        connection = PostgresqlConnection(
                            type=CONNECTION_TYPE.postgres,
                            host=data.get("host", ""),
                            user=data.get("username", ""),
                            password=data.get("password", ""),
                            port=data.get("port", 5432),
                            dbname=data.get("database", ""),
                            schema=data.get("schema", ""),
                            ssh_host=data.get("bastionHost"),
                            ssh_port=data.get("bastionPort"),
                            ssh_user=data.get("bastionUsername"),
                            ssh_password=data.get("bastionPassword"),
                            ssh_private_key=data.get("bastionPrivateKey"),
                        )
                    elif connection_type == "mysql":
                        connection = MysqlConnection(
                            type=CONNECTION_TYPE.mysql,
                            host=data.get("host", ""),
                            user=data.get("username", ""),
                            password=data.get("password", ""),
                            port=data.get("port", 3306),
                            dbname=data.get("database", ""),
                            ssh_host=data.get("bastionHost"),
                            ssh_port=data.get("bastionPort"),
                            ssh_user=data.get("bastionUsername"),
                            ssh_password=data.get("bastionPassword"),
                            ssh_private_key=data.get("bastionPrivateKey"),
                        )
                    elif connection_type == "redshift":
                        connection = RedshiftConnection(
                            type=CONNECTION_TYPE.redshift,
                            host=data.get("host", ""),
                            user=data.get("username", ""),
                            password=data.get("password", ""),
                            port=data.get("port", 5439),
                            dbname=data.get("database", ""),
                            schema=data.get("schema", ""),
                            ssh_host=data.get("bastionHost"),
                            ssh_port=data.get("bastionPort"),
                            ssh_user=data.get("bastionUsername"),
                            ssh_password=data.get("bastionPassword"),
                            ssh_private_key=data.get("bastionPrivateKey"),
                        )
                    elif connection_type == "snowflake" and auth_type == "keyPair":
                        if auth_data is None:
                            continue
                        connection = SnowflakeConnectionKeyPair(
                            type=CONNECTION_TYPE.snowflake,
                            method=CONNECTION_DETAIL_TYPE.snowflake_key_pair,
                            account=auth_data.get("server", ""),
                            username=auth_data.get("username", ""),
                            database=data.get("database", ""),
                            key_pair=auth_data.get("privateKey", ""),
                            role=data.get("role", ""),
                            schema=data.get("schema", ""),
                            warehouse=data.get("warehouse", ""),
                            passphrase=data.get("passphrase"),
                        )
                    elif (
                        connection_type == "bigquery" and auth_type == "serviceAccount"
                    ):
                        if auth_data is None:
                            continue
                        credentials = (
                            json.loads(auth_data.get("credentials", "{}"))
                            if type(auth_data.get("credentials")) == str
                            else auth_data.get("credentials", {})
                        )
                        connection = BigqueryConnectionServiceAccountJson(
                            type=CONNECTION_TYPE.bigquery,
                            method=CONNECTION_DETAIL_TYPE.bigquery_service_account_json,
                            project=data.get("projectId", ""),
                            dataset=data.get("dataset", ""),
                            keyfile_json=BigqueryConnectionServiceAccountJsonKeyFile(
                                project_id=credentials.get("project_id", ""),
                                private_key_id=credentials.get("private_key_id", ""),
                                private_key=credentials.get("private_key", ""),
                                client_email=credentials.get("client_email", ""),
                                client_id=credentials.get("client_id", ""),
                                auth_uri=credentials.get("auth_uri", ""),
                                token_uri=credentials.get("token_uri", ""),
                                auth_provider_x509_cert_url=credentials.get(
                                    "auth_provider_x509_cert_url", ""
                                ),
                                client_x509_cert_url=credentials.get(
                                    "client_x509_cert_url", ""
                                ),
                            ),
                            location=data.get("location"),
                        )
                    else:
                        continue

                    connections[connection_slug] = connection

                if len(connections.keys()) > 0:
                    profile = ProfileYaml.load_yaml()
                    profile.add_connections(connections)
                    profile.save_yaml(override)
        except Exception as e:
            click.echo(
                click.style(
                    f"Error: Failed to sync connections. {str(e)}",
                    fg="red",
                )
            )

    def to_dict(self) -> Any:
        def convert(obj):
            if isinstance(obj, Enum):
                return obj.value
            elif isinstance(obj, list):
                return [convert(i) for i in obj]
            elif isinstance(obj, dict):
                return {k: convert(v) for k, v in obj.items()}
            elif hasattr(obj, "__dict__"):
                return {k: convert(v) for k, v in asdict(obj).items()}
            else:
                return obj

        return convert(asdict(self))

    def add_connections(self, connections: Dict[str, Any]) -> None:
        self.connections.update(connections)

    def save_yaml(self, override: Optional[bool] = False) -> None:
        if override or (
            not override
            and (self.connections is None or len(self.connections.keys()) == 0)
        ):
            with open(ProjectConfig.MORPH_PROFILE_PATH, "w") as file:
                yaml.dump(self.to_dict(), file)
