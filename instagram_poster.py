import os
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from pathlib import Path

SESSION_FILE = "session.json"


def get_client():
      """Get authenticated Instagram client, reusing session if available."""
      cl = Client()
      cl.delay_range = [2, 5]

    if Path(SESSION_FILE).exists():
              try:
                            cl.load_settings(SESSION_FILE)
                            cl.login(os.getenv("INSTAGRAM_USERNAME"), os.getenv("INSTAGRAM_PASSWORD"))
                            cl.get_timeline_feed()
                            print("Reused existing Instagram session.")
                            return cl
except (LoginRequired, Exception):
            print("Session expired. Re-logging in...")
            Path(SESSION_FILE).unlink(missing_ok=True)

    cl.login(os.getenv("INSTAGRAM_USERNAME"), os.getenv("INSTAGRAM_PASSWORD"))
    cl.dump_settings(SESSION_FILE)
    print("Logged into Instagram successfully.")
    return cl


def post_photo(image_path, caption):
      """Post a single photo to Instagram."""
      cl = get_client()
      media = cl.photo_upload(path=image_path, caption=caption)
      print(f"Posted to Instagram! Media ID: {media.pk}")
      return {"media_id": str(media.pk), "image": image_path}
