from __future__ import annotations

from typing import Literal

try:
    from pydantic import BaseModel, ConfigDict, Field
except ImportError:  # pragma: no cover

    class BaseModel:  # type: ignore[no-redef]
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

        @classmethod
        def model_validate(cls, payload: dict):
            return cls(**payload)

        def model_dump(self) -> dict:
            def _serialize(value):
                if isinstance(value, BaseModel):
                    return value.model_dump()
                if isinstance(value, list):
                    return [_serialize(v) for v in value]
                if isinstance(value, dict):
                    return {k: _serialize(v) for k, v in value.items()}
                return value

            return {k: _serialize(v) for k, v in self.__dict__.items()}

        def model_dump_json(self, indent: int = 2) -> str:
            import json

            return json.dumps(self.model_dump(), indent=indent)

    def Field(default=None, **kwargs):  # type: ignore[no-redef]
        return default

    ConfigDict = dict  # type: ignore[assignment]


class BoMItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    item_name: str = Field(min_length=1)
    category: Literal["fixture", "pipe", "fitting", "other"]
    size: str = Field(default="N/A", min_length=1)
    quantity: float = Field(ge=0)
    page_numbers: list[int] = Field(default_factory=list)
    evidence_snippets: list[str] = Field(default_factory=list)
    confidence_score: float = Field(ge=0, le=1)


class BoMReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_file: str = Field(min_length=1)
    extraction_mode: Literal["vector", "scanned", "mixed"]
    items: list[BoMItem] = Field(default_factory=list)
