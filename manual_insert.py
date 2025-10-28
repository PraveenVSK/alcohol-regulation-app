from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to MongoDB Atlas (same as your app)
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGODB_URI)
db = client['alcohol_regulation']

# Collections
shop_owners_collection = db['shop_owners']
admin_collection = db['admin_details']
users_collection = db['users']

def insert_all_data():
    print("Starting complete data insertion to MongoDB Atlas...")
    
    # Clear ALL existing data first
    shop_owners_collection.delete_many({})
    admin_collection.delete_many({})
    users_collection.delete_many({})
    
    print("Cleared all existing data")

    # Sample shop owners with districts
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
            "email": "muralikrishna01018@gmail.com",
            "license_number": "TN01CN002",
            "password": "12345",
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

    # Sample admin users
    sample_admins = [
        {
            "type": "admin",
            "email": "praveenvsk041@gmail.com",
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
        },
        {
            "type": "admin",
            "email": "senthilkumaran6382@gmail.com",
            "password": "madurai123",
            "name": "Madurai District Admin",
            "district_access": ["Madurai"],
            "created_at": datetime.now()
        }
    ]

    # Sample users data
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
            'district': 'Chennai',
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
            'district': 'Chennai',
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
            'district': 'Chennai',
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
            'district': 'Chennai',
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
            'district': 'Chennai',
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
            'district': 'Chennai',
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
            'district': 'Chennai',
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
    ]

    # Insert all data
    shop_result = shop_owners_collection.insert_many(sample_shop_owners)
    admin_result = admin_collection.insert_many(sample_admins)
    users_result = users_collection.insert_many(sample_users)

    print(f"✅ Inserted {len(shop_result.inserted_ids)} shop owners")
    print(f"✅ Inserted {len(admin_result.inserted_ids)} admin users")
    print(f"✅ Inserted {len(users_result.inserted_ids)} regular users")
    print("🎉 ALL sample data insertion completed successfully!")

if __name__ == '__main__':
    insert_all_data()