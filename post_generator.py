import openai
import base64
import os
import random
from pathlib import Path


def encode_image(image_path: str) -> str:
    """Encode image to base64 string for OpenAI API."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def get_image_media_type(image_path: str) -> str:
    """Get the media type based on file extension."""
    ext = Path(image_path).suffix.lower()
    media_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp"
    }
    return media_types.get(ext, "image/jpeg")


def get_hat_name(image_path: str) -> str:
    """Extract a human-readable hat name from the filename."""
    stem = Path(image_path).stem  # e.g. "clarified_navy_hat"
    parts = stem.replace("clarified_", "").replace("_hat", "").replace("_", " ")
    return parts.strip().title()  # e.g. "Navy"


def get_hat_images(assets_dir: str = "assets/hats") -> list:
    """Get all hat images from the assets directory."""
    assets_path = Path(assets_dir)
    if not assets_path.exists():
        raise FileNotFoundError(f"Assets directory not found: {assets_dir}")

    extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    images = []
    for f in assets_path.iterdir():
        if f.suffix.lower() in extensions and f.name != ".gitkeep":
            images.append(str(f))

    if not images:
        raise ValueError(f"No images found in {assets_dir}")

    return images


def generate_caption(image_path: str, api_key: str) -> str:
    """Generate an Instagram caption using ChatGPT (GPT-4o) with vision."""
    client = openai.OpenAI(api_key=api_key)

    hat_name = get_hat_name(image_path)
    image_data = encode_image(image_path)
    media_type = get_image_media_type(image_path)

    styles = [
        "hype and energetic with lots of emojis",
        "clean and minimal, very short and punchy",
        "storytelling and lifestyle-focused",
        "question-based to drive engagement",
        "bold statement style with attitude"
    ]
    style = random.choice(styles)

    prompt = f"""You are a social media expert for Clarified, a streetwear hat brand by BOSHI.

This is a product photo of the Clarified {hat_name} hat. Create an Instagram caption in a {style} style.

Requirements:
- Keep it under 150 words
- Include 5-10 relevant hashtags at the end
- Make it feel authentic and on-brand for streetwear
- Mention the specific colourway: {hat_name}
- Focus on the hat's quality, style, and the Clarified brand identity
- Hashtags should include: #Clarified #BOSHI and relevant streetwear/hat tags

Write only the caption text and hashtags, nothing else."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{media_type};base64,{image_data}"
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ],
        max_tokens=300
    )

    caption = response.choices[0].message.content.strip()
    hashtags = "#Clarified #BOSHI #streetwear #hats #trucker"

    if "#" not in caption:
        full_caption = caption + "\n\n" + hashtags
    else:
        full_caption = caption

    return full_caption


def select_random_hat(assets_dir: str = "assets/hats") -> str:
    """Select a random hat image."""
    images = get_hat_images(assets_dir)
    return random.choice(images)


def generate_post(assets_dir: str = "assets/hats", api_key: str = None) -> dict:
    """Generate a complete post with image and caption."""
    if api_key is None:
        api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("No API key provided. Set OPENAI_API_KEY environment variable.")

    image_path = select_random_hat(assets_dir)
    caption = generate_caption(image_path, api_key)

    return {
        "image_path": image_path,
        "caption": caption
    }
