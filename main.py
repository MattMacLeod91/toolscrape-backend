from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from reddit_scraper import RedditScraper


app = FastAPI()

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
