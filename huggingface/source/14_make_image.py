# uv pip install diffusers transformers accelerate torch
# pip uninstall -y diffusers transformers huggingface-hub
# uv pip install –no-cache-dir -U huggingface-hub transformers diffusers
# uv

from diffusers import StableDiffusionPipeline
import torch

model_id = "sd-legacy/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    dtype=torch.float32,
    safety_checker=None
)
pipe = pipe.to("cuda")

prompt = "a photo of an astronaut riding a horse on mars"
image = pipe(prompt).images[0]

image.save("astronaut_rides_horse.png")
