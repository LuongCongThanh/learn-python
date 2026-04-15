from advanced_crawler import AdvancedCrawler
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import random
import urllib3
import ssl
import requests
import os
import uuid

# Tắt cảnh báo SSL để tránh lỗi chứng chỉ
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ThanhNienCrawler(AdvancedCrawler):
    """Crawler được tối ưu cho trang Thanh Niên"""
    
    def get_page(self, url):
        """Tải trang với retry và xử lý lỗi SSL"""
        max_retries = 3
        retry_delay = 2

        for attempt in range(max_retries):
            try:
                if self.use_selenium:
                    # Thêm tùy chọn bỏ qua lỗi SSL cho Selenium
                    self.driver.get(url)
                    time.sleep(3)  # Đợi trang load
                    return self.driver.page_source
                else:
                    headers = {"User-Agent": random.choice(self.USER_AGENTS)}
                    response = requests.get(
                        url,
                        headers=headers,
                        timeout=15,
                        verify=False  # Bỏ qua xác thực SSL
                    )
                    response.raise_for_status()
                    return response.text
            except Exception as e:
                print(f"⚠️ Lần thử {attempt + 1}/{max_retries} thất bại: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Tăng thời gian chờ giữa các lần thử
                else:
                    print(f"❌ Không thể tải trang {url} sau {max_retries} lần thử")
                    return None
    
    def get_internal_links(self, html, base_url):
        """Lọc các link theo các chuyên mục quan trọng"""
        if not html:
            return set()

        soup = BeautifulSoup(html, "lxml")
        links = set()
        
        # Lấy tất cả thẻ a có href
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            if not href:
                continue
                
            # Chuyển đổi relative URL thành absolute URL
            full_url = urljoin(base_url, href)
            
            # Chỉ lấy các URL từ domain thanhnien.vn
            if "thanhnien.vn" in full_url:
                # Lọc các URL không mong muốn
                if any(x in full_url.lower() for x in [".jpg", ".png", ".pdf", "javascript:", "#", "mailto:", "tel:"]):
                    continue
                    
                # Loại bỏ các tham số query và fragment
                clean_url = full_url.split("?")[0].split("#")[0]
                links.add(clean_url)
                
        return links
        
    def save_page_content(self, url, html, article_id):
        """Lưu nội dung trang web"""
        try:
            # Tạo thư mục cho bài viết
            article_dir = f"thanhnien_data/article_{article_id}"
            os.makedirs(article_dir, exist_ok=True)
            
            # Lưu HTML gốc
            with open(f"{article_dir}/original.html", "w", encoding="utf-8") as f:
                f.write(html)
            
            soup = BeautifulSoup(html, "lxml")
            
            # Lưu nội dung bài viết (chỉ phần content)
            article_content = soup.select_one(".detail-article")
            if article_content:
                # Lưu nội dung dạng text
                with open(f"{article_dir}/content.txt", "w", encoding="utf-8") as f:
                    f.write(article_content.get_text(separator="\n", strip=True))
                
                # Lưu nội dung HTML đã làm sạch
                with open(f"{article_dir}/content.html", "w", encoding="utf-8") as f:
                    f.write(str(article_content))
            
            # Lưu hình ảnh trong bài viết
            for img in soup.select(".detail-article img[src]"):
                try:
                    img_url = urljoin(url, img["src"])
                    img_filename = os.path.basename(img_url).split("?")[0]
                    img_path = f"{article_dir}/images"
                    os.makedirs(img_path, exist_ok=True)
                    
                    img_response = requests.get(img_url, verify=False)
                    with open(f"{img_path}/{img_filename}", "wb") as f:
                        f.write(img_response.content)
                except Exception as e:
                    print(f"⚠️ Không thể tải ảnh từ {img_url}: {e}")
            
            return article_dir
        except Exception as e:
            print(f"❌ Lỗi khi lưu nội dung cho {url}: {e}")
            return None

    def process_page(self, url):
        """Xử lý trang và trích xuất thông tin bài viết"""
        if url in self.visited:
            return None

        try:
            print(f"🔍 Đang crawl: {url}")
            html = self.get_page(url)
            if not html:
                print(f"⚠️ Không thể tải trang: {url}")
                return None

            self.visited.add(url)
            soup = BeautifulSoup(html, "lxml")
            
            # Kiểm tra xem có phải trang bài viết không
            if not soup.select_one(".detail-article"):
                return None, self.get_internal_links(html, self.start_url)
                
            # Tạo ID duy nhất cho bài viết
            article_id = str(uuid.uuid4())[:8]
            
            # Lưu nội dung trang
            content_dir = self.save_page_content(url, html, article_id)
            
            # Thêm đường dẫn đến thư mục nội dung vào dữ liệu
            data["content_directory"] = content_dir
            
            # Lấy tiêu đề
            title = soup.title.string if soup.title else "No Title"
            
            # Lấy chuyên mục
            category = "Unknown"
            breadcrumb = soup.select_one(".breadcrumb")
            if breadcrumb:
                category = breadcrumb.get_text(strip=True)
                
            # Lấy thời gian đăng
            publish_time = ""
            time_element = soup.select_one(".meta time")
            if time_element:
                publish_time = time_element.get_text(strip=True)
                
            # Lấy tóm tắt bài viết
            summary = ""
            summary_element = soup.select_one(".sapo")
            if summary_element:
                summary = summary_element.get_text(strip=True)

            data = {
                "url": url,
                "title": title.strip() if title else "",
                "category": category,
                "publish_time": publish_time,
                "summary": summary
            }

            # Tìm các link khác
            new_links = self.get_internal_links(html, self.start_url)
            
            # Delay ngẫu nhiên để tránh bị chặn
            time.sleep(random.uniform(2, 3))
            
            return data, new_links

        except Exception as e:
            print(f"❌ Lỗi khi xử lý trang {url}: {str(e)}")
            return None

def crawl_thanhnien():
    target_url = "https://thanhnien.vn"
    
    print(f"🔥 Bắt đầu crawl Thanh Niên từ: {target_url}")
    print("ℹ️  Chỉ crawl các bài viết từ chuyên mục chính")
    
    crawler = ThanhNienCrawler(
        start_url=target_url,
        max_pages=15,  # Giới hạn số trang để test
        max_workers=2,  # Giữ 2 luồng để tránh bị block
        use_selenium=False  # Thử không dùng Selenium trước
    )
    
    print("⏳ Đang crawl dữ liệu, quá trình này có thể mất vài phút...")
    crawler.crawl()
    
    output_file = "thanhnien_articles.csv"
    crawler.save_to_csv(output_file)
    print(f"✅ Hoàn thành! Đã lưu {len(crawler.data)} bài viết vào {output_file}")

if __name__ == "__main__":
    try:
        crawl_thanhnien()
    except KeyboardInterrupt:
        print("\n⚠️ Đã dừng crawl theo yêu cầu của người dùng")
    except Exception as e:
        print(f"❌ Lỗi không mong muốn: {str(e)}")
