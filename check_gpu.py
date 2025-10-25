import torch

print("="*60)
print("GPU Configuration Check")
print("="*60)
print(f"PyTorch Version: {torch.__version__}")
print(f"CUDA Available: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"CUDA Version: {torch.version.cuda}")
    print(f"GPU Device: {torch.cuda.get_device_name(0)}")
    print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    print(f"Number of GPUs: {torch.cuda.device_count()}")
    print("\n✅ GPU is ready for FinBERT acceleration!")
else:
    print("\n❌ CUDA not available - using CPU only")
    print("\nTo enable GPU support:")
    print("1. Check CUDA version: nvidia-smi")
    print("2. Uninstall current PyTorch: uv pip uninstall torch")
    print("3. Install GPU version:")
    print("   uv pip install torch --index-url https://download.pytorch.org/whl/cu121")

print("="*60)
