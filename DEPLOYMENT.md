# 部署指南

## 📤 上傳到 GitHub

專案已經初始化完成，現在可以上傳到 GitHub：

```powershell
git push -u origin main
```

如果遇到權限問題，可能需要：
1. 使用 Personal Access Token (PAT)
2. 或使用 GitHub Desktop
3. 或使用 SSH 金鑰

## 🚀 部署到 Streamlit Cloud

### 步驟 1：確認 GitHub Repository
確保專案已上傳到：`https://github.com/pcchou102/movie_crawler`

### 步驟 2：登入 Streamlit Cloud
1. 前往 [share.streamlit.io](https://share.streamlit.io)
2. 使用 GitHub 帳號登入
3. 授權 Streamlit Cloud 存取您的 GitHub

### 步驟 3：部署應用程式
1. 點擊「New app」按鈕
2. 選擇以下設定：
   - **Repository:** `pcchou102/movie_crawler`
   - **Branch:** `main`
   - **Main file path:** `app.py`
3. 點擊「Deploy!」按鈕

### 步驟 4：等待部署完成
- 部署通常需要 2-5 分鐘
- 可以在部署日誌中看到進度
- 部署成功後，會顯示應用程式網址

### 步驟 5：取得網址
部署完成後，您的應用程式網址會是：
- `https://movie-crawler.streamlit.app` (自訂網址)
- 或 `https://share.streamlit.io/pcchou102/movie_crawler/main/app.py`

## 🔄 更新部署

當您修改程式碼並推送到 GitHub 後：

```powershell
git add .
git commit -m "更新說明"
git push
```

Streamlit Cloud 會自動偵測變更並重新部署！

## ⚙️ Streamlit Cloud 設定

### Python 版本
Streamlit Cloud 會自動使用 Python 3.9+，無需額外設定。

### 依賴套件
確保 `requirements.txt` 包含所有必要套件：
- requests
- beautifulsoup4
- pandas
- streamlit

### 資料檔案
`movie.csv` 會隨著專案一起部署，所以應用程式啟動後就能直接顯示資料。

## 🎯 自訂網域（選擇性）

Streamlit Cloud 的免費方案會提供一個預設網址。如果需要自訂網域：
1. 在 Streamlit Cloud 設定中找到「Custom subdomain」
2. 輸入想要的子網域名稱
3. 儲存後，網址會變更為：`https://your-custom-name.streamlit.app`

## 📝 注意事項

1. **免費額度**：Streamlit Community Cloud 提供免費託管，但有資源限制
2. **休眠機制**：如果應用程式 7 天未使用，會進入休眠狀態
3. **重新啟動**：訪問休眠的應用程式時，需要 30-60 秒啟動
4. **公開存取**：免費方案的應用程式是公開的，任何人都可以存取

## 🔒 隱私設定（選擇性）

如果需要限制存取：
1. 在 Streamlit Cloud 設定中找到「Sharing」
2. 選擇「Private」
3. 添加允許存取的 email 地址

## 📊 監控與日誌

在 Streamlit Cloud 控制台可以：
- 查看應用程式運行狀態
- 檢視日誌訊息
- 監控資源使用情況
- 重新啟動應用程式

---

**祝部署順利！🎉**
