import sys
from scheduler import run_daily_post


def main():
    """Main entry point for the Clarified social media manager."""
    print("Clarified Social Media Manager")
    print("=" * 40)
    run_daily_post()


if __name__ == "__main__":
    main()
