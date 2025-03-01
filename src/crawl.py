'''This file will scrape the documentations of the Cerebras API and save them as markdown files in the `scraped_data` directory.
The `crawl_sequential` function will sequentially crawl the URLs in the `urls` list and save the markdown content to a file.
We utilize crawl4ai to perform the web scraping.
Taken from: https://github.com/unclecode/crawl4ai
'''

import asyncio
import json
import os
from typing import List
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import requests
from xml.etree import ElementTree

SAVE_DIR = "scraped_data"

# Ensure save directory exists
os.makedirs(SAVE_DIR, exist_ok=True)

async def crawl_sequential(urls: List[str]):
    print("\n=== Sequential Crawling with Session Reuse ===")

    browser_config = BrowserConfig(
        headless=True,
        extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"],
    )

    crawl_config = CrawlerRunConfig(markdown_generator=DefaultMarkdownGenerator())

    crawler = AsyncWebCrawler(config=browser_config)
    await crawler.start()

    results_metadata = []
    
    try:
        session_id = "session1"
        for url in urls:
            result = await crawler.arun(url=url, config=crawl_config, session_id=session_id)
            
            if result.success:
                markdown_content = result.markdown_v2.raw_markdown
                filename = os.path.join(SAVE_DIR, f"{url.replace('https://', '').replace('/', '_')}.md")
                
                with open(filename, "w", encoding="utf-8") as md_file:
                    md_file.write(markdown_content)
                
                print(f"Saved: {filename} (Length: {len(markdown_content)})")
                results_metadata.append({"url": url, "status": "success", "filename": filename})
            else:
                print(f"Failed: {url} - Error: {result.error_message}")
                results_metadata.append({"url": url, "status": "failed", "error": result.error_message})
    finally:
        await crawler.close()
        
        # Save metadata
        with open(os.path.join(SAVE_DIR, "scraping_results.json"), "w", encoding="utf-8") as json_file:
            json.dump(results_metadata, json_file, indent=4)

def get_api_docs_urls():
    sitemap_url = "https://openweathermap.org/sitemap.xml"
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()
        
        root = ElementTree.fromstring(response.content)
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        return [loc.text for loc in root.findall('.//ns:loc', namespace)]
    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        return []

async def main():
    urls = get_api_docs_urls()
    if urls:
        print(f"Found {len(urls)} URLs to crawl")
        await crawl_sequential(urls)
    else:
        print("No URLs found to crawl")

if __name__ == "__main__":
    asyncio.run(main())
