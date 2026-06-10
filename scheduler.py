import os
import sys
import logging
from datetime import datetime
from post_generator import generate_post
from instagram_poster import post_to_instagram

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def run_daily_post():
    """Run the daily Instagram post."""
    logger.info("Starting daily post job")
    logger.info(f"Current time: {datetime.now()}")

    api_key = os.environ.get("OPENAI_API_KEY")
    instagram_username = os.environ.get("INSTAGRAM_USERNAME")
    instagram_password = os.environ.get("INSTAGRAM_PASSWORD")

    if not api_key:
        logger.error("OPENAI_API_KEY not set")
        sys.exit(1)

    if not instagram_username or not instagram_password:
        logger.error("INSTAGRAM_USERNAME or INSTAGRAM_PASSWORD not set")
        sys.exit(1)

    try:
        logger.info("Generating post content...")
        post_data = generate_post(api_key=api_key)
        logger.info(f"Selected image: {post_data['image_path']}")
        logger.info(f"Generated caption: {post_data['caption'][:100]}...")

        logger.info("Posting to Instagram...")
        result = post_to_instagram(
            image_path=post_data["image_path"],
            caption=post_data["caption"],
            username=instagram_username,
            password=instagram_password
        )

        logger.info(f"Post successful! Media ID: {result}")
        return True

    except Exception as e:
        logger.error(f"Failed to post: {e}")
        raise

if __name__ == "__main__":
    run_daily_post()
