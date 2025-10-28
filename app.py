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
from dotenv import load_dotenv  # ← ADD THIS

# Load environment variables
load_dotenv()  # ← ADD THIS

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', os.urandom(24))  # ← UPDATE THIS

# MongoDB connection - works both locally and in production
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')  # ← UPDATE THIS
client = MongoClient(MONGODB_URI)  # ← UPDATE THIS
db = client['alcohol_regulation']
users_collection = db['users']
shop_owners_collection = db['shop_owners']
admin_collection = db['admin_details']

# Email configuration - use environment variables
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS', 'pvsk435@gmail.com')  # ← UPDATE THIS
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'vrjqkmcejzhmyxrn')  # ← UPDATE THIS
# Initialize database with sample data if empty
def init_db():
    if users_collection.count_documents({}) == 0:
        sample_users = [
            {
                'name': 'Praveen',
                'id': '1234',
                'bloodGroup': 'O+',
                'phoneNumber': '125678938980',
                'age': '25',
                'state': 'Tamil Nadu',
                'district': 'Chennai',
                'photo': 'https://img.etimg.com/thumb/msid-75194748,width-640,height-480,imgsize-300190,resizemode-4/anchor-beard.jpg',
                'consumption': {
                    'jan': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'feb': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'mar': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'apr': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'may': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'jun': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'jul': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'aug': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'sep': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'}
                }
            },
            {
                'name': 'Jane Smith',
                'id': '5678',
                'bloodGroup': 'A-',
                'phoneNumber': '258702547109',
                'age': '65',
                'state': 'Tamil Nadu',
                'photo': 'https://a.espncdn.com/combiner/i?img=/i/headshots/soccer/players/full/285629.png&w=350&h=254',
                'consumption': {
                    'jan': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'feb': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'mar': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'apr': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'may': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'jun': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'jul': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'aug': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'sep': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'}
                }
            },
            {
                'name': 'Jon',
                'id': '5588',
                'bloodGroup': 'B-',
                'phoneNumber': '782277774451',
                'age': '30',
                'state': 'Tamil Nadu',
                'photo': 'https://media.istockphoto.com/id/1392990621/photo/smart-handsome-positive-indian-or-arabian-guy-with-glasses-in-casual-wear-student-or.jpg?s=2048x2048&w=is&k=20&c=FYklnJ34SEXccfiXVE0RYv22ie1HhcCePUTv7T0PCS8=',
                'consumption': {
                    'jan': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'feb': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'mar': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'apr': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'may': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'jun': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'jul': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'aug': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'sep': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'}
                }
            },
            {
                'name': 'Santhosh',
                'id': '338',
                'bloodGroup': 'A+',
                'phoneNumber': '985728301830',
                'age': '62',
                'state': 'Tamil Nadu',
                'photo': 'https://www.travelvisapro.com/wp-content/uploads/2023/05/Facial-Hair-in-Passport-Photo.jpg',
                'consumption': {
                    'jan': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'feb': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'mar': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'apr': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'may': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'jun': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'jul': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'aug': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'sep': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'}
                }
            },
            {
                'name': 'Rafael',
                'id': '318',
                'bloodGroup': 'B+',
                'phoneNumber': '987654321234',
                'age': '23',
                'state': 'Tamil Nadu',
                'photo': 'https://i.shgcdn.com/8fec0c30-2420-4a45-9ceb-042a337e16d7/-/format/auto/-/preview/3000x3000/-/quality/lighter/',
                'consumption': {
                    'jan': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'feb': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'mar': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'apr': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'may': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'jun': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'jul': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'aug': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'sep': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'}
                }
            },
            {
                'name': 'Murali',
                'id': '291',
                'bloodGroup': 'A-',
                'phoneNumber': '987865342457',
                'age': '20',
                'state': 'Tamil Nadu',
                'photo': 'https://png.pngtree.com/png-vector/20230928/ourmid/pngtree-young-indian-man-png-image_10149659.png',
                'consumption': {
                    'jan': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'feb': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'mar': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'apr': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'may': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'jun': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'jul': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'aug': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'sep': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'}
                }
            },
            {
                'name': 'Rajesh',
                'id': '325',
                'bloodGroup': 'B+',
                'phoneNumber': '345654345678',
                'age': '27',
                'state': 'Tamil Nadu',
                'photo': 'https://i.pinimg.com/474x/84/fb/3b/84fb3b82c7de88656e6ea770bec71b3e.jpg',
                'consumption': {
                    'jan': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'feb': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'mar': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'apr': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'may': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'jun': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'jul': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'aug': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'sep': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'}
                }
            },
            {
                'name': 'Naren',
                'id': '295',
                'bloodGroup': 'O+',
                'phoneNumber': '345610986327',
                'age': '16',
                'state': 'Tamil Nadu',
                'photo': 'https://media.istockphoto.com/id/1336063208/photo/single-portrait-of-smiling-confident-male-student-teenager-looking-at-camera-in-library.jpg?s=612x612&w=0&k=20&c=w9SCRRCFa-Li82fmZotJzHdGGWXBVN7FgfBCD5NK7ic=',
                'consumption': {
                    'jan': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'feb': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'mar': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'apr': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'may': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'jun': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'jul': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'aug': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'},
                    'sep': {'w1': '0', 'w2': '0', 'w3': '0', 'w4': '0'}
                }
            }
            # ... (other users remain the same)
        ]
        users_collection.insert_many(sample_users)
        print("Sample data inserted into MongoDB")
    
    if shop_owners_collection.count_documents({}) == 0:
        sample_shop_owners = [
            {
                "type": "shop_owner",
                "email": "praveenvsk031@gmail.com",
                "license_number": "TN01CN001",
                "password": "password123",
                "shop_name": "TASMAC Chennai Branch 1",
                "district": "Chennai",
                "created_at": datetime.now()
            },
            {
                "type": "shop_owner",
                "email": "owner2@example.com",
                "license_number": "TN01CN002",
                "password": "password123",
                "shop_name": "TASMAC Chennai Branch 2",
                "district": "Chennai",
                "created_at": datetime.now()
            },
            {
                "type": "shop_owner",
                "email": "owner3@example.com",
                "license_number": "TN01CN003",
                "password": "password123",
                "shop_name": "TASMAC Chennai Branch 3",
                "district": "Chennai",
                "created_at": datetime.now()
            },
            {
                "type": "shop_owner",
                "email": "owner4@example.com",
                "license_number": "TN01CN004",
                "password": "password123",
                "shop_name": "TASMAC Madurai Branch 1",
                "district": "Madurai",
                "created_at": datetime.now()
            },
            {
                "type": "shop_owner",
                "email": "owner5@example.com",
                "license_number": "TN01CN005",
                "password": "password123",
                "shop_name": "TASMAC Madurai Branch 2",
                "district": "Madurai",
                "created_at": datetime.now()
            },
            {
                "type": "shop_owner",
                "email": "owner6@example.com",
                "license_number": "TN01CN006",
                "password": "password123",
                "shop_name": "TASMAC Coimbatore Branch 1",
                "district": "Coimbatore",
                "created_at": datetime.now()
            }
        ]
        shop_owners_collection.insert_many(sample_shop_owners)
        print("Sample shop owners inserted into MongoDB")
    
    if admin_collection.count_documents({}) == 0:
        sample_admins = [
            {
                "type": "admin",
                "email": "admin@tasmac.com",
                "password": "admin123",
                "name": "TASMAC Admin",
                "district_access": ["Chennai", "Madurai", "Coimbatore"],
                "created_at": datetime.now()
            },
            {
                "type": "admin",
                "email": "chennai.admin@tasmac.com",
                "password": "chennai123",
                "name": "Chennai District Admin",
                "district_access": ["Chennai"],
                "created_at": datetime.now()
            }
        ]
        admin_collection.insert_many(sample_admins)
        print("Sample admin users inserted into MongoDB")

