#!/usr/bin/env python3
"""
Automatic Credit Reset Script for gaccode.com (Advanced Version with Config File Support)
This script automates the process of creating a credit refill request ticket.
"""

import requests
import json
import time
import os
import sys
import argparse
import smtplib
from datetime import datetime, timezone
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


class CreditResetBot:
    """Bot to automatically reset credits by creating support tickets"""
    
    def __init__(self, config, config_file_path=None):
        """
        Initialize the bot with configuration
        
        Args:
            config: Configuration dictionary
            config_file_path: Path to config file (for saving updated token)
        """
        self.base_url = config.get('base_url', 'https://gaccode.com/api')
        self.auth_token = config.get('auth_token', '')
        self.email = config.get('email')
        self.password = config.get('password')
        self.ticket_config = config.get('ticket_config', {})
        self.retry_config = config.get('retry_config', {})
        self.config = config
        self.config_file_path = config_file_path
        
        # If auth_token is empty or placeholder, we'll try to login later
        # Don't raise error here, allow initialization
        
        self.headers = {
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'authorization': f'Bearer {self.auth_token}',
            'accept-language': self.ticket_config.get('language', 'zh'),
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
            'content-type': 'application/json',
            'accept': '*/*',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
        }
    
    def save_config(self):
        """
        Save current configuration (including updated token) to config file
        
        Returns:
            bool: True if save successful, False otherwise
        """
        if not self.config_file_path:
            print("[WARNING] No config file path provided, cannot save configuration")
            return False
        
        try:
            # Update token in config
            self.config['auth_token'] = self.auth_token
            
            # Save to file with pretty formatting
            with open(self.config_file_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            print(f"[SUCCESS] Configuration saved to {self.config_file_path}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to save configuration: {e}")
            return False
    
    def refresh_token(self, save_to_config=True):
        """
        Refresh authentication token by logging in again
        
        Args:
            save_to_config: Whether to save the new token to config file
        
        Returns:
            bool: True if token refresh successful, False otherwise
        """
        if not self.email or not self.password:
            print("[ERROR] Email and password are required for token refresh")
            print("[INFO] Please provide email and password in configuration")
            return False
        
        url = f"{self.base_url}/login"
        headers = {
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
            'accept': '*/*',
            'origin': 'https://gaccode.com',
            'referer': 'https://gaccode.com/login',
        }
        
        payload = {
            "email": self.email,
            "password": self.password
        }
        
        try:
            print("[INFO] Attempting to login and get authentication token...")
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'token' in data:
                self.auth_token = data['token']
                # Update authorization header
                self.headers['authorization'] = f'Bearer {self.auth_token}'
                print(f"[SUCCESS] Login successful!")
                print(f"[INFO] New token: {self.auth_token[:50]}...")
                
                # Save to config file
                if save_to_config:
                    self.save_config()
                
                # Send token refresh email notification
                self.send_email_alert(
                    "认证Token已刷新",
                    f"登录成功，已自动更新认证token。\n登录时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nToken (前50字符): {self.auth_token[:50]}...",
                    "token_refresh"
                )
                
                return True
            else:
                print(f"[ERROR] No token in response: {data}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to login: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    print(f"[ERROR] Server response: {error_data}")
                except:
                    print(f"[ERROR] Server response: {e.response.text}")
            return False
    
    def check_active_subscription(self):
        """
        Check if user has an active subscription that supports credit refill
        
        Returns:
            tuple: (bool, dict) - (has_active_subscription, subscription_info)
        """
        url = f"{self.base_url}/subscriptions/active"
        headers = self.headers.copy()
        headers['referer'] = 'https://gaccode.com/subscriptions'
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            # Check if token is invalid (401)
            if response.status_code == 401:
                print("[WARNING] Token appears to be invalid (401 Unauthorized)")
                if self.refresh_token():
                    # Retry with new token
                    headers['authorization'] = f'Bearer {self.auth_token}'
                    response = requests.get(url, headers=headers, timeout=10)
                else:
                    return False, None
            
            response.raise_for_status()
            data = response.json()
            
            subscriptions = data.get('subscriptions', [])
            
            if not subscriptions:
                print("[WARNING] No active subscriptions found")
                print("[INFO] Credit refill may not be available without an active subscription")
                return False, None
            
            # Check the first (most recent) subscription
            sub = subscriptions[0]
            sub_info = sub.get('subscription', {})
            
            print(f"[INFO] Active subscription found:")
            print(f"  - Tier: {sub_info.get('tier')}")
            print(f"  - Description: {sub_info.get('description')}")
            print(f"  - Start Date: {sub.get('startDate')}")
            print(f"  - End Date: {sub.get('endDate')}")
            print(f"  - Supports Refill: {sub_info.get('supportsRefill')}")
            
            # Check if subscription supports refill
            if not sub_info.get('supportsRefill', False):
                print("[WARNING] Current subscription does not support credit refill")
                return False, sub_info
            
            # Check if subscription has expired
            end_date_str = sub.get('endDate')
            if end_date_str:
                end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
                current_date = datetime.now(timezone.utc)
                
                if current_date > end_date:
                    print("[WARNING] Subscription has expired")
                    print(f"[INFO] Expired on: {end_date_str}")
                    return False, sub_info
            
            return True, sub_info
            
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to check subscription status: {e}")
            if hasattr(e, 'response') and e.response is not None:
                if e.response.status_code == 401:
                    print("[INFO] Token may be invalid. Try refreshing token.")
            return False, None
    
    def check_today_reset(self):
        """
        Check if credit has been reset today by checking the latest ticket
        
        Returns:
            tuple: (bool, str) - (already_reset_today, created_time)
        """
        url = f"{self.base_url}/tickets?page=1&limit=20"
        headers = self.headers.copy()
        headers['referer'] = 'https://gaccode.com/tickets'
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            tickets = data.get('tickets', [])
            if not tickets:
                print("[INFO] No previous tickets found")
                return False, None
            
            # Get the first (most recent) ticket
            latest_ticket = tickets[0]
            created_at = latest_ticket.get('createdAt')
            
            if not created_at:
                print("[WARNING] Latest ticket has no createdAt field")
                return False, None
            
            # Parse the timestamp (ISO 8601 format with Z for UTC)
            created_datetime = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            current_datetime = datetime.now(timezone.utc)
            
            # Check if the date is the same (ignoring time)
            created_date = created_datetime.date()
            current_date = current_datetime.date()
            
            print(f"[INFO] Latest ticket information:")
            print(f"  - Ticket ID: {latest_ticket.get('id')}")
            print(f"  - Title: {latest_ticket.get('title')}")
            print(f"  - Created at: {created_at}")
            print(f"  - Status: {latest_ticket.get('status')}")
            
            if created_date == current_date:
                return True, created_at
            else:
                return False, created_at
                
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to check tickets: {e}")
            print(f"[WARNING] Cannot verify today's reset status due to network error")
            print(f"[INFO] Aborting to avoid duplicate submission")
            return True, None  # Return True to abort execution
        except (ValueError, AttributeError) as e:
            print(f"[ERROR] Failed to parse date: {e}")
            print(f"[WARNING] Cannot verify today's reset status due to parsing error")
            print(f"[INFO] Proceeding with caution...")
            return False, None  # Data format error, proceed but warn
    
    def check_recaptcha_required(self):
        """
        Check if recaptcha is required for creating tickets
        
        Returns:
            dict: Response containing recaptcha status, ticket count, and daily limit
        """
        url = f"{self.base_url}/tickets/recaptcha-required"
        headers = self.headers.copy()
        headers['referer'] = 'https://gaccode.com/tickets/new'
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            print(f"[INFO] Recaptcha check result:")
            print(f"  - Requires Recaptcha: {data.get('requiresRecaptcha')}")
            print(f"  - Tickets today: {data.get('ticketCountToday')}")
            print(f"  - Daily limit: {data.get('dailyLimit')}")
            return data
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to check recaptcha status: {e}")
            return None
    
    def create_ticket(self):
        """
        Create a credit refill request ticket
        
        Returns:
            dict: Response containing ticket information
        """
        url = f"{self.base_url}/tickets"
        headers = self.headers.copy()
        headers['origin'] = 'https://gaccode.com'
        headers['referer'] = 'https://gaccode.com/tickets/new'
        
        payload = {
            "categoryId": self.ticket_config.get('category_id', 3),
            "title": self.ticket_config.get('title', '重置积分'),
            "description": self.ticket_config.get('description', ''),
            "language": self.ticket_config.get('language', 'zh')
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'ticket' in data:
                ticket = data['ticket']
                print(f"[SUCCESS] Ticket created successfully!")
                print(f"  - Ticket ID: {ticket.get('id')}")
                print(f"  - Title: {ticket.get('title')}")
                print(f"  - Status: {ticket.get('status')}")
                print(f"  - Created at: {ticket.get('createdAt')}")
                
                # Print messages if any
                messages = ticket.get('messages', [])
                if messages:
                    print(f"  - Response message: {messages[0].get('message')}")
                
                return data
            else:
                print(f"[WARNING] Unexpected response format: {data}")
                return data
                
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to create ticket: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    print(f"[ERROR] Server response: {error_data}")
                except:
                    print(f"[ERROR] Server response: {e.response.text}")
            return None
    
    def verify_ticket(self, ticket_id):
        """
        Verify the ticket status
        
        Args:
            ticket_id: ID of the ticket to verify
            
        Returns:
            dict: Ticket information
        """
        url = f"{self.base_url}/tickets/{ticket_id}"
        headers = self.headers.copy()
        headers['referer'] = f'https://gaccode.com/tickets/{ticket_id}'
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'ticket' in data:
                ticket = data['ticket']
                print(f"[INFO] Ticket verification:")
                print(f"  - Ticket ID: {ticket.get('id')}")
                print(f"  - Status: {ticket.get('status')}")
                print(f"  - Updated at: {ticket.get('updatedAt')}")
                
                messages = ticket.get('messages', [])
                if messages:
                    print(f"  - Latest message: {messages[-1].get('message')}")
                
                return data
            else:
                print(f"[WARNING] Unexpected response format: {data}")
                return data
                
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to verify ticket: {e}")
            return None
    
    def get_credit_balance(self):
        """
        Get current credit balance
        
        Returns:
            dict: Credit balance information
        """
        url = f"{self.base_url}/credits/balance"
        headers = self.headers.copy()
        headers['referer'] = 'https://gaccode.com/'
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            print(f"[INFO] Credit balance:")
            print(f"  - Balance: {data.get('balance', 'N/A')}")
            return data
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to get credit balance: {e}")
            return None
    
    def send_email_alert(self, subject, body, alert_type="info"):
        """
        Send email alert notification
        
        Args:
            subject: Email subject
            body: Email body text
            alert_type: Type of alert (info, success, warning, error)
        """
        email_config = self.config.get('email_alerts', {})
        
        # Check if email alerts are enabled
        if not email_config.get('enabled', False):
            return
        
        # Check notification settings based on alert type
        if alert_type == "success" and not email_config.get('on_success', False):
            return
        if alert_type == "error" and not email_config.get('on_failure', True):
            return
        if alert_type == "token_refresh" and not email_config.get('on_token_refresh', True):
            return
        
        # Check required email configuration fields
        required_fields = ['smtp_server', 'smtp_user', 'smtp_password', 'from_email', 'to_email']
        missing_fields = [field for field in required_fields if not email_config.get(field)]
        
        if missing_fields:
            print(f"[WARNING] Email configuration incomplete, missing: {missing_fields}")
            return
        
        try:
            print(f"[INFO] Sending email: {subject}")
            
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = email_config['from_email']
            msg['To'] = email_config['to_email']
            msg['Subject'] = Header(f"[GAC积分重置工具] {subject}", 'utf-8')
            
            # Email body with timestamp
            full_body = f"""
GAC积分重置工具通知

时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
类型: {alert_type}

{body}

---
此邮件由GAC积分重置工具自动发送
配置文件: {self.config_file_path}
"""
            
            msg.attach(MIMEText(full_body, 'plain', 'utf-8'))
            
            # Connect to SMTP server based on port
            smtp_port = email_config.get('smtp_port', 587)
            
            if smtp_port == 465:
                # SSL connection
                server = smtplib.SMTP_SSL(email_config['smtp_server'], smtp_port, timeout=30)
            else:
                # STARTTLS connection (587, 25)
                server = smtplib.SMTP(email_config['smtp_server'], smtp_port, timeout=30)
                server.starttls()
            
            # Login and send
            server.login(email_config['smtp_user'], email_config['smtp_password'])
            server.sendmail(email_config['from_email'], [email_config['to_email']], msg.as_string())
            server.quit()
            
            print(f"[SUCCESS] Email sent successfully: {subject}")
            
        except Exception as e:
            print(f"[ERROR] Failed to send email: {e}")
            import traceback
            print(f"[DEBUG] Email error details: {traceback.format_exc()}")
    
    def run(self, check_balance=False, skip_subscription_check=False):
        """
        Run the complete credit reset process
        
        Args:
            check_balance: Whether to check balance before and after
            skip_subscription_check: Skip subscription check (for testing)
            
        Returns:
            bool: True if successful, False otherwise
        """
        print("=" * 60)
        print(f"Credit Reset Bot - Started at {datetime.now()}")
        print("=" * 60)
        
        # Step -2: Check and initialize auth token
        if not self.auth_token or self.auth_token == 'YOUR_AUTH_TOKEN_HERE':
            print("\n[STEP -2] No valid auth token found, attempting to login...")
            if not self.refresh_token(save_to_config=True):
                print("\n" + "=" * 60)
                print("[ERROR] ❌ Failed to obtain authentication token!")
                print("[INFO] Please check your email and password in configuration.")
                print("=" * 60)
                return False
            print("[INFO] ✓ Authentication token obtained and saved!")
        
        # Step -1: Check active subscription
        if not skip_subscription_check:
            print("\n[STEP -1] Checking active subscription...")
            has_subscription, sub_info = self.check_active_subscription()
            
            if not has_subscription:
                print("\n" + "=" * 60)
                print("[WARNING] ⚠️  No valid active subscription!")
                print("[INFO] Credit refill requires an active subscription that supports refill.")
                print("[INFO] Please check your subscription status at https://gaccode.com/subscriptions")
                print("=" * 60)
                
                # Send subscription error email
                self.send_email_alert(
                    "订阅检查失败",
                    "未找到有效的活跃订阅或订阅不支持积分重置。\n请访问 https://gaccode.com/subscriptions 检查订阅状态。",
                    "error"
                )
                
                # For automated runs, we return False
                return False
            else:
                print("[INFO] ✓ Active subscription verified!")
        else:
            print("\n[INFO] Skipping subscription check (--skip-subscription-check)")
        
        # Step 0: Check if already reset today
        print("\n[STEP 0] Checking if already reset today...")
        already_reset, reset_time = self.check_today_reset()
        
        if already_reset:
            if reset_time is None:
                # Network error or other issue, cannot verify
                print("\n" + "=" * 60)
                print(f"[ERROR] ❌ Cannot verify today's reset status!")
                print(f"[INFO] Aborting execution to avoid duplicate submission.")
                print(f"[INFO] Please check your network connection and try again.")
                print("=" * 60)
                
                # Send network error email
                self.send_email_alert(
                    "网络错误 - 无法验证重置状态",
                    "无法验证今天是否已经重置积分（网络连接失败）。\n为避免重复提交，已终止执行。\n请检查网络连接后重试。",
                    "error"
                )
                
                return False  # Return False to indicate error
            else:
                # Already reset today
                print("\n" + "=" * 60)
                print(f"[INFO] ⚠️  Already reset today!")
                print(f"[INFO] Last reset time: {reset_time}")
                print(f"[INFO] Please wait until tomorrow to reset again.")
                print("=" * 60)
                
                # Send email notification for already reset
                self.send_email_alert(
                    "今日已重置 - 无需操作",
                    f"今天已经完成积分重置，无需重复操作。\n\n上次重置时间: {reset_time}\n\n请等待明天再次重置。",
                    "info"
                )
                
                return True  # Return True because no error occurred
        else:
            print("[INFO] ✓ No reset found today, proceeding...")
        
        # Optional: Check balance before
        if check_balance:
            print("\n[STEP 0.5] Checking credit balance before reset...")
            self.get_credit_balance()
        
        # Step 1: Check recaptcha requirement
        print("\n[STEP 1] Checking recaptcha requirement...")
        recaptcha_status = self.check_recaptcha_required()
        
        if not recaptcha_status:
            print("[FAILED] Could not check recaptcha status")
            return False
        
        if recaptcha_status.get('requiresRecaptcha', False):
            print("[FAILED] Recaptcha is required. Manual intervention needed.")
            return False
        
        # Check if daily limit is reached
        ticket_count = recaptcha_status.get('ticketCountToday', 0)
        daily_limit = recaptcha_status.get('dailyLimit', 3)
        
        if ticket_count >= daily_limit:
            print(f"[FAILED] Daily ticket limit reached ({ticket_count}/{daily_limit})")
            return False
        
        # Step 2: Create ticket
        print("\n[STEP 2] Creating credit refill request ticket...")
        time.sleep(1)  # Small delay to be polite to the server
        
        ticket_response = self.create_ticket()
        
        if not ticket_response or 'ticket' not in ticket_response:
            print("[FAILED] Could not create ticket")
            return False
        
        ticket_id = ticket_response['ticket'].get('id')
        
        # Step 3: Verify ticket
        print("\n[STEP 3] Verifying ticket status...")
        time.sleep(1)  # Small delay
        
        verification = self.verify_ticket(ticket_id)
        
        if not verification:
            print("[FAILED] Could not verify ticket")
            return False
        
        # Check if ticket is closed (which means credits are reset)
        status = verification['ticket'].get('status')
        if status == 'CLOSED':
            print("\n" + "=" * 60)
            print("[SUCCESS] Credits have been reset successfully! ✅")
            print("=" * 60)
            
            # Optional: Check balance after
            balance_info = ""
            if check_balance:
                print("\n[STEP 4] Checking credit balance after reset...")
                time.sleep(1)
                balance_data = self.get_credit_balance()
                if balance_data and 'balance' in balance_data:
                    balance_info = f"\n当前积分: {balance_data.get('balance', 'N/A')}"
            
            # Send success email notification
            messages = verification['ticket'].get('messages', [])
            response_msg = messages[-1].get('message', '') if messages else ''
            
            self.send_email_alert(
                "积分重置成功 ✅",
                f"积分已成功重置！\n\n工单ID: {ticket_id}\n响应消息: {response_msg}\n完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{balance_info}",
                "success"
            )
            
            return True
        else:
            print(f"\n[WARNING] Ticket created but status is: {status}")
            print("Please check manually if credits were reset.")
            
            # Send warning email
            self.send_email_alert(
                "积分重置状态异常",
                f"工单已创建但状态为: {status}\n工单ID: {ticket_id}\n请手动检查是否重置成功。",
                "error"
            )
            
            return False


def load_config(config_path):
    """
    Load configuration from file
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        dict: Configuration dictionary
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"[ERROR] Configuration file not found: {config_path}")
        print("[INFO] Please create config.json based on config.json.example")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON in configuration file: {e}")
        sys.exit(1)


def main():
    """Main entry point for the script"""
    
    parser = argparse.ArgumentParser(
        description='Automatic Credit Reset Bot for gaccode.com',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python auto_reset_credits_advanced.py
  python auto_reset_credits_advanced.py --config my_config.json
  python auto_reset_credits_advanced.py --check-balance
  python auto_reset_credits_advanced.py --token YOUR_TOKEN_HERE
        """
    )
    
    parser.add_argument(
        '--config', '-c',
        default='config.json',
        help='Path to configuration file (default: config.json)'
    )
    
    parser.add_argument(
        '--token', '-t',
        help='Authentication token (overrides config file)'
    )
    
    parser.add_argument(
        '--check-balance', '-b',
        action='store_true',
        help='Check credit balance before and after reset'
    )
    
    parser.add_argument(
        '--dry-run', '-d',
        action='store_true',
        help='Dry run mode (only check recaptcha status)'
    )
    
    parser.add_argument(
        '--skip-subscription-check',
        action='store_true',
        help='Skip subscription check (for testing)'
    )
    
    parser.add_argument(
        '--test-email',
        action='store_true',
        help='Test email notification functionality'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Override token if provided via command line
    if args.token:
        config['auth_token'] = args.token
    
    # Also check environment variable
    env_token = os.getenv('GACCODE_AUTH_TOKEN')
    if env_token:
        config['auth_token'] = env_token
    
    try:
        # Create bot instance with config file path for saving
        bot = CreditResetBot(config, config_file_path=args.config)
        
        # Test email mode
        if args.test_email:
            print("=" * 60)
            print("Email Notification Test Mode")
            print("=" * 60)
            print(f"Config: {args.config}")
            print("-" * 60)
            
            # Get balance for test email
            balance_data = bot.get_credit_balance()
            balance_info = ""
            if balance_data and 'balance' in balance_data:
                balance_info = f"\n当前积分: {balance_data.get('balance', 'N/A')}"
            
            # Send test email
            test_body = f"""这是一封测试邮件，用于验证GAC积分重置工具的邮件功能。

如果您收到此邮件，说明邮件配置正确。{balance_info}

配置文件: {args.config}
测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

您可以根据需要调整 config.json 中的邮件通知设置。"""
            
            bot.send_email_alert(
                "邮件功能测试",
                test_body,
                "info"
            )
            
            print("-" * 60)
            print("Test complete. Please check your inbox.")
            print("=" * 60)
            sys.exit(0)
        
        # Dry run mode - only check status
        if args.dry_run:
            print("[INFO] Running in dry-run mode...")
            bot.check_recaptcha_required()
            if args.check_balance:
                bot.get_credit_balance()
            return
        
        # Run the bot
        success = bot.run(
            check_balance=args.check_balance,
            skip_subscription_check=args.skip_subscription_check
        )
        
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
            
    except ValueError as e:
        print(f"[ERROR] Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

