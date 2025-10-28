from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import json
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
import functools
import signal
import threading

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', os.urandom(24))

# MongoDB connection with SSL fix for Render
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')

try:
    # For production (Render) with SSL fix
    if MONGODB_URI.startswith('mongodb+srv://'):
        client = MongoClient(
            MONGODB_URI,
            tls=True,
            tlsAllowInvalidCertificates=False,
            retryWrites=True,
            w='majority',
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000,
            maxPoolSize=10  # Limit connections to save memory
        )
    else:
        # For local development
        client = MongoClient(MONGODB_URI)
    
    # Test connection immediately
    client.admin.command('ping')
    print("✅ MongoDB connected successfully with SSL!")
    
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    # Fallback for local development
    client = MongoClient('mongodb://localhost:27017/')
    print("🔄 Using local MongoDB fallback")

db = client['alcohol_regulation']
users_collection = db['users']
shop_owners_collection = db['shop_owners']
admin_collection = db['admin_details']

# Email configuration - use environment variables
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS', 'pvsk435@gmail.com')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'vrjqkmcejzhmyxrn')

# Threading-based timeout for email sending
def send_email_with_timeout(to_email, subject, html_content, timeout=25):
    """Send email with threading timeout to avoid blocking"""
    result = [None]  # Use list to store result across threads
    exception = [None]
    
    def send_email():
        try:
            msg = MIMEText(html_content, 'html')
            msg['Subject'] = subject
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = to_email
            
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)
            
            result[0] = True
        except Exception as e:
            exception[0] = e
            result[0] = False
    
    # Start email sending in a separate thread
    email_thread = threading.Thread(target=send_email)
    email_thread.daemon = True
    email_thread.start()
    email_thread.join(timeout=timeout)  # Wait for specified timeout
    
    if email_thread.is_alive():
        print(f"❌ Email sending timed out after {timeout} seconds")
        return False, "Email sending timed out. Please try again."
    
    if exception[0]:
        print(f"❌ Email error: {exception[0]}")
        return False, f"Failed to send email: {str(exception[0])}"
    
    return result[0], "Email sent successfully" if result[0] else "Failed to send email"

def check_database_connection():
    """Simple function to verify database connection"""
    try:
        client.admin.command('ping')
        collections = db.list_collection_names()
        print(f"✅ Connected to MongoDB. Collections: {collections}")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