# Admin Routes
@app.route('/admin')
def admin_login_page():
    return render_template('admin-login.html')

@app.route('/admin-dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect('/admin')
    
    admin_email = session.get('admin_email')
    admin = admin_collection.find_one({'email': admin_email})
    
    if not admin:
        return redirect('/admin')
    
    # Get all shop owners based on admin's district access
    districts = admin.get('district_access', [])
    shop_owners = list(shop_owners_collection.find({'district': {'$in': districts}}))
    
    # Get all users from those districts
    users = list(users_collection.find({'district': {'$in': districts}}))
    
    # Calculate total sales and other stats
    total_sales = 0
    for user in users:
        for month, weeks in user['consumption'].items():
            for week, bottles in weeks.items():
                total_sales += int(bottles) if bottles.isdigit() else 0
    
    # Count shops by district
    shops_by_district = {}
    for district in districts:
        shops_by_district[district] = shop_owners_collection.count_documents({'district': district})
    
    return render_template('admin-dashboard.html', 
                         admin=admin, 
                         shop_owners=shop_owners, 
                         total_sales=total_sales,
                         shops_by_district=shops_by_district,
                         total_users=len(users))

@app.route('/admin-login', methods=['POST'])
def admin_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    admin = admin_collection.find_one({'email': email, 'password': password})
    
    if admin:
        session['admin_logged_in'] = True
        session['admin_email'] = email
        session['admin_name'] = admin.get('name', 'Admin')
        session['admin_districts'] = admin.get('district_access', [])
        
        return jsonify({'success': True, 'message': 'Login successful'})
    else:
        return jsonify({'success': False, 'message': 'Invalid email or password'})

@app.route('/admin-logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_email', None)
    session.pop('admin_name', None)
    session.pop('admin_districts', None)
    return redirect('/admin')

@app.route('/admin-forgot-password')
def admin_forgot_password():
    return render_template('admin-forgot-password.html')

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
        
        # Create professional HTML email template
        html_content = f"""
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
        
        # Send OTP via email
        try:
            msg = MIMEText(html_content, 'html')
            msg['Subject'] = '🔐 TASMAC Admin Password Reset - Verification Code'
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = email
            
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)
            
            print(f"Admin OTP {otp} sent to {email}")
            return jsonify({'success': True, 'message': 'OTP sent successfully'})
            
        except Exception as e:
            print(f"Email error: {str(e)}")
            return jsonify({'success': False, 'message': f'Failed to send OTP: {str(e)}'})
            
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({'success': False, 'message': 'Server error occurred'})

@app.route('/admin-verify-otp')
def admin_verify_otp():
    email = session.get('admin_otp_email')
    if not email:
        return redirect('/admin-forgot-password')
    return render_template('admin-verify-otp.html', email=email)

@app.route('/admin-validate-otp', methods=['POST'])
def admin_validate_otp():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data received'})

        user_otp = data.get('otp')
        if not user_otp:
            return jsonify({'success': False, 'message': 'OTP is required'})
        
        stored_otp = session.get('admin_otp')
        expiry = session.get('admin_otp_expiry')
        
        print(f"Received Admin OTP: {user_otp}, Stored OTP: {stored_otp}")
        
        if not stored_otp or not expiry:
            return jsonify({'success': False, 'message': 'OTP expired or not found'})
        
        if datetime.now() > datetime.fromisoformat(expiry):
            return jsonify({'success': False, 'message': 'OTP expired'})
        
        if user_otp == stored_otp:
            session['admin_otp_verified'] = True
            return jsonify({'success': True, 'message': 'OTP verified successfully'})
        else:
            return jsonify({'success': False, 'message': 'Invalid OTP'})
            
    except Exception as e:
        print(f"Admin OTP validation error: {str(e)}")
        return jsonify({'success': False, 'message': 'Server error occurred'})

@app.route('/admin-reset-password')
def admin_reset_password():
    if not session.get('admin_otp_verified'):
        return redirect('/admin-forgot-password')
    return render_template('admin-reset-password.html')

@app.route('/admin-update-password', methods=['POST'])
def admin_update_password():
    print("Admin update password endpoint called")
    if not session.get('admin_otp_verified'):
        print("Admin OTP not verified")
        return jsonify({'success': False, 'message': 'OTP not verified'})

    data = request.json
    print("Received data:", data)

    email = session.get('admin_otp_email')
    password = data.get('password')
    confirm_password = data.get('confirmPassword')

    if password != confirm_password:
        return jsonify({'success': False, 'message': 'Passwords do not match'})

    # Update password in database
    try:
        result = admin_collection.update_one(
            {'email': email},
            {'$set': {'password': password}}
        )
        
        if result.modified_count == 0:
            return jsonify({'success': False, 'message': 'Failed to update password'})
        
        # Clear session
        session.pop('admin_otp', None)
        session.pop('admin_otp_email', None)
        session.pop('admin_otp_expiry', None)
        session.pop('admin_otp_verified', None)
        
        print("Admin password updated successfully")
        return jsonify({'success': True, 'message': 'Password updated successfully'})
    except Exception as e:
        print(f"Error updating admin password: {str(e)}")
        return jsonify({'success': False, 'message': f'Failed to update password: {str(e)}'})

# API Routes for admin data
@app.route('/api/admin/shop-owners')
def get_shop_owners():
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    districts = session.get('admin_districts', [])
    shop_owners = list(shop_owners_collection.find({'district': {'$in': districts}}))
    
    for shop in shop_owners:
        shop['_id'] = str(shop['_id'])
    
    return jsonify(shop_owners)

@app.route('/api/admin/sales-data')
def get_sales_data():
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    districts = session.get('admin_districts', [])
    users = list(users_collection.find({'district': {'$in': districts}}))
    
    monthly_sales = {
        'jan': 0, 'feb': 0, 'mar': 0, 'apr': 0,
        'may': 0, 'jun': 0, 'jul': 0, 'aug': 0, 'sep': 0
    }
    
    for user in users:
        for month, weeks in user['consumption'].items():
            if month in monthly_sales:
                for week, bottles in weeks.items():
                    monthly_sales[month] += int(bottles) if bottles.isdigit() else 0
    
    return jsonify(monthly_sales)

# ... (rest of your existing routes remain the same)

# Forgot Password Routes (for shop owners - existing)
@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot-password.html')

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
        
        # Create professional HTML email template for shop owners
        html_content = f"""
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
        
        # Send OTP via email
        try:
            msg = MIMEText(html_content, 'html')
            msg['Subject'] = '🔐 TASMAC Password Reset - Verification Code'
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = email
            
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)
            
            print(f"OTP {otp} sent to {email}")
            return jsonify({'success': True, 'message': 'OTP sent successfully'})
            
        except Exception as e:
            print(f"Email error: {str(e)}")
            return jsonify({'success': False, 'message': f'Failed to send OTP: {str(e)}'})
            
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({'success': False, 'message': 'Server error occurred'})

