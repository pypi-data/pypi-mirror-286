# coding: utf-8

"""
    Hatchet API

    The Hatchet API

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations

import json
import pprint
import re  # noqa: F401
from typing import Any, ClassVar, Dict, List, Optional, Set

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr, field_validator
from typing_extensions import Self


class WorkflowConcurrency(BaseModel):
    """
    WorkflowConcurrency
    """  # noqa: E501

    max_runs: StrictInt = Field(
        description="The maximum number of concurrent workflow runs.", alias="maxRuns"
    )
    limit_strategy: StrictStr = Field(
        description="The strategy to use when the concurrency limit is reached.",
        alias="limitStrategy",
    )
    get_concurrency_group: StrictStr = Field(
        description="An action which gets the concurrency group for the WorkflowRun.",
        alias="getConcurrencyGroup",
    )
    __properties: ClassVar[List[str]] = [
        "maxRuns",
        "limitStrategy",
        "getConcurrencyGroup",
    ]

    @field_validator("limit_strategy")
    def limit_strategy_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(
            ["CANCEL_IN_PROGRESS", "DROP_NEWEST", "QUEUE_NEWEST", "GROUP_ROUND_ROBIN"]
        ):
            raise ValueError(
                "must be one of enum values ('CANCEL_IN_PROGRESS', 'DROP_NEWEST', 'QUEUE_NEWEST', 'GROUP_ROUND_ROBIN')"
            )
        return value

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of WorkflowConcurrency from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of WorkflowConcurrency from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "maxRuns": obj.get("maxRuns"),
                "limitStrategy": obj.get("limitStrategy"),
                "getConcurrencyGroup": obj.get("getConcurrencyGroup"),
            }
        )
        return _obj
