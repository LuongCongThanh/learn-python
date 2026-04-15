from advanced_crawler import AdvancedCrawler
from bs4 import BeautifulSoup
import time
import random

class ThanhNienCrawler(AdvancedCrawler):
    """Crawler được tối ưu cho trang Thanh Niên"""
    
    def get_internal_links(self, html, base_url):
        """Lọc các link theo các chuyên mục quan trọng"""
        links = super().get_internal_links(html, base_url)
        filtered_links = set()
        
        # Chỉ lấy các link thuộc các chuyên mục chính
        important_sections = [
            "/thoi-su",
            "/the-gioi",
            "/kinh-te",
            "/giao-duc",
            "/doi-song",
            "/van-hoa",
            "/the-thao",
            "/cong-nghe"
        ]
        
        for link in links:
            if any(section in link for section in important_sections):
                filtered_links.add(link)
        
        return filtered_links

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
        time.sleep(random.uniform(1, 2))
        
        return data, new_links

def crawl_thanhnien():
    target_url = "https://thanhnien.vn"
    
    print(f"🔥 Bắt đầu crawl Thanh Niên từ: {target_url}")
    print("ℹ️  Chỉ crawl các chuyên mục chính và bài viết mới")
    
    crawler = ThanhNienCrawler(
        start_url=target_url,
        max_pages=20,  # Tăng số trang để lấy nhiều bài hơn
        max_workers=2,  # Giữ 2 luồng để tránh bị block
        use_selenium=True
    )
    
    print("⏳ Đang crawl dữ liệu, quá trình này có thể mất vài phút...")
    crawler.crawl()
    
    output_file = "thanhnien_articles.csv"
    crawler.save_to_csv(output_file)
    print(f"✅ Hoàn thành! Đã lưu {len(crawler.data)} bài viết vào {output_file}")

if __name__ == "__main__":
    crawl_thanhnien()
