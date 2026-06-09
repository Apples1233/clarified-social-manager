import anthropic
import random
import os
from pathlib import Path
import base64

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

CAPTION_STYLES = [
      "hype/streetwear",
      "minimal and clean",
      "storytelling lifestyle",
      "bold and confident",
      "community-focused",
      "question-based engagement",
      "product highlight",
      "limited drop energy",
]

HASHTAG_SETS = [
      "#clarified #clarifiedhats #truckerhat #hatgang #streetwear #snapback #hatlife #fitted #headwear #streetstyle",
      "#clarified #hatcollection #drip #fashion #mensfashion #womensfashion #accessories #ootd #swag #style",
      "#clarified #boshi #embroidered #premiumhats #capsofinstagram #hatoftheday #newera #hathead #flexfit",
      "#clarified #streetwearfashion #urbanstyle #hatgame #capsule #wearitwell #boldstyle #dailylook #brandname",
]


def get_hat_images():
      hat_dir = Path("assets/hats")
      hat_dir.mkdir(parents=True, exist_ok=True)
      images = []
      supported = (".jpg", ".jpeg", ".png", ".webp")
      for img_path in hat_dir.iterdir():
                if img_path.suffix.lower() in supported:
                              with open(img_path, "rb") as f:
                                                data = base64.standard_b64encode(f.read()).decode("utf-8")
                                            ext = img_path.suffix.lower().lstrip(".")
                              media_type = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"
                              images.append({"path": str(img_path), "data": data, "media_type": media_type})
                      return images


def generate_post(style=None, hat_image_path=None):
      style = style or random.choice(CAPTION_STYLES)
      hashtags = random.choice(HASHTAG_SETS)
      images = get_hat_images()

    if not images:
              raise FileNotFoundError("No hat images found in assets/hats/. Add your product photos.")

    selected = next((img for img in images if img["path"] == hat_image_path), None)
    if selected is None:
              selected = random.choice(images)

    prompt = (
              f'You are a creative social media manager for CLARIFIED, a premium streetwear hat brand by BOSHI.\n\n'
              f'The hats feature bold embroidered CLARIFIED branding in white with a mesh trucker-style back.\n'
              f'Available in navy blue and black colorways.\n\n'
              f'Generate a single Instagram caption in the "{style}" style.\n\n'
              f'Requirements:\n'
              f'- 1-4 sentences max, punchy and on-brand\n'
              f'- No emojis unless completely natural (1-2 max)\n'
              f'- Bold, confident, street-ready brand voice\n'
              f'- Do NOT include hashtags\n'
              f'- Make it feel fresh and different each time\n\n'
              f'Return ONLY the caption text, nothing else.'
    )

    message = client.messages.create(
              model="claude-opus-4-5",
              max_tokens=300,
              messages=[
                            {
                                              "role": "user",
                                              "content": [
                                                                    {
                                                                                              "type": "image",
                                                                                              "source": {
                                                                                                                            "type": "base64",
                                                                                                                            "media_type": selected["media_type"],
                                                                                                                            "data": selected["data"],
                                                                                                },
                                                                    },
                                                                    {"type": "text", "text": prompt},
                                              ],
                            }
              ],
    )

    caption = message.content[0].text.strip()
    full_caption = caption + "\n\n" + hashtags

    return {
              "caption": full_caption,
              "image_path": selected["path"],
              "style_used": style,
    }
