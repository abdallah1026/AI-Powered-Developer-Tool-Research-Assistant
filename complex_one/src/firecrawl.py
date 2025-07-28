import os
from dotenv import load_dotenv
from firecrawl import FirecrawlApp, ScrapeOptions

load_dotenv()


class FirecrawlService:
    def __init__(self):
        api_key = os.environ.get('FIRECRAWL_API_KEY')
        if not api_key:
            raise Exception("Missing FIRECRAWL_API_KEY")
        self.app = FirecrawlApp(api_key=api_key)

    def search_company(self, query: str, num_results: int = 5):
        try:
            result = self.app.search(
                query=f"{query} company pricing",
                limit=num_results,
                scrape_options=ScrapeOptions(
                    output_format=["markdown"]
                )
            )
            return result

        except Exception as e:
            print(e)
            return []

    def scrap_company_pages(self, url: str):
        try:
            result = self.app.scrape_url(
                url,
                output_format=["markdown"]
            )
        except Exception as e:
            print(e)
            return None
