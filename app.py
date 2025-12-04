import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="電影資料庫",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自訂 CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 1rem;
    }
    .movie-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
        background-color: #f9f9f9;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🎬 電影資料庫</h1>', unsafe_allow_html=True)
st.markdown("資料來源：[https://ssr1.scrape.center/](https://ssr1.scrape.center/)")

@st.cache_data
def load_data():
    """載入電影資料"""
    if os.path.exists('movie.csv'):
        df = pd.read_csv('movie.csv')
        # 轉換評分為數值型態
        df['Score'] = pd.to_numeric(df['Score'], errors='coerce')
        return df
    return None


try:
    df = load_data()
    
    if df is None:
        st.error("❌ 找不到 movie.csv 檔案！")
        st.info("請先執行 `python movie_crawler.py` 來爬取電影資料")
        st.stop()
    
    # 顯示統計資訊
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 電影總數", len(df))
    
    with col2:
        avg_score = df['Score'].mean()
        st.metric("⭐ 平均評分", f"{avg_score:.2f}")
    
    with col3:
        max_score = df['Score'].max()
        st.metric("🏆 最高評分", f"{max_score:.1f}")
    
    with col4:
        total_categories = len(set([c.strip() for cats in df['Categories'].dropna() 
                                    for c in cats.split(',') if cats != 'N/A']))
        st.metric("🎭 電影類別", total_categories)
    
    st.markdown("---")
    
    # 側邊欄篩選器
    st.sidebar.header("🔍 篩選選項")
    
    # 搜尋框
    search_term = st.sidebar.text_input("🔎 搜尋電影標題", "")
    
    # 評分範圍
    st.sidebar.subheader("評分範圍")
    score_range = st.sidebar.slider(
        "選擇評分範圍",
        float(df['Score'].min()),
        float(df['Score'].max()),
        (float(df['Score'].min()), float(df['Score'].max())),
        0.1
    )
    
    # 電影類別
    st.sidebar.subheader("電影類別")
    all_categories = set()
    for cats in df['Categories'].dropna():
        if cats != 'N/A':
            for c in cats.split(','):
                all_categories.add(c.strip())
    
    selected_categories = st.sidebar.multiselect(
        "選擇類別（可多選）",
        sorted(list(all_categories))
    )
    
    # 排序方式
    st.sidebar.subheader("排序方式")
    sort_by = st.sidebar.selectbox(
        "排序依據",
        ["評分（高到低）", "評分（低到高）", "標題（A-Z）", "上映日期"]
    )
    
    # 套用篩選
    filtered_df = df.copy()
    
    # 搜尋篩選
    if search_term:
        filtered_df = filtered_df[filtered_df['Title'].str.contains(search_term, case=False, na=False)]
    
    # 評分篩選
    filtered_df = filtered_df[
        (filtered_df['Score'] >= score_range[0]) & 
        (filtered_df['Score'] <= score_range[1])
    ]
    
    # 類別篩選
    if selected_categories:
        mask = filtered_df['Categories'].apply(
            lambda x: any(cat in str(x) for cat in selected_categories)
        )
        filtered_df = filtered_df[mask]
    
    # 排序
    if sort_by == "評分（高到低）":
        filtered_df = filtered_df.sort_values('Score', ascending=False)
    elif sort_by == "評分（低到高）":
        filtered_df = filtered_df.sort_values('Score', ascending=True)
    elif sort_by == "標題（A-Z）":
        filtered_df = filtered_df.sort_values('Title')
    elif sort_by == "上映日期":
        filtered_df = filtered_df.sort_values('Release Date', ascending=False)
    
    # 顯示結果
    st.subheader(f"📋 找到 {len(filtered_df)} 部電影")
    
    # 標籤頁
    tab1, tab2, tab3 = st.tabs(["🖼️ 圖片展示", "📊 表格檢視", "📈 資料分析"])
    
    with tab1:
        # 圖片卡片展示
        if len(filtered_df) > 0:
            # 每列顯示數量選擇
            cols_per_row = st.select_slider("每列顯示數量", options=[2, 3, 4, 5], value=4)
            
            cols = st.columns(cols_per_row)
            for idx, row in filtered_df.iterrows():
                col = cols[idx % cols_per_row]
                with col:
                    # 顯示封面圖片
                    if row['Cover URL'] != 'N/A':
                        st.image(row['Cover URL'], width='stretch')
                    
                    # 電影標題
                    st.markdown(f"**{row['Title']}**")
                    
                    # 評分與星星
                    score = row['Score']
                    stars = "⭐" * int(score // 2)
                    st.markdown(f"{stars} {score}")
                    
                    # 其他資訊
                    st.caption(f"🎭 {row['Categories']}")
                    st.caption(f"⏱️ {row['Duration']}")
                    st.caption(f"🌍 {row['Region']}")
                    st.caption(f"📅 {row['Release Date']}")
                    
                    # 詳情連結
                    if 'Detail URL' in row and row['Detail URL'] != 'N/A':
                        st.link_button("查看詳情", row['Detail URL'], width='stretch')
                    
                    st.divider()
        else:
            st.info("沒有符合條件的電影")
    
    with tab2:
        # 表格檢視
        st.dataframe(
            filtered_df,
            width='stretch',
            hide_index=True,
            column_config={
                "Cover URL": st.column_config.ImageColumn("封面", width="small"),
                "Score": st.column_config.NumberColumn("評分", format="%.1f"),
                "Detail URL": st.column_config.LinkColumn("詳情連結")
            }
        )
        
        # 下載按鈕
        csv = filtered_df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 下載篩選結果 (CSV)",
            data=csv,
            file_name="filtered_movies.csv",
            mime="text/csv"
        )
    
    with tab3:
        # 資料分析
        st.subheader("📈 評分分布")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 評分分布圖
            score_counts = filtered_df['Score'].value_counts().sort_index()
            st.bar_chart(score_counts)
        
        with col2:
            # 類別統計
            st.subheader("🎭 類別統計")
            category_list = []
            for cats in filtered_df['Categories'].dropna():
                if cats != 'N/A':
                    category_list.extend([c.strip() for c in cats.split(',')])
            
            if category_list:
                from collections import Counter
                cat_counter = Counter(category_list)
                cat_df = pd.DataFrame(cat_counter.most_common(10), columns=['類別', '數量'])
                st.dataframe(cat_df, width='stretch', hide_index=True)
        
        # Top 10 電影
        st.subheader("🏆 Top 10 高評分電影")
        top_movies = filtered_df.nlargest(10, 'Score')[['Title', 'Score', 'Categories', 'Release Date']]
        st.dataframe(top_movies, width='stretch', hide_index=True)

except Exception as e:
    st.error(f"❌ 發生錯誤: {str(e)}")
    st.info("請確認 movie.csv 檔案格式正確")

