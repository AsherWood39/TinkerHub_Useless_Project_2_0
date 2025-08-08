import os

from huggingface_hub import InferenceClient
from groq_interpretation import get_groq_interpretation
from image_cleaning import detect_creases

def image_to_image(image, prompt):
  api_key = os.getenv("HF_TOKEN")

  client = InferenceClient(
      provider="fal-ai",
      api_key=api_key,
    )

  with open(image, "rb") as image_file:
    input_image = image_file.read()

  image = client.image_to_image(
      input_image,
      prompt=prompt,
      model="black-forest-labs/FLUX.1-Kontext-dev",
  )

  image.save("image.png")
  print("Image generated and saved successfully.")
  return "image.png"