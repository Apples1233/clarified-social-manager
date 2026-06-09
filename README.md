# Clarified Hat Brand - Instagram Social Media Manager

AI-powered daily Instagram posting for the **CLARIFIED** hat brand by BOSHI.
Built with Claude AI (Anthropic) + instagrapi + GitHub Actions.

## Features

- Posts daily to Instagram automatically
- Claude AI generates a unique caption every time using your actual hat photos
- 8 different caption style rotations (hype, minimal, storytelling, bold, etc.)
- 4 rotating hashtag sets for maximum reach
- Session caching so you stay logged into Instagram
- Full post log stored in post_log.json
- GitHub Actions for zero-maintenance daily automation

## Setup

### 1. Clone and install

```bash
git clone https://github.com/Apples1233/clarified-social-manager
cd clarified-social-manager
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Add credentials

```bash
cp .env.example .env
```

Edit `.env` and add your keys:
- `ANTHROPIC_API_KEY` from console.anthropic.com
- `INSTAGRAM_USERNAME` your Instagram login
- `INSTAGRAM_PASSWORD` your Instagram password

### 3. Add your hat photos

Drop your product images into `assets/hats/` folder (JPG or PNG).

### 4. Preview a post (no posting)

```bash
python main.py --preview
```

### 5. Post immediately

```bash
python main.py --post-now
```

### 6. Run daily scheduler at 9am

```bash
python main.py --schedule 09:00
```

## GitHub Actions (Automated daily posting)

Add these secrets in your repo Settings > Secrets > Actions:
- `ANTHROPIC_API_KEY`
- `INSTAGRAM_USERNAME`
- `INSTAGRAM_PASSWORD`

The workflow runs automatically every day at 9am EST.
You can also trigger it manually from the Actions tab.

## Project Structure

```
clarified-social-manager/
├── .env.example          # Environment variable template
├── .gitignore
├── README.md
├── requirements.txt
├── main.py               # Entry point - CLI interface
├── scheduler.py          # Daily posting scheduler
├── post_generator.py     # Claude AI caption generation
├── instagram_poster.py   # Instagram API posting
└── assets/
    └── hats/             # Drop your product photos here
    ```
