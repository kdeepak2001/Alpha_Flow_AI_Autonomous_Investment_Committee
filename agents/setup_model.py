import os
from huggingface_hub import snapshot_download

# Define the folder where we want the model
local_model_path = os.path.join(os.getcwd(), "my_local_model")

print(f"⬇️ Starting manual download to: {local_model_path}")
print("   (This helps avoid Windows permission/symlink errors)")

try:
    # Force download of the actual files (no shortcuts/symlinks)
    snapshot_download(
        repo_id="sentence-transformers/all-MiniLM-L6-v2",
        local_dir=local_model_path,
        local_dir_use_symlinks=False,  # <--- THIS IS THE FIX
        resume_download=True
    )
    print("\n✅ Success! Model is saved safely on your disk.")
except Exception as e:
    print(f"\n❌ Download failed: {e}")