# 電影爬蟲與展示系統

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://movie-crawler.streamlit.app)

🌐 **線上展示：[[https://movie-crawler.streamlit.app](https://movie-crawler.streamlit.app)](https://cwaweather-kspfc8samf3xupib2tciau.streamlit.app/)**

這是一個完整的電影資料爬蟲與視覺化展示系統，從 [https://ssr1.scrape.center/](https://ssr1.scrape.center/) 爬取電影資訊，並使用 Streamlit 建立互動式網頁應用程式。

## 📁 專案結構

```
爬蟲/
├── movie_crawler.py    # 主要爬蟲程式（物件導向設計）
├── scraper.py          # 簡化版爬蟲程式
├── app.py              # Streamlit 網頁應用程式
├── movie.csv           # 爬取的電影資料
├── requirements.txt    # Python 套件依賴
└── README.md           # 專案說明文件
```

## 🚀 快速開始

### 1. 安裝依賴套件

```bash
pip install -r requirements.txt
```

### 2. 執行爬蟲程式

使用完整版爬蟲（推薦）：
```bash
python movie_crawler.py
```

或使用簡化版：
```bash
python scraper.py
```

爬蟲會：
- 依序爬取 10 頁電影資訊（共 100 部電影）
- 解析每部電影的標題、類別、地區、時長、上映日期、評分、封面圖、詳情連結
- 將資料儲存為 `movie.csv`
- 顯示爬取統計資訊

### 3. 啟動 Streamlit 應用程式

```bash
streamlit run app.py
```

瀏覽器會自動開啟，預設網址為：`http://localhost:8501`

## 📊 功能特色

### 爬蟲程式 (`movie_crawler.py`)

- **物件導向設計**：使用 `MovieCrawler` 類別，便於擴展和維護
- **依序爬取**：按照頁碼順序爬取 1-10 頁
- **完整資料解析**：
  - 電影標題（中英文）
  - 電影類別（可能有多個）
  - 地區資訊
  - 片長
  - 上映日期
  - 評分
  - 封面圖片 URL
  - 詳情頁面連結
- **錯誤處理**：妥善處理網路錯誤和解析錯誤
- **禮貌爬取**：每次請求間隔 1 秒，避免對伺服器造成負擔
- **資料統計**：自動生成爬取資料的統計報告

### Streamlit 應用程式 (`app.py`)

#### 📈 資料總覽
- 顯示電影總數、平均評分、最高評分、類別數量

#### 🔍 篩選功能
- **搜尋**：依電影標題關鍵字搜尋
- **評分範圍**：使用滑桿選擇評分範圍
- **電影類別**：多選電影類別（劇情、愛情、動作等）
- **排序方式**：
  - 評分（高到低）
  - 評分（低到高）
  - 標題（A-Z）
  - 上映日期

#### 📱 三種展示模式

**1. 🖼️ 圖片展示**
- 以卡片形式展示電影
- 可調整每列顯示數量（2-5 列）
- 顯示封面圖片、標題、評分、類別、時長、地區、上映日期
- 提供「查看詳情」按鈕

**2. 📊 表格檢視**
- 完整表格展示所有欄位
- 支援排序和篩選
- 可下載篩選結果為 CSV

**3. 📈 資料分析**
- 評分分布圖
- 類別統計（前 10 名）
- Top 10 高評分電影

## 📋 資料欄位說明

| 欄位名稱 | 說明 | 範例 |
|---------|------|------|
| Title | 電影標題（中英文） | 霸王別姬 - Farewell My Concubine |
| Categories | 電影類別 | 劇情, 愛情 |
| Region | 上映地區 | 中國內地、中國香港 |
| Duration | 片長 | 171 分鐘 |
| Release Date | 上映日期 | 1993-07-26 上映 |
| Score | 評分 | 9.5 |
| Cover URL | 封面圖片連結 | https://... |
| Detail URL | 詳情頁面連結 | https://ssr1.scrape.center/detail/1 |

## 🛠️ 技術棧

- **Python 3.x**
- **Requests**：HTTP 請求
- **BeautifulSoup4**：HTML 解析
- **Pandas**：資料處理與分析
- **Streamlit**：互動式網頁應用程式

## 💡 使用建議

1. **重新爬取資料**：如果網站內容有更新，重新執行爬蟲程式即可更新資料
2. **調整爬取範圍**：修改 `movie_crawler.py` 中的 `end_page` 參數來改變爬取頁數
3. **自訂展示**：可以修改 `app.py` 來添加更多視覺化功能
4. **部署到雲端**：可以將 Streamlit 應用程式部署到 Streamlit Cloud、Heroku 等平台

## 🌐 部署到 Streamlit Cloud

### 方法一：透過 GitHub 自動部署（推薦）

1. **上傳專案到 GitHub**
   ```bash
   cd "c:\Users\周\Desktop\AIOT\爬蟲"
   git init
   git add .
   git commit -m "Initial commit: Movie crawler with Streamlit app"
   git branch -M main
   git remote add origin https://github.com/pcchou102/movie_crawler.git
   git push -u origin main
   ```

2. **登入 Streamlit Cloud**
   - 前往 [share.streamlit.io](https://share.streamlit.io)
   - 使用 GitHub 帳號登入

3. **部署應用程式**
   - 點擊「New app」
   - 選擇 repository：`pcchou102/movie_crawler`
   - 設定 Main file path：`app.py`
   - 點擊「Deploy」

4. **等待部署完成**
   - 通常需要 2-3 分鐘
   - 部署完成後會得到一個網址：`https://movie-crawler.streamlit.app`

### 方法二：使用 Streamlit CLI 部署

```bash
streamlit deploy app.py
```

## 📦 Git 使用說明

專案已包含 `.gitignore` 檔案，以下檔案不會被上傳到 GitHub：
- Python 快取檔案（`__pycache__/`）
- 虛擬環境（`venv/`, `env/`）
- IDE 設定檔（`.vscode/`, `.idea/`）
- 作業系統檔案（`.DS_Store`, `Thumbs.db`）

**注意**：`movie.csv` 會被上傳，因為 Streamlit 應用程式需要這個檔案來顯示資料。

## 📝 注意事項

- 請遵守網站的 robots.txt 和使用條款
- 爬取時使用合理的請求間隔，避免對伺服器造成負擔
- 僅用於學習和研究目的
- 爬取的資料版權歸原網站所有

## 🔄 更新記錄

- **v1.0** (2025-12-04)
  - 完成電影爬蟲程式
  - 建立 Streamlit 展示介面
  - 支援多種篩選和排序功能
  - 提供三種展示模式

## 📧 問題回報

如有任何問題或建議，歡迎提出 Issue。

---

**Happy Coding! 🎬✨**
