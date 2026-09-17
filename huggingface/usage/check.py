import torch

print(torch.cuda.is_available())
# MAC
# print(torch.backends.mps.is_available())
print(torch.__version__)