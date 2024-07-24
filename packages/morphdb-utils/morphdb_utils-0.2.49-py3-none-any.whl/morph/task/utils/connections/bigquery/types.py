from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class BigqueryExecption(Exception):
    def __init__(
        self, message: str, code: int, errors: List[Dict[str, Any]], status: str
    ):
        super().__init__(message)
        self.code = code
        self.errors = errors
        self.status = status


class BigqueryFieldTypes(Enum):
    INTEGER = "INTEGER"
    INT64 = "INT64"
    FLOAT = "FLOAT"
    FLOAT64 = "FLOAT64"
    STRING = "STRING"
    BYTES = "BYTES"
    BOOLEAN = "BOOLEAN"
    BOOL = "BOOL"
    TIMESTAMP = "TIMESTAMP"
    DATE = "DATE"
    TIME = "TIME"
    DATETIME = "DATETIME"
    GEOGRAPHY = "GEOGRAPHY"
    RECORD = "RECORD"
    STRUCT = "STRUCT"
    NUMERIC = "NUMERIC"
    BIGNUMERIC = "BIGNUMERIC"
    JSON = "JSON"


class BigqueryFieldModes(Enum):
    NULLABLE = "NULLABLE"
    REQUIRED = "REQUIRED"
    REPEATED = "REPEATED"


@dataclass
class BigqueryTableFieldSchema:
    name: str
    type: BigqueryFieldTypes
    mode: BigqueryFieldModes
    fields: List["BigqueryTableFieldSchema"] = field(default_factory=list)
    description: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BigqueryTableFieldSchema":
        fields = [cls.from_dict(field) for field in data.get("fields", [])]
        return cls(
            name=data["name"],
            type=BigqueryFieldTypes[data["type"]],
            mode=BigqueryFieldModes[data["mode"]],
            fields=fields,
            description=data.get("description"),
        )


@dataclass
class BigqueryTableSchema:
    fields: List[BigqueryTableFieldSchema] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BigqueryTableSchema":
        fields = [
            BigqueryTableFieldSchema.from_dict(field)
            for field in data.get("fields", [])
        ]
        return cls(fields=fields)


@dataclass
class BigqueryQueryResponse:
    schema: BigqueryTableSchema
    rows: List[Dict[str, Any]]
    next_token: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BigqueryQueryResponse":
        schema = BigqueryTableSchema.from_dict(data["schema"])
        return cls(schema=schema, rows=data["rows"], next_token=data.get("next_token"))


@dataclass
class BigqueryQueryErrorResponse:
    code: int
    message: str
