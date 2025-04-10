import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
import schedule

# -------- 爬虫逻辑 -------- #
def fetch_baidu_news(query, max_results=5):
    query_encoded = urllib.parse.quote(query)
    url = f"https://www.baidu.com/s?tn=news&word={query_encoded}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for item in soup.select('div.result')[:max_results]:
        a_tag = item.find('a')
        if a_tag:
            title = a_tag.get_text(strip=True)
            link = a_tag['href']
            results.append((title, link))
    return results

def fetch_sina_news(query, max_results=5):
    query_encoded = urllib.parse.quote(query)
    url = f"https://search.sina.com.cn/?q={query_encoded}&c=news"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for item in soup.select('div.box-result.clearfix')[:max_results]:
        h2_tag = item.find('h2')
        if h2_tag and h2_tag.a:
            title = h2_tag.a.get_text(strip=True)
            link = h2_tag.a['href']
            results.append((title, link))
    return results

# -------- Streamlit 页面 -------- #
st.title("📰 中文新闻爬虫工具（百度 + 新浪）")
query = st.text_input("请输入关键词", "2025年4月 美国 关税")

if st.button("🔍 开始抓取"):
    st.write("正在抓取新闻，请稍候...")

    baidu_news = fetch_baidu_news(query)
    sina_news = fetch_sina_news(query)

    st.subheader("📌 百度新闻")
    if baidu_news:
        for idx, (title, link) in enumerate(baidu_news, 1):
            st.markdown(f"{idx}. [{title}]({link})")
    else:
        st.write("未抓到百度新闻内容")

    st.subheader("📌 新浪新闻")
    if sina_news:
        for idx, (title, link) in enumerate(sina_news, 1):
            st.markdown(f"{idx}. [{title}]({link})")
    else:
        st.write("未抓到新浪新闻内容")

# -------- 定时任务逻辑（选填） -------- #
def scheduled_task():
    print("⏰ 定时抓取一次新闻...")
    fetch_baidu_news(query)
    fetch_sina_news(query)

# 每隔30分钟抓一次（如需后台运行请取消注释）
# schedule.every(30).minutes.do(scheduled_task)
# while True:
#     schedule.run_pending()
#     time.sleep(1)