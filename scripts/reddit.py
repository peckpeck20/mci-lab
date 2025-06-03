import praw
import json
import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env from project root
env_path = Path(__file__).resolve().parents[1] / '.env'
load_dotenv(dotenv_path=env_path)

# Read credentials from env
client_id = os.getenv("REDDIT_CLIENT_ID")
client_secret = os.getenv("REDDIT_CLIENT_SECRET")
user_agent = os.getenv("REDDIT_USER_AGENT")

# Authenticate
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

# Fetch post
submission = reddit.submission(url='https://www.reddit.com/r/Innsbruck/comments/1kgsu2d/gott_sei_dank_war_schon_verwirrt_a_bombe_so_weit/')
submission.comments.replace_more(limit=None)

# Collect data
data = {
    "id": submission.id,
    "title": submission.title,
    "author": str(submission.author),
    "score": submission.score,
    "upvote_ratio": submission.upvote_ratio,
    "url": submission.url,
    "selftext": submission.selftext,
    "created_utc": submission.created_utc,
    "num_comments": submission.num_comments,
    "flair": submission.link_flair_text,
    "subreddit": str(submission.subreddit),
    "comments": []
}

# Add all comments
for comment in submission.comments.list():
    data["comments"].append({
        "id": comment.id,
        "author": str(comment.author),
        "body": comment.body,
        "score": comment.score,
        "created_utc": comment.created_utc,
        "parent_id": comment.parent_id
    })

# Save to datasets/ folder in project root
datasets_path = Path(__file__).resolve().parents[1] / "datasets"
output_file = datasets_path / "reddit_dataset.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

