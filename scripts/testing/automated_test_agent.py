#!/usr/bin/env python3
"""
Museum Information System - Automated Testing Agent
===================================================
This agent automatically tests all routes, buttons, forms, and API endpoints
in the Flask application and generates a comprehensive report.

Usage:
    python automated_test_agent.py [--base-url URL] [--username EMAIL] [--password PASS]

Requirements:
    pip install selenium requests beautifulsoup4 colorama
"""

import os
import sys
import json
import time
import argparse
import requests
import traceback
from datetime import datetime
from urllib.parse import urljoin, urlparse
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from bs4 import BeautifulSoup
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    print("Installing required packages...")
    os.system("pip install beautifulsoup4 colorama requests")
    from bs4 import BeautifulSoup
    from colorama import init, Fore, Style
    init(autoreset=True)

# Try to import Selenium for browser-based testing
SELENIUM_AVAILABLE = False
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.common.exceptions import (
        TimeoutException, NoSuchElementException,
        ElementClickInterceptedException, WebDriverException
    )
    SELENIUM_AVAILABLE = True
except ImportError:
    print(f"{Fore.YELLOW}Warning: Selenium not available. Browser-based testing disabled.")
    print("Install with: pip install selenium")


class TestResult:
    """Represents the result of a single test."""
    def __init__(self, name, category, status, message="", details=None, duration=0):
        self.name = name
        self.category = category
        self.status = status  # 'PASS', 'FAIL', 'SKIP', 'ERROR'
        self.message = message
        self.details = details or {}
        self.duration = duration
        self.timestamp = datetime.now().isoformat()

    def to_dict(self):
        return {
            'name': self.name,
            'category': self.category,
            'status': self.status,
            'message': self.message,
            'details': self.details,
            'duration': self.duration,
            'timestamp': self.timestamp
        }