@app.route('/verify-otp')
def verify_otp():
    email = session.get('otp_email')
    if not email:
        return redirect('/forgot-password')
    return render_template('verify-otp.html', email=email)

@app.route('/validate-otp', methods=['POST'])
def validate_otp():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data received'})

        user_otp = data.get('otp')
        if not user_otp:
            return jsonify({'success': False, 'message': 'OTP is required'})
        
        stored_otp = session.get('otp')
        expiry = session.get('otp_expiry')
        
        print(f"Received OTP: {user_otp}, Stored OTP: {stored_otp}")
        
        if not stored_otp or not expiry:
            return jsonify({'success': False, 'message': 'OTP expired or not found'})
        
        if datetime.now() > datetime.fromisoformat(expiry):
            return jsonify({'success': False, 'message': 'OTP expired'})
        
        if user_otp == stored_otp:
            session['otp_verified'] = True
            return jsonify({'success': True, 'message': 'OTP verified successfully'})
        else:
            return jsonify({'success': False, 'message': 'Invalid OTP'})
            
    except Exception as e:
        print(f"OTP validation error: {str(e)}")
        return jsonify({'success': False, 'message': 'Server error occurred'})

@app.route('/reset-password')
def reset_password():
    if not session.get('otp_verified'):
        return redirect('/forgot-password')
    return render_template('reset-password.html')

