#!/usr/bin/env python3
"""
CLARIFIED Hat Brand - Instagram Social Media Manager
Powered by Claude AI + instagrapi + GitHub Actions
"""

import argparse
import os
from dotenv import load_dotenv

load_dotenv()


def main():
      parser = argparse.ArgumentParser(
                description="Clarified Instagram Social Media Manager"
      )
      parser.add_argument(
          "--post-now", action="store_true", help="Generate and post immediately"
      )
      parser.add_argument(
          "--preview",
          action="store_true",
          help="Preview a generated post without posting",
      )
      parser.add_argument(
          "--schedule",
          type=str,
          default="09:00",
          help="Daily post time in HH:MM (default: 09:00)",
      )
      parser.add_argument(
          "--style", type=str, help="Caption style override (optional)"
      )
      args = parser.parse_args()

    required = ["ANTHROPIC_API_KEY", "INSTAGRAM_USERNAME", "INSTAGRAM_PASSWORD"]
    missing = [v for v in required if not os.getenv(v)]
    if missing:
              print(f"Missing environment variables: {', '.join(missing)}")
              print("Copy .env.example to .env and fill in your credentials.")
              return

    if args.preview:
              from post_generator import generate_post

        post = generate_post(style=args.style)
        print(f"\nCLARIFIED Post Preview\n{'=' * 40}")
        print(f"Style: {post['style_used']}")
        print(f"Image: {post['image_path']}")
        print(f"\nCaption:\n{post['caption']}")

elif args.post_now:
        from scheduler import run_daily_post

        run_daily_post()

else:
        from scheduler import start_scheduler

        start_scheduler(post_time=args.schedule)


if __name__ == "__main__":
      main()
