import os
from instagrapi import Client
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

SESSION_FILE = "session.json"


def post_to_instagram(image_path: str, caption: str, username: str, password: str) -> str:
    """Post an image to Instagram."""
    cl = Client()
    cl.delay_range = [2, 5]
    
    session_path = Path(SESSION_FILE)
    
    if session_path.exists():
        try:
            cl.load_settings(SESSION_FILE)
            cl.login(username, password)
            logger.info("Logged in using saved session")
        except Exception:
            logger.info("Session expired, logging in fresh")
            session_path.unlink(missing_ok=True)
            cl.login(username, password)
            cl.dump_settings(SESSION_FILE)
    else:
        cl.login(username, password)
        cl.dump_settings(SESSION_FILE)
        logger.info("Logged in and saved session")
    
    image_path_obj = Path(image_path)
    if not image_path_obj.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    media = cl.photo_upload(str(image_path_obj), caption)
    logger.info(f"Posted successfully! Media ID: {media.pk}")
    return str(media.pk)
