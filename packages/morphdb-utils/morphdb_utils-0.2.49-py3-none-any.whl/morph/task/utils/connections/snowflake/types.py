from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union, cast

T = TypeVar("T")


class SnowflakeExecption(Exception):
    def __init__(self, message, code=None, sqlState=None, statementHandle=None):
        super().__init__(message)
        self.code = code
        self.sqlState = sqlState
        self.statementHandle = statementHandle


class SnowflakeNetworkResponse(Generic[T]):
    def __init__(self, data: T, status: int):
        self.data = data
        self.status = status


class SnowflakeNetworkErrorResponse:
    def __init__(self, code: str, message: str, sqlState: str, statementHandle: str):
        self.code = code
        self.message = message
        self.sqlState = sqlState
        self.statementHandle = statementHandle


def is_snowflake_network_error(input: Any) -> bool:
    return isinstance(input, SnowflakeNetworkErrorResponse) or (
        isinstance(input, dict)
        and "code" in input
        and "message" in input
        and "sqlState" in input
        and "statementHandle" in input
    )


class SnowflakeOAuthError:
    def __init__(self, code: str, message: str):
        if code != "390318":
            raise ValueError("code must be '390318'")
        self.code = code
        self.message = message


def is_snowflake_oauth_error(input: Any) -> bool:
    return isinstance(input, SnowflakeOAuthError) or (
        isinstance(input, dict)
        and "code" in input
        and input["code"] == "390318"
        and "message" in input
        and isinstance(input["message"], str)
    )


class SnowflakeRowTypeFieldType(Enum):
    NUMBER = "NUMBER"
    DECIMAL = "DECIMAL"
    NUMERIC = "NUMERIC"
    INT = "INT"
    INTEGER = "INTEGER"
    BIGINT = "BIGINT"
    SMALLINT = "SMALLINT"
    TINYINT = "TINYINT"
    BYTEINT = "BYTEINT"
    FLOAT = "FLOAT"
    FLOAT4 = "FLOAT4"
    FLOAT8 = "FLOAT8"
    FIXED = "FIXED"
    REAL = "REAL"
    DOUBLE = "DOUBLE"
    DOUBLE_PRECISION = "DOUBLE PRECISION"
    VARCHAR = "VARCHAR"
    CHAR = "CHAR"
    CHARACTER = "CHARACTER"
    STRING = "STRING"
    TEXT = "TEXT"
    BINARY = "BINARY"
    VARBINARY = "VARBINARY"
    BOOLEAN = "BOOLEAN"
    DATE = "DATE"
    DATETIME = "DATETIME"
    TIME = "TIME"
    TIMESTAMP = "TIMESTAMP"
    TIMESTAMP_LTZ = "TIMESTAMP_LTZ"
    TIMESTAMP_NTZ = "TIMESTAMP_NTZ"
    TIMESTAMP_TZ = "TIMESTAMP_TZ"
    VARIANT = "VARIANT"
    OBJECT = "OBJECT"
    ARRAY = "ARRAY"
    GEOGRAPHY = "GEOGRAPHY"


@dataclass
class SnowflakeRowType:
    name: str
    database: str
    schema: str
    table: str
    precision: Optional[int]
    byteLength: Optional[int]
    scale: Optional[int]
    type: SnowflakeRowTypeFieldType
    nullable: bool
    collation: Optional[str]
    length: Optional[int]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SnowflakeRowType":
        return cls(
            name=data["name"],
            database=data["database"],
            schema=data["schema"],
            table=data["table"],
            precision=data.get("precision"),
            byteLength=data.get("byteLength"),
            scale=data.get("scale"),
            type=SnowflakeRowTypeFieldType[data["type"].upper()],
            nullable=data["nullable"],
            collation=data.get("collation"),
            length=data.get("length"),
        )


@dataclass
class PartitionInfo:
    rowCount: int
    uncompressedSize: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PartitionInfo":
        return cls(rowCount=data["rowCount"], uncompressedSize=data["uncompressedSize"])


@dataclass
class ResultSetMetaData:
    numRows: int
    format: str
    partitionInfo: List[PartitionInfo]
    rowType: List[SnowflakeRowType]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ResultSetMetaData":
        partitionInfo = [PartitionInfo.from_dict(pi) for pi in data["partitionInfo"]]
        rowType = [SnowflakeRowType.from_dict(rt) for rt in data["rowType"]]
        return cls(
            numRows=data["numRows"],
            format=data["format"],
            partitionInfo=partitionInfo,
            rowType=rowType,
        )


@dataclass
class SnowflakeExecuteSqlStatementsResponse:
    resultSetMetaData: ResultSetMetaData
    data: List[List[Union[str, int, float, bool, None]]]
    code: str
    statementStatusUrl: str
    requestId: str
    sqlState: str
    statementHandle: str
    message: str
    createdOn: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SnowflakeExecuteSqlStatementsResponse":
        resultSetMetaData = ResultSetMetaData.from_dict(data["resultSetMetaData"])
        return cls(
            resultSetMetaData=resultSetMetaData,
            data=data["data"],
            code=data["code"],
            statementStatusUrl=data["statementStatusUrl"],
            requestId=data["requestId"],
            sqlState=data["sqlState"],
            statementHandle=data["statementHandle"],
            message=data["message"],
            createdOn=data["createdOn"],
        )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class SnowflakeExecuteSqlImplResponse:
    data: SnowflakeExecuteSqlStatementsResponse
    status: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SnowflakeExecuteSqlImplResponse":
        data_ = SnowflakeExecuteSqlStatementsResponse.from_dict(
            cast(Dict[str, Any], data["data"])
        )
        return cls(data=data_, status=data["status"])
