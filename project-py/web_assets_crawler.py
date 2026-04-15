import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import time
import random
from concurrent.futures import ThreadPoolExecutor
import urllib3
import re

# Tắt cảnh báo SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class WebAssetsCrawler:
    def __init__(self, url, output_dir=None):
        self.start_url = url
        # Tạo thư mục đầu ra với tên domain
        domain = urlparse(url).netloc
        self.output_dir = output_dir or f"crawled_sites/{domain}"
        self.session = requests.Session()
        self.downloaded_files = set()
        
        # Tạo User-Agent giả
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36"
        }

    def download_file(self, url, subfolder):
        """Tải file và lưu vào thư mục con tương ứng"""
        if url in self.downloaded_files:
            return

        try:
            # Tạo tên file từ URL
            filename = os.path.basename(urlparse(url).path)
            if not filename:
                filename = "index.html"
            
            # Thêm .html cho các file không có phần mở rộng
            if not os.path.splitext(filename)[1]:
                filename += ".html"
            
            # Tạo đường dẫn đầy đủ
            output_path = os.path.join(self.output_dir, subfolder, filename)
            
            # Tạo thư mục nếu chưa tồn tại
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Tải file
            print(f"📥 Đang tải: {url}")
            response = self.session.get(url, headers=self.headers, verify=False, timeout=10)
            response.raise_for_status()
            
            # Lưu file
            with open(output_path, "wb") as f:
                f.write(response.content)
            
            self.downloaded_files.add(url)
            return output_path

        except Exception as e:
            print(f"❌ Lỗi khi tải {url}: {str(e)}")
            return None

    def download_css_images(self, css_content, css_url):
        """Tải các hình ảnh được tham chiếu trong CSS"""
        # Tìm tất cả URL trong CSS
        urls = re.findall(r'url\(["\']?(.*?)["\']?\)', css_content)
        
        for url in urls:
            if url.startswith('data:'):  # Bỏ qua data URL
                continue
                
            full_url = urljoin(css_url, url)
            self.download_file(full_url, "images")

    def crawl(self):
        """Bắt đầu crawl trang web"""
        try:
            print(f"🔍 Bắt đầu crawl: {self.start_url}")
            
            # Tải trang chủ
            response = self.session.get(
                self.start_url, 
                headers=self.headers, 
                verify=False,
                timeout=10
            )
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Lưu HTML chính
            html_path = os.path.join(self.output_dir, "index.html")
            os.makedirs(self.output_dir, exist_ok=True)
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"✅ Đã lưu HTML chính vào: {html_path}")
            
            # Tìm và tải CSS
            css_links = []
            for css in soup.find_all("link", rel="stylesheet"):
                if css.get("href"):
                    css_url = urljoin(self.start_url, css.get("href"))
                    css_links.append(css_url)
            
            # Tìm và tải JavaScript
            js_links = []
            for script in soup.find_all("script", src=True):
                if script.get("src"):
                    js_url = urljoin(self.start_url, script.get("src"))
                    js_links.append(js_url)
            
            # Tải CSS và JS song song
            with ThreadPoolExecutor(max_workers=5) as executor:
                # Tải CSS
                css_futures = [
                    executor.submit(self.download_file, url, "css")
                    for url in css_links
                ]
                
                # Tải JavaScript
                js_futures = [
                    executor.submit(self.download_file, url, "js")
                    for url in js_links
                ]
                
                # Đợi tải xong
                for future in css_futures + js_futures:
                    future.result()
            
            # Tải hình ảnh
            img_links = []
            for img in soup.find_all("img", src=True):
                if img.get("src"):
                    img_url = urljoin(self.start_url, img.get("src"))
                    img_links.append(img_url)
            
            # Tải hình ảnh song song
            with ThreadPoolExecutor(max_workers=5) as executor:
                img_futures = [
                    executor.submit(self.download_file, url, "images")
                    for url in img_links
                ]
                
                for future in img_futures:
                    future.result()
            
            print(f"""
✨ Crawl hoàn tất! 
📁 Thư mục lưu trữ: {self.output_dir}
📊 Thống kê:
   - CSS files: {len([f for f in self.downloaded_files if f in css_links])}
   - JS files: {len([f for f in self.downloaded_files if f in js_links])}
   - Images: {len([f for f in self.downloaded_files if f in img_links])}
            """)
            
        except Exception as e:
            print(f"❌ Lỗi: {str(e)}")

def main():
    import argparse
    
    # Tạo parser cho command line arguments
    parser = argparse.ArgumentParser(description='Crawl web assets (HTML, CSS, JS, Images) từ một URL.')
    parser.add_argument('url', help='URL trang web cần crawl')
    parser.add_argument('--output', '-o', help='Thư mục lưu kết quả (tùy chọn)')
    
    # Parse arguments
    args = parser.parse_args()
    
    print(f"🎯 URL: {args.url}")
    print(f"📁 Thư mục đầu ra: {args.output or 'mặc định'}")
    
    # Tạo và chạy crawler
    crawler = WebAssetsCrawler(args.url, args.output)
    crawler.crawl()

if __name__ == "__main__":
    main()
