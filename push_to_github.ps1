# 快速上傳到 GitHub 腳本

Write-Host "正在上傳到 GitHub..." -ForegroundColor Green
Write-Host ""

# 推送到 GitHub
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ 成功上傳到 GitHub！" -ForegroundColor Green
    Write-Host ""
    Write-Host "🔗 GitHub Repository: https://github.com/pcchou102/movie_crawler" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📝 接下來的步驟：" -ForegroundColor Yellow
    Write-Host "1. 前往 https://share.streamlit.io" -ForegroundColor White
    Write-Host "2. 使用 GitHub 帳號登入" -ForegroundColor White
    Write-Host "3. 點擊 'New app'" -ForegroundColor White
    Write-Host "4. 選擇 Repository: pcchou102/movie_crawler" -ForegroundColor White
    Write-Host "5. 設定 Main file path: app.py" -ForegroundColor White
    Write-Host "6. 點擊 'Deploy!'" -ForegroundColor White
    Write-Host ""
    Write-Host "⏱️  部署通常需要 2-3 分鐘" -ForegroundColor Magenta
    Write-Host "🌐 部署完成後的網址: https://movie-crawler.streamlit.app" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "❌ 上傳失敗！" -ForegroundColor Red
    Write-Host ""
    Write-Host "可能的原因：" -ForegroundColor Yellow
    Write-Host "1. 尚未設定 GitHub 認證" -ForegroundColor White
    Write-Host "2. Repository 尚未在 GitHub 上建立" -ForegroundColor White
    Write-Host "3. 網路連線問題" -ForegroundColor White
    Write-Host ""
    Write-Host "解決方法：" -ForegroundColor Yellow
    Write-Host "1. 使用 GitHub Desktop (推薦)" -ForegroundColor White
    Write-Host "2. 或設定 Personal Access Token" -ForegroundColor White
    Write-Host "   參考: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token" -ForegroundColor White
    Write-Host ""
}

Write-Host "按任意鍵繼續..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