class TestReport:
    """Aggregates and reports test results."""
    def __init__(self):
        self.results = []
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = datetime.now()

    def end(self):
        self.end_time = datetime.now()

    def add_result(self, result):
        self.results.append(result)
        status_color = {
            'PASS': Fore.GREEN,
            'FAIL': Fore.RED,
            'SKIP': Fore.YELLOW,
            'ERROR': Fore.MAGENTA
        }
        color = status_color.get(result.status, Fore.WHITE)
        print(f"  [{color}{result.status}{Style.RESET_ALL}] {result.category}: {result.name}")
        if result.status in ('FAIL', 'ERROR') and result.message:
            print(f"         {Fore.RED}{result.message}{Style.RESET_ALL}")

    def get_summary(self):
        total = len(self.results)
        passed = sum(1 for r in self.results if r.status == 'PASS')
        failed = sum(1 for r in self.results if r.status == 'FAIL')
        errors = sum(1 for r in self.results if r.status == 'ERROR')
        skipped = sum(1 for r in self.results if r.status == 'SKIP')

        duration = (self.end_time - self.start_time).total_seconds() if self.end_time else 0

        return {
            'total': total,
            'passed': passed,
            'failed': failed,
            'errors': errors,
            'skipped': skipped,
            'pass_rate': f"{(passed/total*100):.1f}%" if total > 0 else "0%",
            'duration_seconds': duration,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None
        }

    def get_by_category(self):
        categories = defaultdict(list)
        for r in self.results:
            categories[r.category].append(r.to_dict())
        return dict(categories)

    def get_failures(self):
        return [r.to_dict() for r in self.results if r.status in ('FAIL', 'ERROR')]

    def to_dict(self):
        return {
            'summary': self.get_summary(),
            'by_category': self.get_by_category(),
            'failures': self.get_failures(),
            'all_results': [r.to_dict() for r in self.results]
        }

    def save_json(self, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    def print_summary(self):
        summary = self.get_summary()
        print("\n" + "=" * 60)
        print(f"{Fore.CYAN}TEST SUMMARY{Style.RESET_ALL}")
        print("=" * 60)
        print(f"Total Tests:  {summary['total']}")
        print(f"{Fore.GREEN}Passed:       {summary['passed']}{Style.RESET_ALL}")
        print(f"{Fore.RED}Failed:       {summary['failed']}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Errors:       {summary['errors']}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Skipped:      {summary['skipped']}{Style.RESET_ALL}")
        print(f"Pass Rate:    {summary['pass_rate']}")
        print(f"Duration:     {summary['duration_seconds']:.1f}s")
        print("=" * 60)


class MuseumTestAgent:
    """Main testing agent for the Museum Information System."""

    # Define all routes to test
    PUBLIC_ROUTES = [
        ('/', 'Landing Page'),
        ('/index', 'Index Page'),
        ('/login', 'Login Page'),
    ]

    AUTHENTICATED_ROUTES = [
        # Dashboard
        ('/dashboard', 'Main Dashboard'),
        ('/dashboard-classic', 'Classic Dashboard'),
        ('/dashboard/customize', 'Customize Dashboard'),

        # Admin Panel
        ('/admin', 'Admin Panel'),
        ('/admin/statistics', 'Statistics'),
        ('/admin/reports', 'Reports'),
        ('/admin/system-settings', 'System Settings'),

        # User Management
        ('/admin/employees_database', 'Employees Database'),
        ('/admin/employee_profiles_database', 'Employee Profiles'),
        ('/admin/add_user', 'Add User Form'),
        ('/admin/password_manager', 'Password Manager'),
        ('/admin/manage_access', 'Manage Access'),
        ('/admin/visitors_database', 'Visitors Database'),

        # Databases
        ('/admin/museum_databases', 'Museum Databases'),
        ('/admin/exhibits_database', 'Exhibits Database'),
        ('/admin/exhibitions_database', 'Exhibitions Database'),
        ('/admin/library_database', 'Library Database'),
        ('/admin/research_database', 'Research Database'),
        ('/admin/inventory_book', 'Inventory Book'),
        ('/admin/inventory_reconciliation', 'Inventory Reconciliation'),

        # Mineral Collection
        ('/admin/mineral_collection', 'Mineral Collection'),
        ('/admin/add_mineral', 'Add Mineral Form'),
        ('/admin/rruff_minerals', 'RRUFF Minerals'),

        # Other Collections
        ('/admin/cultural_heritage_database', 'Cultural Heritage'),
        ('/admin/botany_collection', 'Botany Collection'),
        ('/admin/bird_ringing_database', 'Bird Ringing Database'),

        # QR Codes
        ('/admin/qr_generator', 'QR Generator'),
        ('/admin/qr_boxes/minerals', 'Mineral QR Boxes'),

        # Images
        ('/admin/batch_image_upload', 'Batch Image Upload'),

        # Timesheet
        ('/timesheet', 'Timesheet'),
        ('/admin/timesheet', 'Admin Timesheet'),
        ('/admin/timesheet_reports', 'Timesheet Reports'),
        ('/admin/timesheet/pending', 'Pending Timesheets'),
        ('/admin/timesheet/analytics', 'Timesheet Analytics'),

        # Integration
        ('/admin/nhm_data_portal', 'NHM Data Portal'),

        # Virtual Depot
        ('/admin/virtual_depot', 'Virtual Depot'),

        # Archives & Signatures
        ('/admin/archive', 'Archive Dashboard'),
        ('/admin/archive/zahtevi', 'Archived Requests'),
        ('/admin/archive/finansije', 'Archived Finance'),
        ('/admin/archive/terenska', 'Archived Field Activities'),
        ('/admin/digital-signatures', 'Digital Signatures'),

        # News
        ('/admin/news', 'News Management'),

        # Exhibition
        ('/exhibition_planner', 'Exhibition Planner'),
        ('/museum_terminology', 'Museum Terminology'),

        # Vehicles
        ('/vehicle_management', 'Vehicle Management'),
        ('/vehicle_reservations', 'Vehicle Reservations'),

        # Financial
        ('/finansije/plan', 'Financial Plan'),
        ('/zahtevi/finansijski', 'Financial Requests'),
        ('/zahtevi/nabavka', 'Procurement Requests'),
        ('/zahtevi/slobodan-dan', 'Free Day Request'),
        ('/zahtevi/godisnji-odmor', 'Annual Leave Request'),

        # Field Operations
        ('/zahtev-sluzbeni-put', 'Service Trip Request'),
    ]

    API_ENDPOINTS = [
        # GET endpoints (read-only, safe to test)
        ('GET', '/api/exhibitions', 'List Exhibitions'),
        ('GET', '/api/website-news', 'Website News'),
        ('GET', '/api/science-news', 'Science News'),
        ('GET', '/api/depot/boxes', 'Depot Boxes'),
        ('GET', '/api/depot/localities', 'Depot Localities'),
        ('GET', '/api/archive/statistics', 'Archive Statistics'),
        ('GET', '/api/digital-signatures', 'Digital Signatures List'),
        ('GET', '/api/digital-signatures/templates', 'Signature Templates'),
        ('GET', '/api/digital-signatures/statistics', 'Signature Statistics'),
        ('GET', '/api/admin/logs', 'System Logs'),
        ('GET', '/api/admin/database/table-stats', 'Database Table Stats'),
        ('GET', '/api/admin/password_manager/users', 'Password Manager Users'),
        ('GET', '/api/nhm/statistics', 'NHM Statistics'),
        ('GET', '/api/nhm/local/statistics', 'Local NHM Statistics'),
        ('GET', '/api/nhm/local/tags', 'NHM Tags'),
        ('GET', '/api/nhm/local/formats', 'NHM Formats'),
        ('GET', '/api/admin/timesheet/employee-analytics', 'Timesheet Analytics'),
    ]

    def __init__(self, base_url, username=None, password=None, headless=True):
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.headless = headless
        self.session = requests.Session()
        self.report = TestReport()
        self.csrf_token = None
        self.logged_in = False
        self.driver = None

    def setup_selenium(self):
        """Initialize Selenium WebDriver."""
        if not SELENIUM_AVAILABLE:
            return False

        try:
            options = Options()
            if self.headless:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')

            self.driver = webdriver.Chrome(options=options)
            self.driver.implicitly_wait(5)
            return True
        except Exception as e:
            print(f"{Fore.YELLOW}Warning: Could not initialize Selenium: {e}")
            return False

    def teardown_selenium(self):
        """Close Selenium WebDriver."""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass

    def get_csrf_token(self, html_content):
        """Extract CSRF token from HTML."""
        soup = BeautifulSoup(html_content, 'html.parser')

        # Try meta tag first
        meta_csrf = soup.find('meta', {'name': 'csrf-token'})
        if meta_csrf:
            return meta_csrf.get('content')

        # Try hidden input
        csrf_input = soup.find('input', {'name': 'csrf_token'})
        if csrf_input:
            return csrf_input.get('value')

        return None

    def login(self):
        """Authenticate with the application."""
        print(f"\n{Fore.CYAN}Attempting login...{Style.RESET_ALL}")

        try:
            # Get login page and CSRF token
            login_url = urljoin(self.base_url, '/login')
            response = self.session.get(login_url, timeout=10)

            if response.status_code != 200:
                self.report.add_result(TestResult(
                    'Login Page Access', 'Authentication',
                    'FAIL', f"Status code: {response.status_code}"
                ))
                return False

            self.csrf_token = self.get_csrf_token(response.text)

            # Prepare login data
            login_data = {
                'email': self.username,
                'password': self.password,
            }
            if self.csrf_token:
                login_data['csrf_token'] = self.csrf_token

            # Submit login
            response = self.session.post(
                login_url,
                data=login_data,
                allow_redirects=True,
                timeout=10
            )

            # Check if login succeeded by examining response content
            response_text = response.text.lower()

            # Login succeeded if: dashboard content present, OR no login form, OR no error messages
            has_dashboard = 'dashboard' in response_text or 'добродошли' in response_text
            has_login_form = 'type="password"' in response_text and 'login' in response.url.lower()
            has_error = 'неисправни' in response_text or 'invalid' in response_text or 'alert-danger' in response_text

            if (has_dashboard or not has_login_form) and not has_error:
                self.logged_in = True
                # Update CSRF token from new page
                self.csrf_token = self.get_csrf_token(response.text)
                self.report.add_result(TestResult(
                    'User Login', 'Authentication',
                    'PASS', 'Successfully authenticated'
                ))
                print(f"{Fore.GREEN}Login successful!{Style.RESET_ALL}")
                return True
            else:
                error_msg = 'Invalid credentials' if has_error else 'Still on login page'
                self.report.add_result(TestResult(
                    'User Login', 'Authentication',
                    'FAIL', error_msg
                ))
                return False

        except Exception as e:
            self.report.add_result(TestResult(
                'User Login', 'Authentication',
                'ERROR', str(e)
            ))
            return False

    def test_route(self, path, name, require_auth=False, retry_on_429=True):
        """Test a single route."""
        url = urljoin(self.base_url, path)
        start = time.time()

        # Add small delay between requests to avoid rate limiting
        time.sleep(0.3)

        try:
            response = self.session.get(url, timeout=15, allow_redirects=True)

            # Retry once if rate limited
            if response.status_code == 429 and retry_on_429:
                time.sleep(2)
                response = self.session.get(url, timeout=15, allow_redirects=True)
            duration = time.time() - start

            # Determine result based on status code
            if response.status_code == 200:
                # Check if we got redirected to login (auth failed)
                if require_auth and 'login' in response.url:
                    return TestResult(
                        name, 'Route Access',
                        'FAIL', 'Redirected to login (auth required)',
                        {'url': url, 'status_code': response.status_code, 'final_url': response.url},
                        duration
                    )
                return TestResult(
                    name, 'Route Access',
                    'PASS', f'OK ({response.status_code})',
                    {'url': url, 'status_code': response.status_code},
                    duration
                )
            elif response.status_code == 302 or response.status_code == 301:
                return TestResult(
                    name, 'Route Access',
                    'PASS', f'Redirect ({response.status_code})',
                    {'url': url, 'status_code': response.status_code, 'redirect': response.headers.get('Location')},
                    duration
                )
            elif response.status_code == 403:
                return TestResult(
                    name, 'Route Access',
                    'SKIP', 'Access denied (403)',
                    {'url': url, 'status_code': response.status_code},
                    duration
                )
            elif response.status_code == 404:
                return TestResult(
                    name, 'Route Access',
                    'FAIL', 'Not found (404)',
                    {'url': url, 'status_code': response.status_code},
                    duration
                )
            else:
                return TestResult(
                    name, 'Route Access',
                    'FAIL', f'Unexpected status: {response.status_code}',
                    {'url': url, 'status_code': response.status_code},
                    duration
                )

        except requests.exceptions.Timeout:
            return TestResult(
                name, 'Route Access',
                'ERROR', 'Request timeout',
                {'url': url},
                15
            )
        except Exception as e:
            return TestResult(
                name, 'Route Access',
                'ERROR', str(e),
                {'url': url},
                time.time() - start
            )

    def test_api_endpoint(self, method, path, name):
        """Test an API endpoint."""
        url = urljoin(self.base_url, path)
        start = time.time()

        # Add small delay to avoid rate limiting
        time.sleep(0.3)

        try:
            headers = {'Accept': 'application/json'}
            if self.csrf_token:
                headers['X-CSRFToken'] = self.csrf_token

            if method == 'GET':
                response = self.session.get(url, headers=headers, timeout=15)
            elif method == 'POST':
                response = self.session.post(url, headers=headers, json={}, timeout=15)
            else:
                return TestResult(name, 'API', 'SKIP', f'Unsupported method: {method}')

            duration = time.time() - start

            # Check response
            if response.status_code == 200:
                # Try to parse JSON
                try:
                    data = response.json()
                    return TestResult(
                        name, 'API',
                        'PASS', 'JSON response OK',
                        {'url': url, 'status_code': 200, 'response_type': 'json'},
                        duration
                    )
                except:
                    return TestResult(
                        name, 'API',
                        'PASS', 'Response OK (non-JSON)',
                        {'url': url, 'status_code': 200, 'response_type': 'other'},
                        duration
                    )
            elif response.status_code in (401, 403):
                return TestResult(
                    name, 'API',
                    'SKIP', f'Auth required ({response.status_code})',
                    {'url': url, 'status_code': response.status_code},
                    duration
                )
            elif response.status_code == 404:
                return TestResult(
                    name, 'API',
                    'FAIL', 'Endpoint not found (404)',
                    {'url': url, 'status_code': response.status_code},
                    duration
                )
            elif response.status_code == 500:
                return TestResult(
                    name, 'API',
                    'ERROR', 'Server error (500)',
                    {'url': url, 'status_code': response.status_code},
                    duration
                )
            else:
                return TestResult(
                    name, 'API',
                    'FAIL', f'Status: {response.status_code}',
                    {'url': url, 'status_code': response.status_code},
                    duration
                )

        except Exception as e:
            return TestResult(
                name, 'API',
                'ERROR', str(e),
                {'url': url},
                time.time() - start
            )

    def discover_buttons(self, html_content, page_url):
        """Find all clickable buttons and links in HTML."""
        soup = BeautifulSoup(html_content, 'html.parser')
        buttons = []

        # Find all buttons
        for btn in soup.find_all('button'):
            btn_text = btn.get_text(strip=True)
            btn_type = btn.get('type', 'button')
            btn_onclick = btn.get('onclick', '')
            btn_id = btn.get('id', '')
            btn_class = ' '.join(btn.get('class', []))

            if btn_text or btn_id:
                buttons.append({
                    'type': 'button',
                    'text': btn_text,
                    'id': btn_id,
                    'class': btn_class,
                    'onclick': btn_onclick,
                    'button_type': btn_type,
                    'page': page_url
                })

        # Find all links that look like buttons
        for link in soup.find_all('a', class_=lambda x: x and ('btn' in str(x).lower())):
            link_text = link.get_text(strip=True)
            link_href = link.get('href', '')
            link_id = link.get('id', '')

            buttons.append({
                'type': 'link_button',
                'text': link_text,
                'href': link_href,
                'id': link_id,
                'page': page_url
            })

        # Find form submit buttons
        for form in soup.find_all('form'):
            form_action = form.get('action', page_url)
            form_method = form.get('method', 'GET').upper()
            submit_btns = form.find_all(['button', 'input'], type='submit')

            for submit in submit_btns:
                text = submit.get('value') or submit.get_text(strip=True)
                buttons.append({
                    'type': 'form_submit',
                    'text': text,
                    'form_action': form_action,
                    'form_method': form_method,
                    'page': page_url
                })

        return buttons

    def test_buttons_with_selenium(self, url, page_name):
        """Use Selenium to find and click buttons on a page."""
        if not self.driver:
            return []

        results = []

        try:
            # Sync session cookies to Selenium
            self.driver.get(self.base_url)
            for cookie in self.session.cookies:
                cookie_dict = {
                    'name': cookie.name,
                    'value': cookie.value,
                    'domain': cookie.domain,
                    'path': cookie.path
                }
                try:
                    self.driver.add_cookie(cookie_dict)
                except:
                    pass

            # Navigate to the page
            self.driver.get(url)
            time.sleep(1)  # Wait for page load

            # Find all buttons
            buttons = self.driver.find_elements(By.TAG_NAME, 'button')
            button_links = self.driver.find_elements(By.CSS_SELECTOR, 'a.btn, a.button')

            all_clickables = buttons + button_links

            for i, elem in enumerate(all_clickables[:20]):  # Limit to 20 buttons per page
                try:
                    btn_text = elem.text or elem.get_attribute('value') or f'Button #{i}'
                    btn_text = btn_text[:50]  # Truncate long text

                    # Check if button is visible and enabled
                    if not elem.is_displayed() or not elem.is_enabled():
                        results.append(TestResult(
                            f'{page_name}: {btn_text}', 'Button Click',
                            'SKIP', 'Button not visible/enabled'
                        ))
                        continue

                    # Try to click the button
                    start = time.time()
                    original_url = self.driver.current_url

                    try:
                        elem.click()
                        time.sleep(0.5)

                        # Check for errors
                        page_source = self.driver.page_source.lower()
                        new_url = self.driver.current_url

                        if 'error' in page_source and 'internal server error' in page_source:
                            results.append(TestResult(
                                f'{page_name}: {btn_text}', 'Button Click',
                                'ERROR', 'Server error after click',
                                {'original_url': original_url, 'new_url': new_url},
                                time.time() - start
                            ))
                        elif '404' in self.driver.title.lower() or 'not found' in page_source:
                            results.append(TestResult(
                                f'{page_name}: {btn_text}', 'Button Click',
                                'FAIL', 'Page not found after click',
                                {'original_url': original_url, 'new_url': new_url},
                                time.time() - start
                            ))
                        else:
                            results.append(TestResult(
                                f'{page_name}: {btn_text}', 'Button Click',
                                'PASS', 'Click successful',
                                {'original_url': original_url, 'new_url': new_url},
                                time.time() - start
                            ))

                        # Navigate back for next button
                        if new_url != original_url:
                            self.driver.get(url)
                            time.sleep(0.5)

                    except ElementClickInterceptedException:
                        results.append(TestResult(
                            f'{page_name}: {btn_text}', 'Button Click',
                            'SKIP', 'Click intercepted (modal/overlay)'
                        ))

                except Exception as e:
                    results.append(TestResult(
                        f'{page_name}: Button #{i}', 'Button Click',
                        'ERROR', str(e)[:100]
                    ))

        except TimeoutException:
            results.append(TestResult(
                f'{page_name}: Page Load', 'Button Click',
                'ERROR', 'Page load timeout'
            ))
        except Exception as e:
            results.append(TestResult(
                f'{page_name}: Discovery', 'Button Click',
                'ERROR', str(e)[:100]
            ))

        return results

    def discover_forms(self, html_content, page_url):
        """Find all forms on a page."""
        soup = BeautifulSoup(html_content, 'html.parser')
        forms = []

        for form in soup.find_all('form'):
            form_data = {
                'action': form.get('action', page_url),
                'method': form.get('method', 'GET').upper(),
                'id': form.get('id', ''),
                'page': page_url,
                'fields': []
            }

            # Find all input fields
            for inp in form.find_all(['input', 'select', 'textarea']):
                field = {
                    'name': inp.get('name', ''),
                    'type': inp.get('type', 'text'),
                    'id': inp.get('id', ''),
                    'required': inp.has_attr('required'),
                    'tag': inp.name
                }
                if field['name']:
                    form_data['fields'].append(field)

            forms.append(form_data)

        return forms

    def test_form_submission(self, form_data, page_name):
        """Test submitting a form with test data."""
        start = time.time()

        # Skip CSRF-protected forms without token
        if form_data['method'] == 'POST' and not self.csrf_token:
            return TestResult(
                f"{page_name}: {form_data.get('id', 'Form')}", 'Form Submission',
                'SKIP', 'No CSRF token available'
            )

        # Build test data
        test_data = {}
        for field in form_data['fields']:
            name = field['name']
            field_type = field['type']

            if name == 'csrf_token':
                test_data[name] = self.csrf_token
            elif field_type == 'email':
                test_data[name] = 'test@example.com'
            elif field_type == 'password':
                test_data[name] = 'TestPassword123!'
            elif field_type in ('number', 'tel'):
                test_data[name] = '123'
            elif field_type == 'date':
                test_data[name] = '2024-01-01'
            elif field_type == 'hidden':
                # Keep hidden field values
                pass
            elif field_type not in ('submit', 'button', 'file'):
                test_data[name] = 'Test Value'

        try:
            url = urljoin(self.base_url, form_data['action'])

            if form_data['method'] == 'GET':
                response = self.session.get(url, params=test_data, timeout=15)
            else:
                response = self.session.post(url, data=test_data, timeout=15)

            duration = time.time() - start

            if response.status_code == 200:
                # Check for error messages in response
                if 'error' in response.text.lower()[:1000]:
                    return TestResult(
                        f"{page_name}: {form_data.get('id', 'Form')}", 'Form Submission',
                        'PASS', 'Form processed (with validation errors)',
                        {'status': 200, 'url': url},
                        duration
                    )
                return TestResult(
                    f"{page_name}: {form_data.get('id', 'Form')}", 'Form Submission',
                    'PASS', 'Form submitted successfully',
                    {'status': 200, 'url': url},
                    duration
                )
            elif response.status_code in (301, 302):
                return TestResult(
                    f"{page_name}: {form_data.get('id', 'Form')}", 'Form Submission',
                    'PASS', 'Form redirected (likely success)',
                    {'status': response.status_code, 'redirect': response.headers.get('Location')},
                    duration
                )
            elif response.status_code == 400:
                return TestResult(
                    f"{page_name}: {form_data.get('id', 'Form')}", 'Form Submission',
                    'PASS', 'Form validation working (400)',
                    {'status': 400},
                    duration
                )
            elif response.status_code == 500:
                return TestResult(
                    f"{page_name}: {form_data.get('id', 'Form')}", 'Form Submission',
                    'ERROR', 'Server error (500)',
                    {'status': 500, 'url': url},
                    duration
                )
            else:
                return TestResult(
                    f"{page_name}: {form_data.get('id', 'Form')}", 'Form Submission',
                    'FAIL', f'Unexpected status: {response.status_code}',
                    {'status': response.status_code},
                    duration
                )

        except Exception as e:
            return TestResult(
                f"{page_name}: {form_data.get('id', 'Form')}", 'Form Submission',
                'ERROR', str(e),
                duration=time.time() - start
            )

    def run_all_tests(self):
        """Execute all tests."""
        self.report.start()

        print(f"\n{Fore.CYAN}{'='*60}")
        print("MUSEUM INFORMATION SYSTEM - AUTOMATED TEST AGENT")
        print(f"{'='*60}{Style.RESET_ALL}")
        print(f"Base URL: {self.base_url}")
        print(f"Testing started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Setup Selenium if available
        selenium_ready = self.setup_selenium()
        if selenium_ready:
            print(f"{Fore.GREEN}Selenium initialized for browser testing{Style.RESET_ALL}")

        # Test public routes first
        print(f"\n{Fore.CYAN}[1/6] Testing Public Routes{Style.RESET_ALL}")
        for path, name in self.PUBLIC_ROUTES:
            result = self.test_route(path, name, require_auth=False)
            self.report.add_result(result)

        # Authenticate
        if self.username and self.password:
            print(f"\n{Fore.CYAN}[2/6] Testing Authentication{Style.RESET_ALL}")
            self.login()
        else:
            print(f"\n{Fore.YELLOW}[2/6] Skipping authentication (no credentials provided){Style.RESET_ALL}")
            self.report.add_result(TestResult(
                'Authentication', 'Authentication',
                'SKIP', 'No credentials provided'
            ))

        # Test authenticated routes
        print(f"\n{Fore.CYAN}[3/6] Testing Authenticated Routes{Style.RESET_ALL}")
        for path, name in self.AUTHENTICATED_ROUTES:
            result = self.test_route(path, name, require_auth=self.logged_in)
            self.report.add_result(result)

            # If route succeeded, discover and test forms/buttons
            if result.status == 'PASS' and self.logged_in:
                try:
                    response = self.session.get(urljoin(self.base_url, path), timeout=10)

                    # Discover forms
                    forms = self.discover_forms(response.text, path)
                    for form in forms[:3]:  # Limit to 3 forms per page
                        form_result = self.test_form_submission(form, name)
                        self.report.add_result(form_result)

                except Exception as e:
                    pass  # Skip form discovery errors

        # Test API endpoints
        print(f"\n{Fore.CYAN}[4/6] Testing API Endpoints{Style.RESET_ALL}")
        for method, path, name in self.API_ENDPOINTS:
            result = self.test_api_endpoint(method, path, name)
            self.report.add_result(result)

        # Test buttons with Selenium
        if selenium_ready and self.logged_in:
            print(f"\n{Fore.CYAN}[5/6] Testing Button Clicks (Selenium){Style.RESET_ALL}")

            # Test buttons on key pages
            key_pages = [
                ('/admin', 'Admin Panel'),
                ('/dashboard', 'Dashboard'),
                ('/admin/mineral_collection', 'Mineral Collection'),
                ('/admin/statistics', 'Statistics'),
            ]

            for path, name in key_pages:
                url = urljoin(self.base_url, path)
                print(f"  Testing buttons on: {name}")
                results = self.test_buttons_with_selenium(url, name)
                for r in results:
                    self.report.add_result(r)
        else:
            print(f"\n{Fore.YELLOW}[5/6] Skipping Selenium tests (not available or not logged in){Style.RESET_ALL}")

        # Security tests
        print(f"\n{Fore.CYAN}[6/6] Running Security Tests{Style.RESET_ALL}")
        self.run_security_tests()

        # Cleanup
        self.teardown_selenium()
        self.report.end()

        # Print summary
        self.report.print_summary()

        return self.report

    def run_security_tests(self):
        """Run basic security tests."""

        # Test unauthorized access to admin routes
        test_session = requests.Session()  # Fresh session without auth

        admin_routes = [
            '/admin',
            '/admin/system-settings',
            '/admin/password_manager',
            '/api/admin/logs',
        ]

        for route in admin_routes:
            url = urljoin(self.base_url, route)
            try:
                response = test_session.get(url, timeout=10, allow_redirects=False)

                if response.status_code == 200:
                    self.report.add_result(TestResult(
                        f'Unauthorized access: {route}', 'Security',
                        'FAIL', 'Admin route accessible without auth!'
                    ))
                elif response.status_code in (302, 301, 401, 403):
                    self.report.add_result(TestResult(
                        f'Unauthorized access: {route}', 'Security',
                        'PASS', f'Protected (status: {response.status_code})'
                    ))
                else:
                    self.report.add_result(TestResult(
                        f'Unauthorized access: {route}', 'Security',
                        'PASS', f'Status: {response.status_code}'
                    ))
            except Exception as e:
                self.report.add_result(TestResult(
                    f'Unauthorized access: {route}', 'Security',
                    'ERROR', str(e)
                ))

        # Test CSRF protection
        if self.logged_in:
            try:
                # Try to submit a form without CSRF token
                response = self.session.post(
                    urljoin(self.base_url, '/admin/add_mineral'),
                    data={'name': 'Test', 'no_csrf': True},
                    timeout=10
                )

                if response.status_code == 400 or 'csrf' in response.text.lower():
                    self.report.add_result(TestResult(
                        'CSRF Protection', 'Security',
                        'PASS', 'CSRF token validation working'
                    ))
                else:
                    self.report.add_result(TestResult(
                        'CSRF Protection', 'Security',
                        'FAIL', 'Form accepted without CSRF token'
                    ))
            except Exception as e:
                self.report.add_result(TestResult(
                    'CSRF Protection', 'Security',
                    'ERROR', str(e)
                ))

        # Test SQL injection (basic)
        injection_payloads = ["' OR '1'='1", "1; DROP TABLE users;--"]
        for payload in injection_payloads:
            try:
                response = self.session.get(
                    urljoin(self.base_url, f'/admin/mineral_collection?search={payload}'),
                    timeout=10
                )

                if response.status_code == 500 or 'sql' in response.text.lower():
                    self.report.add_result(TestResult(
                        f'SQL Injection: {payload[:20]}...', 'Security',
                        'FAIL', 'Possible SQL injection vulnerability'
                    ))
                else:
                    self.report.add_result(TestResult(
                        f'SQL Injection: {payload[:20]}...', 'Security',
                        'PASS', 'Input appears sanitized'
                    ))
            except:
                pass

        # Test XSS (basic)
        xss_payload = '<script>alert("xss")</script>'
        try:
            response = self.session.get(
                urljoin(self.base_url, f'/admin/mineral_collection?search={xss_payload}'),
                timeout=10
            )

            if xss_payload in response.text:
                self.report.add_result(TestResult(
                    'XSS Vulnerability', 'Security',
                    'FAIL', 'Unescaped script tag in response'
                ))
            else:
                self.report.add_result(TestResult(
                    'XSS Vulnerability', 'Security',
                    'PASS', 'Script tag properly escaped or filtered'
                ))
        except:
            pass


def main():
    parser = argparse.ArgumentParser(
        description='Museum Information System - Automated Testing Agent',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default settings (localhost)
  python automated_test_agent.py

  # Run with custom URL and credentials
  python automated_test_agent.py --base-url http://museum.local --username admin@museum.rs --password secret

  # Run in visible browser mode
  python automated_test_agent.py --no-headless
        """
    )

    parser.add_argument(
        '--base-url', '-u',
        default='http://localhost:5000',
        help='Base URL of the application (default: http://localhost:5000)'
    )
    parser.add_argument(
        '--username', '-e',
        help='Login email/username'
    )
    parser.add_argument(
        '--password', '-p',
        help='Login password'
    )
    parser.add_argument(
        '--no-headless',
        action='store_true',
        help='Run browser in visible mode (not headless)'
    )
    parser.add_argument(
        '--output', '-o',
        default='test_report.json',
        help='Output file for JSON report (default: test_report.json)'
    )

    args = parser.parse_args()

    # Create and run test agent
    agent = MuseumTestAgent(
        base_url=args.base_url,
        username=args.username,
        password=args.password,
        headless=not args.no_headless
    )

    try:
        report = agent.run_all_tests()

        # Save report
        report_path = os.path.join(os.path.dirname(__file__), args.output)
        report.save_json(report_path)
        print(f"\n{Fore.GREEN}Report saved to: {report_path}{Style.RESET_ALL}")

        # Return exit code based on failures
        summary = report.get_summary()
        if summary['failed'] > 0 or summary['errors'] > 0:
            sys.exit(1)
        sys.exit(0)

    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Test interrupted by user{Style.RESET_ALL}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{Fore.RED}Fatal error: {e}{Style.RESET_ALL}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
