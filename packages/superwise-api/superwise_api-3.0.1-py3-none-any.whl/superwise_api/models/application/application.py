from datetime import datetime
from enum import Enum
from typing import Optional
from typing import Sequence
from typing import Union

from pydantic import Field
from pydantic import HttpUrl
from pydantic import UUID4

from superwise_api.models import SuperwiseEntity
from superwise_api.models.tool.tool import ToolDef


class ModelProvider(str, Enum):
    OPENAI = "OpenAI"
    GOOGLE = "GoogleAI"
    VERTEX_AI_MODEL_GARDEN = "VertexAIModelGarden"


class OpenAIModelVersion(str, Enum):
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_3_5_TURBO_1106 = "gpt-3.5-turbo-1106"
    GPT_4 = "gpt-4"
    GPT_4_1106_PREVIEW = "gpt-4-1106-preview"
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_4_TURBO_PREVIEW = "gpt-4-turbo-preview"
    GPT_4O = "gpt-4o"


class GoogleModelVersion(str, Enum):
    GEMINI_1_5 = "models/gemini-1.5-pro"
    GEMINI_PRO = "gemini-pro"
    TEXT_BISON_001 = "models/text-bison-001"


class VertexAIModelGardenVersion(str, Enum):
    PLACEHOLDER = "placeholder"


class ApplicationStatus(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"
    DEGRADED = "degraded"


class ModelLLM(SuperwiseEntity):
    provider: ModelProvider
    version: Union[OpenAIModelVersion, GoogleModelVersion, VertexAIModelGardenVersion]
    api_token: str

    @classmethod
    def from_dict(cls, obj: dict):
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ModelLLM.parse_obj(obj)

        _obj = ModelLLM.parse_obj(
            {"provider": obj.get("provider"), "version": obj.get("version"), "api_token": obj.get("api_token")}
        )
        return _obj


class Application(SuperwiseEntity):
    id: UUID4
    created_by: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    name: str
    llm_model: Optional[ModelLLM] = Field(None, alias="model")
    prompt: Optional[str]
    dataset_id: str
    tools: Sequence[ToolDef]
    url: HttpUrl
    show_cites: bool = Field(default=False)
    status: ApplicationStatus = ApplicationStatus.UNKNOWN

    @classmethod
    def from_dict(cls, obj: dict):
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Application.parse_obj(obj)

        _obj = Application.parse_obj(
            {
                "id": obj.get("id"),
                "created_by": obj.get("created_by"),
                "created_at": obj.get("created_at"),
                "updated_at": obj.get("updated_at"),
                "name": obj.get("name"),
                "model": ModelLLM.from_dict(obj.get("model")) if obj.get("model") is not None else None,
                "prompt": obj.get("prompt"),
                "dataset_id": obj.get("dataset_id"),
                "tools": [ToolDef.parse_obj(tool) for tool in obj.get("tools")],
                "url": obj.get("url"),
                "show_cites": obj.get("show_cites"),
                "status": obj.get("status"),
            }
        )
        return _obj
