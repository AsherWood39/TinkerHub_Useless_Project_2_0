# Story generation module using Groq AI
# Takes processed images and generates creative interpretations based on detected patterns
# Uses the Groq API to create engaging, contextual stories about the shapes it sees

import base64
import os
import google.generativeai as genai
from PIL import Image
from diffusers import DiffusionPipeline
from diffusers.utils import load_image
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import requests 
import io 

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

def get_gemini_interpretation(image_path):
    """
    Takes an image path, sends it with a text prompt to the Gemini API,
    and returns the creative interpretation.
    """
    if not api_key:
        raise ValueError("Oops! Can't seem to find your GOOGLE_API_KEY. Please check your .env file.")

    # 1. Configure the Gemini client
    genai.configure(api_key=api_key)

    # 2. Define the text part of the prompt (your instructions are unchanged)
    prompt_text = """
    You are a playful and imaginative friend looking at funny doodles! These white contours on a black background are like a cosmic Rorschach test that reveals the most amusing and whimsical stories. Channel your inner child and let's have fun discovering silly shapes and telling goofy tales!

    Important Instructions (but keep it fun!):
    * **Embrace the Silly:** These aren't just lines - they could be dancing spaghetti monsters, cloud animals having a party, or robots learning to do the moonwalk! Let your imagination run wild, but stick to what you actually see.
    * **Find the Funny:** Maybe that squiggly line looks like a mustache on an invisible face? Or those zigzags remind you of a chicken doing aerobics? Tell us about it!
    * **Be a Shape Detective:** Point out the actual patterns you see, but with a playful twist - "these wobbly lines remind me of a jellyfish practicing yoga" or "these spirals look like a dizzy snail's afternoon adventure!"
    * **Connect the Dots (or Squiggles):** Build your story around the real shapes you see, but don't be afraid to give them quirky personalities and funny situations.
    * **Details = More Giggles:** Notice something peculiar like a dot that looks like a nose or curves that form a goofy grin? That's comedy gold!

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
     Oh my goodness, look at these wild contours! There's this totally bonkers shape that looks like a paper boat having an identity crisis - it thinks it's a disco dancer! Check out those crazy zigzag patterns on its sail - they remind me of a lightning bolt that got tangled up at a sock puppet party! And near the bow, I can totally see what looks like a tiny origami captain, but plot twist - they're wearing a party hat and doing the macarena while steering through the stormiest dance floor in the seven seas! 

     ~ ~ ~

     "WAIT, is that sail doing the electric boogie with those zappy patterns?"
     "OMG yes! And those wobbly curves at the bottom? It's like the boat is surfing on a wave made of jelly!"
     "I can't unsee the tiny captain now - they're definitely wearing mismatched socks on their paper feet!"
     "What if the lightning-disco-sail powers the boat's built-in karaoke machine?"
     "That's why there are all those squiggly lines behind it - it's leaving a trail of party confetti and dad jokes!"
    """
    
    # 3. Load the image using the Pillow library
    image = Image.open(image_path)

    # 4. Initialize the model and generate content
    # gemini-2.5-flash is a fast and capable multimodal model
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # The API call combines the text and image in a list
    response = model.generate_content([prompt_text, image])

    # 5. Extract and return the text from the response
    interpretations = response.text
    print("Gemini's interpretations:")
    print(interpretations)
    return interpretations


def image_to_image(story, style="color"):
    load_dotenv()
    HF_API_TOKEN = os.getenv("HF_TOKEN")
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

    if not HF_API_TOKEN:
        raise ValueError("Hugging Face API token not found. Please set HF_TOKEN in a .env file.")

    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    
    # Define different style prompts
    style_prompts = {
        "color": f"{story}, silly cartoon style, exaggerated expressions, goofy character design, playful doodle art, rainbow color palette, fun and wonky perspective, big googly eyes, rubber hose animation style, squash and stretch effect, saturday morning cartoons, children's book illustration, bouncy and energetic, kawaii inspired, cheerful atmosphere",
        "sketch": f"{story}, monochrome black and white only, no colors, grayscale art, pure black and white ink drawing, high contrast monochromatic, pen and ink illustration, stark black and white, bold ink strokes, detailed linework, woodcut style, black ink on white paper, vintage newspaper illustration style, graphic novel noir style, dramatic shadows and highlights"
    }
    
    # Select the appropriate prompt based on style
    selected_prompt = style_prompts.get(style, style_prompts["color"])
    
    payload = {"inputs": selected_prompt}

    print(f"🎨 Sending prompt to Hugging Face: '{selected_prompt}'")
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