@app.route('/update-password', methods=['POST'])
def update_password():
    print("Update password endpoint called")
    if not session.get('otp_verified'):
        print("OTP not verified")
        return jsonify({'success': False, 'message': 'OTP not verified'})

    data = request.json
    print("Received data:", data)

    email = session.get('otp_email')
    password = data.get('password')
    confirm_password = data.get('confirmPassword')

    if password != confirm_password:
        return jsonify({'success': False, 'message': 'Passwords do not match'})

    # Update password in database
    try:
        result = shop_owners_collection.update_one(
            {'email': email},
            {'$set': {'password': password}}
        )
        
        if result.modified_count == 0:
            return jsonify({'success': False, 'message': 'Failed to update password'})
        
        # Clear session
        session.pop('otp', None)
        session.pop('otp_email', None)
        session.pop('otp_expiry', None)
        session.pop('otp_verified', None)
        
        print("Password updated successfully")
        return jsonify({'success': True, 'message': 'Password updated successfully'})
    except Exception as e:
        print(f"Error updating password: {str(e)}")
        return jsonify({'success': False, 'message': f'Failed to update password: {str(e)}'})

# API Routes
@app.route('/api/user/<user_id>')
def get_user(user_id):
    user = users_collection.find_one({'id': user_id})
    if user:
        user['_id'] = str(user['_id'])
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/user-by-license/<license_number>')
def get_user_by_license(license_number):
    # First check shop owners, then regular users
    user = shop_owners_collection.find_one({'license_number': license_number})
    if not user:
        user = users_collection.find_one({'license_number': license_number})

    if user:
        user['_id'] = str(user['_id'])
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/user/<user_id>/update_consumption', methods=['POST'])
def update_consumption(user_id):
    data = request.json
    month = data.get('month')
    week = data.get('week')
    value = int(data.get('value', 0))

    user = users_collection.find_one({'id': user_id})
    if not user:
        return jsonify({'error': 'User not found'}), 404

    age = int(user['age'])
    if age < 18:
        return jsonify({'error': 'Cannot provide alcohol to underage person'}), 400

    month_data = user['consumption'][month]
    monthly_total = sum(int(month_data[w]) for w in ['w1', 'w2', 'w3', 'w4'])

    if monthly_total + value > 12:
        return jsonify({'error': 'Monthly limit exceeded. Cannot provide more alcohol'}), 400

    current_week_value = int(month_data[week])
    if current_week_value + value > 3:
        return jsonify({'error': 'Weekly limit exceeded. Cannot provide more alcohol'}), 400

    new_value = current_week_value + value
    update_query = {f'consumption.{month}.{week}': str(new_value)}

    users_collection.update_one({'id': user_id}, {'$set': update_query})

    updated_user = users_collection.find_one({'id': user_id})
    updated_user['_id'] = str(updated_user['_id'])
    return jsonify(updated_user)

# Serve pages
@app.route('/details')
def details():
    return render_template('details.html')

@app.route('/fingerprint')
def fingerprint():
    return render_template('fingerprint.html')

@app.route('/fingerprint.html')
def fingerprint_html():
    return render_template('fingerprint.html')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
    
if __name__ == '__main__':
    init_db()
    # Disable reloader to prevent socket errors
    app.run(debug=True, port=5000, use_reloader=False)    