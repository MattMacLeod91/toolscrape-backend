from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from reddit_scraper import RedditScraper
from fastapi.middleware.cors import CORSMiddleware
import traceback

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Optional: restrict to Lovable origin later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScrapeRequest(BaseModel):
    config: dict

@app.post("/scrape")
def scrape(request: ScrapeRequest):
    try:
        scraper = RedditScraper(request.config)
        data = scraper.fetch_data()
        return {"status": "success", "data": data}
    except Exception as e:
        print("❌ Exception during scrape:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
