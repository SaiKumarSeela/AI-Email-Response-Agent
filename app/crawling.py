
import asyncio

from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://aws.amazon.com/ec2/autoscaling/faqs/",
        )
        print(result.markdown)  # Show the first 300 characters of extracted text

if __name__ == "__main__":
    asyncio.run(main())

# from crawl4ai import AsyncWebCrawler
# from crawl4ai.chunking_strategy import RegexChunking
# async def main():
#     async with AsyncWebCrawler(verbose=True) as crawler:
#         result = await crawler.arun(url="https://en.wikipedia.org/wiki/3_Idiots", bypass_cache=False) 
#         print(f"Extracted content: {result.markdown}")


# if __name__ == "__main__":
#     asyncio.run(main())


from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-85be9a11d01d4885a7b39c2f26f47826")

# Scrape a website:
scrape_status = app.scrape_url(
  'https://aws.amazon.com/ec2/autoscaling/faqs/', 
  params={'formats': ['markdown', 'html']}
)
print(scrape_status["markdown"])

# # Crawl a website:
# crawl_status = app.crawl_url(
#   'https://firecrawl.dev', 
#   params={
#     'limit': 1, 
#     'scrapeOptions': {'formats': ['markdown', 'html']}
#   }
# )
# print(crawl_status)