# Story generation module using Groq AI
# Takes processed images and generates creative interpretations based on detected patterns
# Uses the Groq API to create engaging, contextual stories about the shapes it sees

import base64
import os
from PIL import Image
from groq import Groq
from diffusers import DiffusionPipeline
from diffusers.utils import load_image
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import requests 
import io 

load_dotenv()
api_key = os.getenv('GROQ_API_KEY')

def get_groq_interpretation(image_path):
    if not api_key:
        raise ValueError("Uh, Oh! Something amiss. I seem to not be able to find your GROQ_API_KEY.")

    client = Groq(api_key=api_key)

    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    prompt_content = [
    {"type": "text", 
     "text": """
     You are an artistic interpreter looking at an image showing white contours on a black background. These lines and patterns could tell countless stories. Your task is to carefully observe the actual shapes, lines, and patterns in the image, and create a story based on what you genuinely see.

     Important Instructions:
     * **Stay True to the Image:** Look closely at the contours and outlines. What do these specific lines and shapes remind you of? What patterns or figures can you actually see formed by these lines?
     * **Describe What You See:** Start by identifying concrete shapes or patterns - "these angular lines here look like...", "this curve reminds me of...", "these intersecting lines form..."
     * **Then Build Your Story:** Create your tale around these actual observed shapes, not random imagined elements.
     * **Keep it Connected:** Make sure every major story element connects back to a visible pattern or shape in the image.
     * **Be Specific:** Point out particular details that caught your eye - unusual angles, interesting intersections, or distinctive curves.

     Remember: Your story should feel like someone exploring an abstract drawing and finding recognizable shapes within it, not like random cloud-watching. Every element should be traceable back to the actual contours you see.

     Share your response in this flowing style:

     📖 The Story
     [Your main story here, written as a flowing paragraph with vivid details]

     ~ ~ ~

     And then, as two friends lying on the grass might chat, a conversation unfolds...

     "Hey, did you notice how [an interesting detail from the story]?"
     "Oh! Speaking of that, I wonder [a curious question]..."
     "Actually, you'll never believe this, but [a surprising revelation]!"
     "What if [an imaginative scenario building on that]?"
     "That reminds me... [a delightful conclusion with a twist]"

     ~ ~ ~

     ✨ A Little Secret
     [A whimsical "did you know?" moment about your character's world]

     Example:

     📖 The Story
     Looking at these contours, I'm drawn to this striking angular shape that looks just like a paper boat, but with unusual zigzag patterns along its sail. These jagged lines remind me of a lightning bolt, making this no ordinary vessel! Near the bow, I can spot what appears to be a small figure formed by intersecting curves - perhaps a brave origami captain steering through stormy seas.

     ~ ~ ~

     "See how those sharp angles in the sail create that electric pattern?"
     "Yes! And did you notice how the curves at the bottom make it look like it's riding a giant wave?"
     "The way those lines intersect at the bow actually forms what looks like a tiny paper captain!"
     "What if the lightning pattern on the sail helps it travel through paper storms?"
     "That explains the peculiar ripple pattern I see trailing behind it - it's leaving a wake of static electricity!"

     ~ ~ ~

     ✨ A Little Secret
     If you look very carefully at where the sail meets the hull, you can see tiny creases that look like morse code - perhaps secret messages from other paper sailors who've ventured these waters before!
     """},
        {"type": "image_url", 
         "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
    ]

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt_content}],
        model="meta-llama/llama-4-scout-17b-16e-instruct" 
    )

    interpretations = chat_completion.choices[0].message.content
    print("Groq's interpretations:")
    print(interpretations)
    return interpretations

def image_to_image(image_path, story):
    load_dotenv()
    HF_API_TOKEN = os.getenv("HF_TOKEN")
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

    if not HF_API_TOKEN:
        raise ValueError("Hugging Face API token not found. Please set HF_TOKEN in a .env file.")

    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    payload = {"inputs": story}

    print(f"🎨 Sending prompt to Hugging Face: '{story}'")
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        # Handle the binary image data from Hugging Face API
        image_data = response.content
        image = Image.open(io.BytesIO(image_data))
        output_filename = "generated_image.png"
        image.save(output_filename)
        print(f"✅ Image saved successfully as '{output_filename}'")
        return output_filename
    else:
        print(f"❌ Hugging Face API Error: {response.status_code}")
        print(response.json())
        return None