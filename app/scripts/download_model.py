from app.config.core import settings
from huggingface_hub import snapshot_download


def download_embedding_model() -> None:
    target_dir = settings.resolved_model_path
    target_dir.mkdir(parents=True, exist_ok=True)

    print(f"Downloading '{settings.EMBEDDING_MODEL_ID}' to '{target_dir}'...")
    snapshot_download(
        repo_id=settings.EMBEDDING_MODEL_ID,
        local_dir=str(target_dir),
        local_dir_use_symlinks=False,
        ignore_patterns=["*.msgpack", "*.h5", "*.ot"],
    )
    print(f"Model successfully saved to {target_dir}")


if __name__ == "__main__":
    download_embedding_model()

