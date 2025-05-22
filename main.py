from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from reddit_scraper import RedditScraper
from fastapi.middleware.cors import CORSMiddleware
import traceback  # ← Add this at the top

@app.post("/scrape")
def scrape(request: ScrapeRequest):
    try:
        scraper = RedditScraper(request.config)
        data = scraper.fetch_data()
        return {"status": "success", "data": data}
    except Exception as e:
        print("❌ Exception during scrape:")
        traceback.print_exc()  # <-- prints full stack trace to logs
        raise HTTPException(status_code=500, detail=str(e))

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to Lovable's origin
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
        raise HTTPException(status_code=500, detail=str(e))
