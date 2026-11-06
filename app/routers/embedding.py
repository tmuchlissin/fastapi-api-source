import time
from app.config.core import settings
from app.schemas.embedding import EmbeddingData, EmbeddingRequest, EmbeddingResponse
from app.services.embedding_service import embedding_service
from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from secrets import compare_digest

router = APIRouter(prefix="/v1", tags=["Embeddings"])
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def verify_api_key(api_key: str | None = Security(api_key_header)) -> str:
    if not api_key or not compare_digest(api_key, settings.API_KEY):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-API-Key header",
        )
    return api_key


@router.post("/embeddings", response_model=EmbeddingResponse)
async def create_embeddings(
    payload: EmbeddingRequest,
    _: str = Depends(verify_api_key),
) -> EmbeddingResponse:
    texts = [payload.input] if isinstance(payload.input, str) else payload.input
    if not texts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Input cannot be empty",
        )

    start_time = time.perf_counter()
    vectors, used_device = await embedding_service.embed(
        texts,
        normalize=payload.normalize,
        device=payload.device,
    )
    duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

    data = [
        EmbeddingData(embedding=vec, index=idx)
        for idx, vec in enumerate(vectors)
    ]

    return EmbeddingResponse(
        data=data,
        model=payload.model,
        device=used_device,
        dimension=len(vectors[0]) if vectors else 0,
        duration_ms=duration_ms,
    )


