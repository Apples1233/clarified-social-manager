import schedule
import time
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from post_generator import generate_post
from instagram_poster import post_photo

load_dotenv()

LOG_FILE = "post_log.json"


def load_log():
      if os.path.exists(LOG_FILE):
                with open(LOG_FILE) as f:
                              return json.load(f)
                      return []


def save_log(log):
      with open(LOG_FILE, "w") as f:
                json.dump(log, f, indent=2)


def run_daily_post():
      """Generate and post one Instagram post."""
      print(f"\nRunning daily post at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
      try:
                post = generate_post()
                print(f"\nCaption preview:\n{post['caption']}\n")
                print(f"Image: {post['image_path']}")

          result = post_photo(post["image_path"], post["caption"])

        log = load_log()
        log.append({
                      "timestamp": datetime.now().isoformat(),
                      "media_id": result["media_id"],
                      "image": post["image_path"],
                      "style": post["style_used"],
                      "caption": post["caption"],
        })
        save_log(log)
        print("Post logged successfully.")

except Exception as e:
        print(f"Error during post: {e}")


def start_scheduler(post_time="09:00"):
      """Start the daily scheduler."""
    print(f"Scheduler started. Daily post scheduled at {post_time}.")
    schedule.every().day.at(post_time).do(run_daily_post)

    while True:
              schedule.run_pending()
              time.sleep(60)
