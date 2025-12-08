import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

# TARGET: The Official RSS Feed (XML)
# This bypasses the HTML scraping issues entirely.
RSS_URL = "https://weworkremotely.com/categories/remote-programming-jobs.rss"

def get_rss_feed(url):
    """
    Fetches the RSS feed and parses it as XML.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # NOTE: We use 'xml' parser here because RSS is XML.
        # This fixes the "XMLParsedAsHTMLWarning" you were seeing.
        return BeautifulSoup(response.content, "xml")
    except Exception as e:
        print(f"❌ Error fetching RSS feed: {e}")
        return None

def main():
    print(f"🚀 Starting Scraper for: {RSS_URL}")
    soup = get_rss_feed(RSS_URL)
    
    if not soup:
        print("❌ Failed to retrieve RSS feed.")
        return

    # In RSS, every job is inside an <item> tag
    job_items = soup.find_all("item")
    
    print(f"   -> Found {len(job_items)} jobs in the feed.")

    all_jobs = []
    
    for job in job_items:
        try:
            # RSS fields are standard: <title>, <link>, <description>, <pubDate>
            title_text = job.title.text if job.title else "N/A"
            link = job.link.text if job.link else "N/A"
            pub_date = job.pubDate.text if job.pubDate else "N/A"
            
            # The 'description' tag in WWR's RSS feed contains the FULL HTML description!
            # This is huge - we don't need to visit the page separately.
            description_html = job.description.text if job.description else ""
            
            # Clean up the description (remove HTML tags for cleaner text analysis later)
            # We create a temporary soup just to strip HTML tags
            desc_soup = BeautifulSoup(description_html, "html.parser")
            clean_description = desc_soup.get_text(separator=" ", strip=True)
            
            # Extract Company Name (Usually "Company: Title" in WWR RSS)
            if ":" in title_text:
                company, title = title_text.split(":", 1)
                company = company.strip()
                title = title.strip()
            else:
                company = "N/A"
                title = title_text

            print(f"   --> Found: {title} at {company}")
            
            all_jobs.append({
                "title": title,
                "company": company,
                "url": link,
                "published_date": pub_date,
                "description": clean_description,
                "scraped_date": datetime.now().strftime("%Y-%m-%d")
            })
            
        except Exception as e:
            print(f"⚠️ Error parsing RSS item: {e}")
            continue

    # Save to CSV
    if all_jobs:
        df = pd.DataFrame(all_jobs)
        output_path = "data/raw/jobs_raw.csv"
        df.to_csv(output_path, index=False)
        print(f"\n✅ SUCCESS! Scraped {len(all_jobs)} jobs. Saved to {output_path}")
    else:
        print("\n❌ No jobs extracted.")

if __name__ == "__main__":
    main()