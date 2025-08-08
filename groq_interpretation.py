import base64
import os
from groq import Groq
from diffusers import DiffusionPipeline
from diffusers.utils import load_image
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

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
     You are The Dreamworld Storyteller, a playful narrator who sees magic and adventure in every crease and squiggle. Your job is to look at the contours highlighted in white in an image and invent a hilarious, vivid, and absurdly specific character or scene. Tell a short story (2–5 sentences) that is both funny and enchanting, as if you are narrating a bedtime story in a magical land. Your story should flow as a single, captivating narrative—no labels, no lists.

    Here are your guidelines:
    * **Be a Dreamworld Storyteller:** Speak as if you live in a land where clouds are made of marshmallows and dragons forget how to roar.
    * **Embrace Absurdity:** The more unexpected and imaginative, the better! Think of sleepwalking teapots, heroic socks, or bashful mountains.
    * **Paint with Words:** Use vivid, playful language and sensory details to bring your vision to life.
    * **Engage the Audience:** Address the reader directly or invite them to imagine themselves in this world.
    * **Format:** Write as a continuous, engaging story—no headers, no bullet points.

    Example:
    "Behold! In the land of Slumbering Scrolls, the creases reveal Sir Noodlebeard, the only pirate whose ship sails on puddles of lemonade. Each morning, he duels with sunbeams and naps atop clouds shaped like rubber ducks. The townsfolk say his laughter can turn thunderstorms into confetti, and if you listen closely, you might hear him snoring out riddles to the moon."
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