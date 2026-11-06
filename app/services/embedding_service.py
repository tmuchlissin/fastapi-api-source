import asyncio, logging, torch
from app.config.core import settings
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class EmbeddingService:
    def __init__(self) -> None:
        self.models: dict[str, SentenceTransformer] = {}
        self.default_device: str = "cpu"

    def _get_or_load_model(self, target_device: str) -> SentenceTransformer:
        if target_device == "cuda" and not torch.cuda.is_available():
            target_device = "cpu"

        if target_device in self.models:
            return self.models[target_device]

        model_path = settings.resolved_model_path
        if not (model_path / "config.json").exists():
            raise FileNotFoundError(
                f"Model not found at {model_path}. "
                "Run `uv run python -m app.scripts.download_model` first."
            )

        logger.info(f"Loading model from {model_path} onto device: {target_device}...")
        model = SentenceTransformer(
            str(model_path),
            device=target_device,
            local_files_only=True,
        )

        if target_device == "cuda":
            model.half()

        model.encode(["warmup"], show_progress_bar=False)
        self.models[target_device] = model
        logger.info(f"Embedding model loaded and warmed up on {target_device}.")
        return model

    def load_model(self) -> None:
        self.default_device = (
            "cuda"
            if settings.EMBEDDING_DEVICE == "cuda" and torch.cuda.is_available()
            else "cpu"
        )
        self._get_or_load_model(self.default_device)

    def unload_model(self) -> None:
        self.models.clear()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    def _encode_sync(
        self,
        texts: list[str],
        normalize: bool,
        device: str | None = None,
    ) -> tuple[list[list[float]], str]:
        target_device = device or self.default_device
        if target_device == "cuda" and not torch.cuda.is_available():
            target_device = "cpu"

        model = self._get_or_load_model(target_device)
        vectors = model.encode(
            texts,
            batch_size=32,
            normalize_embeddings=normalize,
            show_progress_bar=False,
        )
        if target_device == "cuda":
            torch.cuda.synchronize()
        return vectors.tolist(), target_device

    async def embed(
        self,
        texts: list[str],
        normalize: bool = True,
        device: str | None = None,
    ) -> tuple[list[list[float]], str]:
        return await asyncio.to_thread(self._encode_sync, texts, normalize, device)



embedding_service = EmbeddingService()

