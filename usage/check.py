# uv pip install transformers
# uv pip install torch --index-url https://download.pytorch.org/whl/cu126

import torch

print(torch.cuda.is_available())

print(torch.__version__)