# KEEP YOUR ORIGINAL BEAUTIFUL EMAIL TEMPLATES - JUST ADD THEM HERE
def create_admin_email_template(otp):
    """Your original beautiful admin email template"""
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>TASMAC Admin Password Reset</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 40px 20px;
                min-height: 100vh;
            }}
            
            .email-container {{
                max-width: 600px;
                margin: 0 auto;
                background: #ffffff;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
                position: relative;
            }}
            
            .header {{
                background: linear-gradient(135deg, #1a1c3d 0%, #2d3748 100%);
                padding: 40px 30px;
                text-align: center;
                position: relative;
                overflow: hidden;
            }}
            
            .header::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="rgba(255,255,255,0.05)"/><circle cx="75" cy="75" r="1" fill="rgba(255,255,255,0.05)"/><circle cx="50" cy="10" r="1" fill="rgba(255,255,255,0.03)"/><circle cx="10" cy="60" r="1" fill="rgba(255,255,255,0.03)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
            }}
            
            .header h1 {{
                color: #ffffff;
                font-size: 28px;
                font-weight: 700;
                margin-bottom: 8px;
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
                position: relative;
                z-index: 1;
            }}
            
            .header .subtitle {{
                color: #cbd5e0;
                font-size: 14px;
                font-weight: 400;
                opacity: 0.9;
                position: relative;
                z-index: 1;
            }}
            
            .logo-icon {{
                display: inline-block;
                width: 50px;
                height: 50px;
                background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
                border-radius: 12px;
                margin-bottom: 20px;
                position: relative;
                z-index: 1;
                box-shadow: 0 4px 12px rgba(66, 153, 225, 0.3);
            }}
            
            .logo-icon::before {{
                content: '🏪';
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 24px;
            }}
            
            .content {{
                padding: 50px 40px;
                background: #ffffff;
            }}
            
            .welcome-text {{
                font-size: 24px;
                font-weight: 600;
                color: #2d3748;
                text-align: center;
                margin-bottom: 20px;
            }}
            
            .instructions {{
                font-size: 16px;
                color: #4a5568;
                text-align: center;
                margin-bottom: 40px;
                line-height: 1.6;
            }}
            
            .otp-section {{
                background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
                border-radius: 16px;
                padding: 30px;
                text-align: center;
                margin: 30px 0;
                border: 2px solid #e2e8f0;
                position: relative;
            }}
            
            .otp-section::before {{
                content: '';
                position: absolute;
                top: -2px;
                left: -2px;
                right: -2px;
                bottom: -2px;
                background: linear-gradient(135deg, #4299e1, #3182ce, #2b6cb0);
                border-radius: 18px;
                z-index: -1;
            }}
            
            .otp-label {{
                font-size: 14px;
                color: #718096;
                font-weight: 500;
                margin-bottom: 15px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            
            .otp-code {{
                font-size: 36px;
                font-weight: 700;
                color: #2d3748;
                letter-spacing: 8px;
                font-family: 'Courier New', monospace;
                background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin: 10px 0;
            }}
            
            .validity-container {{
                background: linear-gradient(135deg, #fed7d7 0%, #feb2b2 100%);
                border-radius: 12px;
                padding: 20px;
                margin: 30px 0;
                border-left: 4px solid #f56565;
            }}
            
            .validity-container .icon {{
                font-size: 20px;
                margin-right: 10px;
            }}
            
            .validity-text {{
                color: #742a2a;
                font-weight: 600;
                font-size: 16px;
            }}
            
            .security-notice {{
                background: linear-gradient(135deg, #e6fffa 0%, #b2f5ea 100%);
                border-radius: 12px;
                padding: 25px;
                margin: 30px 0;
                border-left: 4px solid #38b2ac;
            }}
            
            .security-title {{
                color: #234e52;
                font-weight: 700;
                font-size: 16px;
                margin-bottom: 15px;
                display: flex;
                align-items: center;
            }}
            
            .security-title::before {{
                content: '🔒';
                margin-right: 8px;
                font-size: 18px;
            }}
            
            .security-list {{
                list-style: none;
                color: #2c7a7b;
                font-size: 14px;
                line-height: 1.8;
            }}
            
            .security-list li {{
                margin: 8px 0;
                position: relative;
                padding-left: 20px;
            }}
            
            .security-list li::before {{
                content: '✓';
                position: absolute;
                left: 0;
                color: #38b2ac;
                font-weight: bold;
            }}
            
            .divider {{
                height: 1px;
                background: linear-gradient(90deg, transparent 0%, #e2e8f0 50%, transparent 100%);
                margin: 40px 0;
            }}
            
            .footer {{
                background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
                padding: 30px 40px;
                text-align: center;
                border-top: 1px solid #e2e8f0;
            }}
            
            .footer .brand {{
                font-size: 18px;
                font-weight: 700;
                color: #2d3748;
                margin-bottom: 8px;
            }}
            
            .footer .govt-text {{
                color: #4a5568;
                font-size: 14px;
                font-weight: 500;
                margin: 4px 0;
            }}
            
            .footer .dept-text {{
                color: #718096;
                font-size: 13px;
                margin-top: 10px;
            }}
            
            .badge {{
                display: inline-block;
                background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
                color: white;
                padding: 6px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
                margin-top: 10px;
            }}
            
            @media (max-width: 600px) {{
                body {{
                    padding: 20px 10px;
                }}
                
                .content {{
                    padding: 30px 20px;
                }}
                
                .header {{
                    padding: 30px 20px;
                }}
                
                .otp-code {{
                    font-size: 28px;
                    letter-spacing: 4px;
                }}
                
                .footer {{
                    padding: 25px 20px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <div class="logo-icon"></div>
                <h1>TASMAC ADMIN</h1>
                <div class="subtitle">Tamil Nadu State Marketing Corporation</div>
            </div>
            
            <div class="content">
                <div class="welcome-text">Password Reset Request</div>
                
                <p class="instructions">
                    We received a request to reset your admin password. Please use the verification code below to proceed with your password reset.
                </p>
                
                <div class="otp-section">
                    <div class="otp-label">Verification Code</div>
                    <div class="otp-code">{otp}</div>
                </div>
                
                <div class="validity-container">
                    <div class="validity-text">
                        <span class="icon">⏰</span>
                        This verification code will expire in 10 minutes
                    </div>
                </div>
                
                <div class="security-notice">
                    <div class="security-title">Security Guidelines</div>
                    <ul class="security-list">
                        <li>Never share this verification code with anyone</li>
                        <li>TASMAC will never ask for your OTP via phone or email</li>
                        <li>If you didn't request this reset, please contact IT support</li>
                        <li>Use this code only on the official TASMAC admin portal</li>
                    </ul>
                </div>
                
                <div class="divider"></div>
                
                <p style="color: #718096; font-size: 14px; text-align: center; line-height: 1.6;">
                    This is an automated security notification from TASMAC Admin System. 
                    Please do not reply to this email.
                </p>
            </div>
            
            <div class="footer">
                <div class="brand">TASMAC ADMIN PORTAL</div>
                <div class="govt-text">Government of Tamil Nadu</div>
                <div class="govt-text">Alcohol Regulation & Licensing Division</div>
                <div class="badge">OFFICIAL</div>
                <div class="dept-text">
                    This email was sent from a secure, monitored system. All access attempts are logged.
                </div>
            </div>
        </div>
    </body>
    </html>
    """

def create_shop_owner_email_template(otp):
    """Your original beautiful shop owner email template"""
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>TASMAC Password Reset</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 40px 20px;
                min-height: 100vh;
            }}
            
            .email-container {{
                max-width: 600px;
                margin: 0 auto;
                background: #ffffff;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
                position: relative;
            }}
            
            .header {{
                background: linear-gradient(135deg, #2b6cb0 0%, #3182ce 100%);
                padding: 40px 30px;
                text-align: center;
                position: relative;
                overflow: hidden;
            }}
            
            .header::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="rgba(255,255,255,0.05)"/><circle cx="75" cy="75" r="1" fill="rgba(255,255,255,0.05)"/><circle cx="50" cy="10" r="1" fill="rgba(255,255,255,0.03)"/><circle cx="10" cy="60" r="1" fill="rgba(255,255,255,0.03)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
            }}
            
            .header h1 {{
                color: #ffffff;
                font-size: 28px;
                font-weight: 700;
                margin-bottom: 8px;
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
                position: relative;
                z-index: 1;
            }}
            
            .header .subtitle {{
                color: #bee3f8;
                font-size: 14px;
                font-weight: 400;
                opacity: 0.9;
                position: relative;
                z-index: 1;
            }}
            
            .logo-icon {{
                display: inline-block;
                width: 50px;
                height: 50px;
                background: linear-gradient(135deg, #4299e1 0%, #63b3ed 100%);
                border-radius: 12px;
                margin-bottom: 20px;
                position: relative;
                z-index: 1;
                box-shadow: 0 4px 12px rgba(66, 153, 225, 0.3);
            }}
            
            .logo-icon::before {{
                content: '🏪';
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 24px;
            }}
            
            .content {{
                padding: 50px 40px;
                background: #ffffff;
            }}
            
            .welcome-text {{
                font-size: 24px;
                font-weight: 600;
                color: #2d3748;
                text-align: center;
                margin-bottom: 20px;
            }}
            
            .instructions {{
                font-size: 16px;
                color: #4a5568;
                text-align: center;
                margin-bottom: 40px;
                line-height: 1.6;
            }}
            
            .otp-section {{
                background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
                border-radius: 16px;
                padding: 30px;
                text-align: center;
                margin: 30px 0;
                border: 2px solid #e2e8f0;
                position: relative;
            }}
            
            .otp-section::before {{
                content: '';
                position: absolute;
                top: -2px;
                left: -2px;
                right: -2px;
                bottom: -2px;
                background: linear-gradient(135deg, #38a169, #48bb78, #68d391);
                border-radius: 18px;
                z-index: -1;
            }}
            
            .otp-label {{
                font-size: 14px;
                color: #718096;
                font-weight: 500;
                margin-bottom: 15px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            
            .otp-code {{
                font-size: 36px;
                font-weight: 700;
                color: #2d3748;
                letter-spacing: 8px;
                font-family: 'Courier New', monospace;
                background: linear-gradient(135deg, #38a169 0%, #48bb78 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin: 10px 0;
            }}
            
            .validity-container {{
                background: linear-gradient(135deg, #fed7d7 0%, #feb2b2 100%);
                border-radius: 12px;
                padding: 20px;
                margin: 30px 0;
                border-left: 4px solid #f56565;
            }}
            
            .validity-container .icon {{
                font-size: 20px;
                margin-right: 10px;
            }}
            
            .validity-text {{
                color: #742a2a;
                font-weight: 600;
                font-size: 16px;
            }}
            
            .security-notice {{
                background: linear-gradient(135deg, #e6fffa 0%, #b2f5ea 100%);
                border-radius: 12px;
                padding: 25px;
                margin: 30px 0;
                border-left: 4px solid #38b2ac;
            }}
            
            .security-title {{
                color: #234e52;
                font-weight: 700;
                font-size: 16px;
                margin-bottom: 15px;
                display: flex;
                align-items: center;
            }}
            
            .security-title::before {{
                content: '🔒';
                margin-right: 8px;
                font-size: 18px;
            }}
            
            .security-list {{
                list-style: none;
                color: #2c7a7b;
                font-size: 14px;
                line-height: 1.8;
            }}
            
            .security-list li {{
                margin: 8px 0;
                position: relative;
                padding-left: 20px;
            }}
            
            .security-list li::before {{
                content: '✓';
                position: absolute;
                left: 0;
                color: #38b2ac;
                font-weight: bold;
            }}
            
            .divider {{
                height: 1px;
                background: linear-gradient(90deg, transparent 0%, #e2e8f0 50%, transparent 100%);
                margin: 40px 0;
            }}
            
            .footer {{
                background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
                padding: 30px 40px;
                text-align: center;
                border-top: 1px solid #e2e8f0;
            }}
            
            .footer .brand {{
                font-size: 18px;
                font-weight: 700;
                color: #2d3748;
                margin-bottom: 8px;
            }}
            
            .footer .govt-text {{
                color: #4a5568;
                font-size: 14px;
                font-weight: 500;
                margin: 4px 0;
            }}
            
            .footer .dept-text {{
                color: #718096;
                font-size: 13px;
                margin-top: 10px;
            }}
            
            .badge {{
                display: inline-block;
                background: linear-gradient(135deg, #38a169 0%, #48bb78 100%);
                color: white;
                padding: 6px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
                margin-top: 10px;
            }}
            
            @media (max-width: 600px) {{
                body {{
                    padding: 20px 10px;
                }}
                
                .content {{
                    padding: 30px 20px;
                }}
                
                .header {{
                    padding: 30px 20px;
                }}
                
                .otp-code {{
                    font-size: 28px;
                    letter-spacing: 4px;
                }}
                
                .footer {{
                    padding: 25px 20px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <div class="logo-icon"></div>
                <h1>TASMAC</h1>
                <div class="subtitle">Tamil Nadu State Marketing Corporation</div>
            </div>
            
            <div class="content">
                <div class="welcome-text">Password Reset Request</div>
                
                <p class="instructions">
                    We received a request to reset your TASMAC account password. Please use the verification code below to proceed with your password reset.
                </p>
                
                <div class="otp-section">
                    <div class="otp-label">Verification Code</div>
                    <div class="otp-code">{otp}</div>
                </div>
                
                <div class="validity-container">
                    <div class="validity-text">
                        <span class="icon">⏰</span>
                        This verification code will expire in 10 minutes
                    </div>
                </div>
                
                <div class="security-notice">
                    <div class="security-title">Security Guidelines</div>
                    <ul class="security-list">
                        <li>Never share this verification code with anyone</li>
                        <li>TASMAC will never ask for your OTP via phone or email</li>
                        <li>If you didn't request this reset, please contact administrator</li>
                        <li>Use this code only on the official TASMAC portal</li>
                    </ul>
                </div>
                
                <div class="divider"></div>
                
                <p style="color: #718096; font-size: 14px; text-align: center; line-height: 1.6;">
                    This is an automated security notification from TASMAC System. 
                    Please do not reply to this email.
                </p>
            </div>
            
            <div class="footer">
                <div class="brand">TASMAC OFFICIAL</div>
                <div class="govt-text">Government of Tamil Nadu</div>
                <div class="govt-text">Alcohol Regulation & Licensing Division</div>
                <div class="badge">OFFICIAL</div>
                <div class="dept-text">
                    This email was sent from a secure, monitored system. All access attempts are logged.
                </div>
            </div>
        </div>
    </body>
    </html>
    """

# KEEP ALL YOUR ORIGINAL ROUTES EXACTLY AS THEY WERE
# Just replace the email sending part in admin_send_otp and send_otp functions:

@app.route('/admin-send-otp', methods=['POST'])
def admin_send_otp():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data received'})

        email = data.get('email')
        if not email:
            return jsonify({'success': False, 'message': 'Email is required'})
        
        # Check if email exists in admin collection
        admin = admin_collection.find_one({'email': email})
        if not admin:
            return jsonify({'success': False, 'message': 'Email not registered. Please contact administrator.'})
        
        # Generate OTP
        otp = str(random.randint(100000, 999999))
        
        # Store OTP in session with expiration
        session['admin_otp'] = otp
        session['admin_otp_email'] = email
        session['admin_otp_expiry'] = (datetime.now() + timedelta(minutes=10)).isoformat()
        
        # Use your original beautiful email template
        html_content = create_admin_email_template(otp)
        
        # Send email with timeout protection
        success, message = send_email_with_timeout(
            email, 
            '🔐 TASMAC Admin Password Reset - Verification Code', 
            html_content
        )
        
        if success:
            print(f"Admin OTP {otp} sent to {email}")
            return jsonify({'success': True, 'message': 'OTP sent successfully'})
        else:
            return jsonify({'success': False, 'message': message})
            
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({'success': False, 'message': 'Server error occurred'})

@app.route('/send-otp', methods=['POST'])
def send_otp():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data received'})

        email = data.get('email')
        if not email:
            return jsonify({'success': False, 'message': 'Email is required'})
        
        # Check if email exists in shop owners
        user = shop_owners_collection.find_one({'email': email})
        if not user:
            return jsonify({'success': False, 'message': 'Email not registered. Please contact administrator.'})
        
        # Generate OTP
        otp = str(random.randint(100000, 999999))
        
        # Store OTP in session with expiration
        session['otp'] = otp
        session['otp_email'] = email
        session['otp_expiry'] = (datetime.now() + timedelta(minutes=10)).isoformat()
        
        # Use your original beautiful email template
        html_content = create_shop_owner_email_template(otp)
        
        # Send email with timeout protection
        success, message = send_email_with_timeout(
            email, 
            '🔐 TASMAC Password Reset - Verification Code', 
            html_content
        )
        
        if success:
            print(f"OTP {otp} sent to {email}")
            return jsonify({'success': True, 'message': 'OTP sent successfully'})
        else:
            return jsonify({'success': False, 'message': message})
            
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({'success': False, 'message': 'Server error occurred'})

# KEEP ALL YOUR OTHER ORIGINAL ROUTES EXACTLY AS THEY WERE
# ... (copy all your other routes exactly as they were)

if __name__ == '__main__':
    check_database_connection()
    app.run(debug=True, port=5000, use_reloader=False)