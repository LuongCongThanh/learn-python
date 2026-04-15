import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pandas as pd
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AdvancedCrawler:
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; rv:109.0) Gecko/20100101 Firefox/115.0"
    ]

    def __init__(self, start_url, max_pages=50, max_workers=5, use_selenium=False):
        self.start_url = start_url
        self.max_pages = max_pages
        self.max_workers = max_workers
        self.use_selenium = use_selenium
        self.visited = set()
        self.data = []
        
        if use_selenium:
            self.setup_selenium()

    def setup_selenium(self):
        """Khởi tạo trình duyệt Chrome ở chế độ headless"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Chạy ẩn
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"user-agent={random.choice(self.USER_AGENTS)}")
        self.driver = webdriver.Chrome(options=chrome_options)

    def get_page_selenium(self, url):
        """Tải trang bằng Selenium (hỗ trợ JavaScript)"""
        try:
            self.driver.get(url)
            # Đợi body load xong
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            # Đợi thêm 2s cho JavaScript chạy
            time.sleep(2)
            return self.driver.page_source
        except Exception as e:
            print(f"❌ Lỗi selenium tại {url}: {e}")
            return None

    def get_page_requests(self, url):
        """Tải trang bằng requests (web tĩnh)"""
        headers = {"User-Agent": random.choice(self.USER_AGENTS)}
        try:
            res = requests.get(url, headers=headers, timeout=10)
            res.raise_for_status()
            return res.text
        except Exception as e:
            print(f"❌ Lỗi requests tại {url}: {e}")
            return None

    def get_page(self, url):
        """Tải trang web (tự động chọn phương thức phù hợp)"""
        if self.use_selenium:
            return self.get_page_selenium(url)
        return self.get_page_requests(url)

    def get_internal_links(self, html, base_url):
        """Tìm tất cả link nội bộ trong trang"""
        if not html:
            return set()
            
        soup = BeautifulSoup(html, "lxml")
        links = set()
        
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            if not href:
                continue
                
            full_url = urljoin(base_url, href)
            if self.is_internal_link(full_url, base_url):
                # Bỏ phần fragment (#) trong URL
                clean_url = full_url.split("#")[0]
                links.add(clean_url)
                
        return links

    def is_internal_link(self, url, base_url):
        """Kiểm tra xem có phải link nội bộ không"""
        return urlparse(url).netloc == urlparse(base_url).netloc

    def process_page(self, url):
        """Xử lý một trang web"""
        if url in self.visited:
            return None

        print(f"🔍 Crawling: {url}")
        html = self.get_page(url)
        if not html:
            return None

        self.visited.add(url)
        soup = BeautifulSoup(html, "lxml")
        
        # Lấy title và description
        title = soup.title.string if soup.title else "No Title"
        meta_desc = soup.find("meta", {"name": "description"})
        description = meta_desc["content"] if meta_desc else "No Description"

        data = {
            "url": url,
            "title": title.strip() if title else "",
            "description": description.strip() if description else ""
        }

        # Tìm thêm link để crawl
        new_links = self.get_internal_links(html, self.start_url)
        return data, new_links

    def crawl(self):
        """Bắt đầu quá trình crawl song song"""
        to_visit = {self.start_url}
        self.data = []  # Reset data

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            while to_visit and len(self.visited) < self.max_pages:
                # Tạo futures cho các URL chưa thăm
                futures = {
                    executor.submit(self.process_page, url): url 
                    for url in list(to_visit)[:self.max_workers]
                }
                
                for future in as_completed(futures):
                    url = futures[future]
                    to_visit.remove(url)
                    
                    try:
                        result = future.result()
                        if result:
                            data, new_links = result
                            self.data.append(data)  # Add to instance data
                            # Thêm links mới vào hàng đợi
                            to_visit.update(new_links - self.visited)
                    except Exception as e:
                        print(f"❌ Lỗi xử lý {url}: {e}")

                    time.sleep(random.uniform(0.5, 1.5))  # Delay ngẫu nhiên

        if self.use_selenium:
            self.driver.quit()

        return self.data

    def save_to_csv(self, filename="crawl_results.csv"):
        """Lưu kết quả ra file CSV"""
        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False, encoding="utf-8-sig")
        print(f"✅ Đã lưu {len(self.data)} kết quả vào {filename}")

def main():
    # Ví dụ sử dụng:
    start_url = "https://quotes.toscrape.com"  # URL trang web cần crawl
    
    # Crawl web tĩnh
    crawler = AdvancedCrawler(
        start_url=start_url,
        max_pages=20,
        max_workers=5,
        use_selenium=False  # Đổi thành True nếu cần xử lý JavaScript
    )
    
    results = crawler.crawl()
    crawler.save_to_csv()

if __name__ == "__main__":
    main()
