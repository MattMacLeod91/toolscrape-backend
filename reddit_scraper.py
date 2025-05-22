import praw
from datetime import datetime

class RedditScraper:
    def __init__(self, config):
        creds = config["praw_credentials"]
        self.reddit = praw.Reddit(
            client_id=creds["client_id"],
            client_secret=creds["client_secret"],
            user_agent=creds["user_agent"]
        )
        self.config = config
        self.results = []

    def fetch_data(self):
        for source in self.config["sources"]:
            if source["type"] == "subreddit":
                self._fetch_subreddit(source)
        return self.results

    def _fetch_subreddit(self, source):
        name = source["name"]
        search_keywords = source.get("search_keywords", [])
        submissions = self.reddit.subreddit(name).search(" OR ".join(search_keywords), limit=10) if search_keywords else self.reddit.subreddit(name).top(limit=10)

        batch = {
            "platform": "Reddit",
            "source_name": f"/r/{name}",
            "signal_batch": []
        }

        for submission in submissions:
            batch["signal_batch"].append({
                "thread_id": submission.id,
                "thread_title": submission.title,
                "text": submission.selftext,
                "url": submission.url,
                "upvotes": submission.score,
                "num_comments_reported": submission.num_comments,
                "timestamp": datetime.utcfromtimestamp(submission.created_utc).isoformat(),
                "comments": []
            })

        self.results.append(batch)
