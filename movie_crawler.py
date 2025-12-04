"""
電影爬蟲程式 - Movie Crawler
功能：依序爬取 https://ssr1.scrape.center/ 共 10 頁的電影資訊，並儲存為 movie.csv
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from typing import List, Dict

class MovieCrawler:
    """電影爬蟲類別"""
    
    def __init__(self, base_url: str = 'https://ssr1.scrape.center/page/{}'):
        self.base_url = base_url
        self.movies = []
    
    def fetch_page(self, page_num: int) -> BeautifulSoup:
        """
        獲取指定頁面的 HTML 內容
        
        Args:
            page_num: 頁碼
            
        Returns:
            BeautifulSoup 物件
        """
        url = self.base_url.format(page_num)
        print(f"正在爬取第 {page_num} 頁: {url}")
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"爬取第 {page_num} 頁失敗: {e}")
            return None
    
    def parse_movie_info(self, item) -> Dict:
        """
        解析單個電影的資訊
        
        Args:
            item: BeautifulSoup 元素
            
        Returns:
            包含電影資訊的字典
        """
        # 電影標題
        title_tag = item.find('h2', class_='m-b-sm')
        title = title_tag.get_text(strip=True) if title_tag else 'N/A'
        
        # 電影類別
        categories_div = item.find(class_='categories')
        categories = []
        if categories_div:
            buttons = categories_div.find_all('button')
            for btn in buttons:
                categories.append(btn.get_text(strip=True))
        category_str = ', '.join(categories) if categories else 'N/A'
        
        # 電影資訊 (地區、時長、上映日期)
        info_divs = item.find_all(class_='info')
        region = 'N/A'
        duration = 'N/A'
        release_date = 'N/A'
        
        if len(info_divs) > 0:
            # 第一個 info div: 地區 / 時長
            text_content = info_divs[0].get_text(strip=True)
            parts = text_content.split('/')
            if len(parts) >= 1:
                region = parts[0].strip()
            if len(parts) >= 2:
                duration = parts[1].strip()
        
        if len(info_divs) > 1:
            # 第二個 info div: 上映日期
            release_date = info_divs[1].get_text(strip=True)
        
        # 評分
        score_tag = item.find(class_='score')
        score = score_tag.get_text(strip=True) if score_tag else 'N/A'
        
        # 封面圖片
        img_tag = item.find('img', class_='cover')
        cover_url = img_tag['src'] if img_tag and img_tag.get('src') else 'N/A'
        
        # 電影詳情連結
        link_tag = item.find('a', href=True)
        detail_url = f"https://ssr1.scrape.center{link_tag['href']}" if link_tag else 'N/A'
        
        return {
            'Title': title,
            'Categories': category_str,
            'Region': region,
            'Duration': duration,
            'Release Date': release_date,
            'Score': score,
            'Cover URL': cover_url,
            'Detail URL': detail_url
        }
    
    def parse_page(self, soup: BeautifulSoup) -> List[Dict]:
        """
        解析單個頁面的所有電影資訊
        
        Args:
            soup: BeautifulSoup 物件
            
        Returns:
            電影資訊列表
        """
        if not soup:
            return []
        
        items = soup.find_all(class_='el-card__body')
        page_movies = []
        
        for item in items:
            try:
                movie_info = self.parse_movie_info(item)
                page_movies.append(movie_info)
            except Exception as e:
                print(f"解析電影資訊時發生錯誤: {e}")
                continue
        
        print(f"本頁解析到 {len(page_movies)} 部電影")
        return page_movies
    
    def crawl(self, start_page: int = 1, end_page: int = 10, delay: float = 1.0):
        """
        爬取指定範圍的頁面
        
        Args:
            start_page: 起始頁碼
            end_page: 結束頁碼（包含）
            delay: 每次請求之間的延遲時間（秒）
        """
        print(f"開始爬取電影資訊，從第 {start_page} 頁到第 {end_page} 頁")
        print("=" * 60)
        
        for page_num in range(start_page, end_page + 1):
            # 獲取頁面 HTML
            soup = self.fetch_page(page_num)
            
            # 解析電影資訊
            page_movies = self.parse_page(soup)
            self.movies.extend(page_movies)
            
            # 禮貌性延遲，避免對伺服器造成過大壓力
            if page_num < end_page:
                time.sleep(delay)
        
        print("=" * 60)
        print(f"爬取完成！共收集 {len(self.movies)} 部電影資訊")
    
    def save_to_csv(self, filename: str = 'movie.csv'):
        """
        將電影資訊儲存為 CSV 檔案
        
        Args:
            filename: 輸出檔名
        """
        if not self.movies:
            print("沒有電影資訊可儲存")
            return
        
        df = pd.DataFrame(self.movies)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"電影資訊已儲存至 {filename}")
        print(f"總共儲存 {len(df)} 筆資料")
        
        # 顯示資料摘要
        print("\n資料摘要:")
        print(df.head())
        print(f"\nCSV 欄位: {', '.join(df.columns.tolist())}")
    
    def get_statistics(self):
        """顯示爬取的資料統計"""
        if not self.movies:
            print("沒有可用的統計資料")
            return
        
        df = pd.DataFrame(self.movies)
        
        print("\n" + "=" * 60)
        print("資料統計")
        print("=" * 60)
        print(f"總電影數: {len(df)}")
        print(f"\n評分分布:")
        print(df['Score'].value_counts().head(10))
        
        # 統計類別
        all_categories = []
        for cats in df['Categories'].dropna():
            if cats != 'N/A':
                all_categories.extend([c.strip() for c in cats.split(',')])
        
        if all_categories:
            from collections import Counter
            cat_counter = Counter(all_categories)
            print(f"\n最常見的電影類別:")
            for cat, count in cat_counter.most_common(10):
                print(f"  {cat}: {count} 部")


def main():
    """主程式"""
    # 建立爬蟲實例
    crawler = MovieCrawler()
    
    # 爬取 10 頁電影資訊
    crawler.crawl(start_page=1, end_page=10, delay=1.0)
    
    # 儲存為 CSV
    crawler.save_to_csv('movie.csv')
    
    # 顯示統計資訊
    crawler.get_statistics()


if __name__ == "__main__":
    main()
