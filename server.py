from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
import os

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super().end_headers()

    def do_GET(self):
        # Print the requested file path
        print(f"Requested file: {self.path}")
        
        # Check if file exists
        if self.path == '/':
            self.path = '/index.html'
        
        file_path = os.path.join(os.getcwd(), self.path.lstrip('/'))
        print(f"Looking for file at: {file_path}")
        
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            self.send_error(404, "File not found")
            return
        
        print(f"Found file: {file_path}")
        print(f"File size: {os.path.getsize(file_path)} bytes")
        
        # Read and print first few lines of CSV files
        if file_path.endswith('.csv'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print(f"CSV content preview:\n{content[:200]}...")
            except Exception as e:
                print(f"Error reading CSV file: {e}")
            
        return super().do_GET()

def run(server_class=HTTPServer, handler_class=CORSRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print("\n=== Server Started ===")
    print("Server running at http://localhost:8000")
    print("Serving files from:", os.getcwd())
    print("Available files:")
    for file in os.listdir('.'):
        if file.endswith(('.html', '.csv')):
            print(f"- {file}")
    print("===================\n")
    webbrowser.open('http://localhost:8000')
    httpd.serve_forever()

if __name__ == '__main__':
    run() 