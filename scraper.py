import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_movies():
    base_url = 'https://ssr1.scrape.center/page/{}'
    movies = []

    for page in range(1, 11):
        url = base_url.format(page)
        print(f"Scraping {url}...")
        try:
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Failed to retrieve page {page}")
                continue
            
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.find_all(class_='el-card__body')
            
            for item in items:
                # Title
                title_tag = item.find('h2', class_='m-b-sm')
                title = title_tag.get_text(strip=True) if title_tag else 'N/A'
                
                # Categories
                categories_div = item.find(class_='categories')
                categories = []
                if categories_div:
                    buttons = categories_div.find_all('button')
                    for btn in buttons:
                        categories.append(btn.get_text(strip=True))
                category_str = ', '.join(categories)
                
                # Info (Region, Duration, Date)
                info_divs = item.find_all(class_='info')
                region = 'N/A'
                duration = 'N/A'
                release_date = 'N/A'
                
                if len(info_divs) > 0:
                    # First info div: Region / Duration
                    text_content = info_divs[0].get_text(strip=True)
                    # Usually "Region / Duration" e.g. "中国内地、中国香港 / 171 分钟"
                    parts = text_content.split('/')
                    if len(parts) >= 1:
                        region = parts[0].strip()
                    if len(parts) >= 2:
                        duration = parts[1].strip()
                
                if len(info_divs) > 1:
                    # Second info div: Release Date
                    release_date = info_divs[1].get_text(strip=True)
                
                # Score
                score_tag = item.find(class_='score')
                score = score_tag.get_text(strip=True) if score_tag else 'N/A'
                
                # Cover
                img_tag = item.find('img', class_='cover')
                cover_url = img_tag['src'] if img_tag else 'N/A'
                
                movies.append({
                    'Title': title,
                    'Categories': category_str,
                    'Region': region,
                    'Duration': duration,
                    'Release Date': release_date,
                    'Score': score,
                    'Cover URL': cover_url
                })
                
        except Exception as e:
            print(f"Error scraping page {page}: {e}")
        
        # Be polite
        time.sleep(1)

    df = pd.DataFrame(movies)
    df.to_csv('movie.csv', index=False, encoding='utf-8-sig')
    print(f"Scraping complete. Saved {len(movies)} movies to movie.csv")

if __name__ == "__main__":
    scrape_movies()
