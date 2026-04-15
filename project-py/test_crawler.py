from advanced_crawler import AdvancedCrawler

def test_static_website():
    """Test crawling trang web tĩnh"""
    print("🔥 Bắt đầu crawl trang web tĩnh...")
    crawler = AdvancedCrawler(
        start_url="https://quotes.toscrape.com",
        max_pages=5,  # Giới hạn 5 trang để test
        max_workers=3,  # Crawl 3 trang song song
        use_selenium=False  # Không cần selenium vì đây là web tĩnh
    )
    
    results = crawler.crawl()
    crawler.save_to_csv("quotes_results.csv")

def test_dynamic_website():
    """Test crawling trang web động (JavaScript)"""
    print("🔥 Bắt đầu crawl trang web động...")
    crawler = AdvancedCrawler(
        start_url="https://quotes.toscrape.com/js",  # Phiên bản JavaScript của trang
        max_pages=5,
        max_workers=2,  # Ít workers hơn vì dùng selenium tốn resource
        use_selenium=True  # Bật selenium để xử lý JavaScript
    )
    
    results = crawler.crawl()
    crawler.save_to_csv("quotes_js_results.csv")

if __name__ == "__main__":
    # Test crawl web tĩnh
    test_static_website()
    
    # Test crawl web động
    test_dynamic_website()
