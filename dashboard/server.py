#!/usr/bin/env python3
"""Simple HTTP server for dashboard with proper file handling."""
from http.server import SimpleHTTPRequestHandler, HTTPServer
import os
import json

class DashboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
    
        self.dashboard_dir = '/app/dashboard'
        self.results_dir = '/app/results'
        super().__init__(*args, directory=self.dashboard_dir, **kwargs)
    
    def do_GET(self):
        print(f" Requête reçue: {self.path}")
        
    
        if self.path == '/' or self.path == '':
            self.path = '/index.html'
        
        
        elif self.path == '/analysis.json' or self.path == '/results/analysis.json':
            try:
                with open('/app/results/analysis.json', 'r') as f:
                    data = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(data.encode())
                return
            except FileNotFoundError:
                self.send_error(404, "analysis.json not found")
                return
        
        
        try:
            return super().do_GET()
        except Exception as e:
            self.send_error(404, f"File not found: {self.path}")
    
    def log_message(self, format, *args):
        print(f"[DASHBOARD] {self.client_address[0]} - {format % args}")

def main():
    port = 8081
    
    print("=" * 60)
    print(" Démarrage du serveur Dashboard...")
    print(f" Dashboard directory: /app/dashboard")
    print(f"Results directory: /app/results")
    
    if os.path.exists('/app/dashboard'):
        print("Dashboard directory exists")
        print(f"   Contenu: {os.listdir('/app/dashboard')}")
    else:
        print(" Dashboard directory NOT FOUND")
    
    if os.path.exists('/app/results'):
        print(" Results directory exists")
        print(f"   Contenu: {os.listdir('/app/results')}")
    else:
        print("Results directory NOT FOUND")
    
    print(f"Serveur démarré sur: http://localhost:{port}")
    print("=" * 60)
    
    with HTTPServer(('0.0.0.0', port), DashboardHandler) as httpd:
        httpd.serve_forever()

if __name__ == '__main__':
    main()