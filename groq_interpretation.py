import base64
import os
from groq import Groq
from diffusers import DiffusionPipeline
from diffusers.utils import load_image
from huggingface_hub import InferenceClient

def get_groq_interpretation(image_path):
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in Colab Secrets.")

    client = Groq(api_key=api_key)

    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    prompt_content = [
        {"type": "text", 
         "text": """
         You are the "Shakesperean Imaginator" 
         Your job is to look at the contours highlighted in white in an image and find a ridiculous, hilarious, or absurdly specific pattern within the chaos. 
         You must then invent a short, comedic backstory for this pattern. Do not follow a rigid "Label" and "Story" format. Instead, combine them into a single, cohesive, and funny narrative.
        Here are your guidelines:

        * **Be a Comedic Narrator:** Speak as if you're telling a grand, over-the-top story.
        * **Absurdity is Key:** Find the funniest, most unexpected thing the lines could possibly represent. Think of mythical creatures, confused animals, or bizarre everyday objects.
        * **Weave the Story:** Invent a short, detailed, and completely ridiculous backstory for your interpretation. The story should be 2-5 sentences long and feel like a mix of a whimsical children's book and stand-up comedy.
        * **Be Specific:** Instead of "a dragon," say "a sleep-deprived dragon." Instead of "a wizard," say "a banana wizard."
        * **The Goal:** Your entire response should be one continuous, imaginative interpretation that fully embodies your persona as the oracle.

        Example of the kind of output I'm looking for:

        "Ah, the creases speak! I see it now: it's 'The Doom of Petasaurus conquering the skies'! 
        Legend says this beast roams the skies looking for its next prey. 
        His tiny, ineffective wings flap a thousand times a second, creating a sound suspiciously similar to a cheap desk fan. 
        The villages below are safe only because he's so distractible, often forgetting what he's hunting mid-flight and instead stopping to admire his own reflection in a puddle."
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