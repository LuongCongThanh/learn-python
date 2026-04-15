import http.server
import socketserver
import os

def start_server(directory, port=8000):
    """Khởi động một HTTP server đơn giản"""
    
    # Chuyển đến thư mục chứa file
    os.chdir(directory)
    
    # Tạo handler
    handler = http.server.SimpleHTTPRequestHandler
    
    # Tạo server
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"🚀 Server đang chạy tại http://localhost:{port}")
        print("📂 Phục vụ files từ thư mục:", directory)
        print("🛑 Nhấn Ctrl+C để dừng server")
        
        # Chạy server
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n⚡ Đã dừng server")

if __name__ == "__main__":
    # Đường dẫn đến thư mục chứa file HTML
    directory = "E:/my-pj/learn-python/project-py/crawled_sites/thanhnien.vn"
    
    # Khởi động server
    start_server(directory)
