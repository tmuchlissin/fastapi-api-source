from pydantic import BaseModel, Field
from typing import Literal


class EmbeddingRequest(BaseModel):
    input: str | list[str] = Field(
        ...,
        description="Single text or batch of texts to embed.",
    )
    model: str = Field(default="bge-m3", description="Embedding model name.")
    normalize: bool = Field(default=True, description="Whether to L2-normalize vectors.")
    device: Literal["cuda", "cpu"] | None = Field(
        default=None,
        description="Optional device override ('cuda' or 'cpu').",
    )


class EmbeddingData(BaseModel):
    object: str = "embedding"
    embedding: list[float]
    index: int


class EmbeddingResponse(BaseModel):
    object: str = "list"
    data: list[EmbeddingData]
    model: str
    device: str
    dimension: int
    duration_ms: float



