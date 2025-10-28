from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection - works both locally and in production
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGODB_URI)
db = client['alcohol_regulation']

# Collections
shop_owners_collection = db['shop_owners']
admin_collection = db['admin_details']
users_collection = db['users']

def insert_sample_data():
    print("Starting data insertion...")
    
    # Clear existing sample data (optional)
    shop_owners_collection.delete_many({})
    admin_collection.delete_many({})
    
    print("Cleared existing sample data")

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
            "email": "praveenmathslover100@gmail.com",
            "license_number": "TN01CN005",
            "password": "password123",
            "shop_name": "TASMAC Madurai Branch 2",
            "district": "Madurai",
            "created_at": datetime.now()
        },
        {
            "type": "shop_owner",
            "email": "vigneshiniramesh345@gmail.com",
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
            "email": "praveenvsk031@gmail.com",
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

    # Insert sample data
    shop_result = shop_owners_collection.insert_many(sample_shop_owners)
    admin_result = admin_collection.insert_many(sample_admins)

    print(f"✅ Inserted {len(shop_result.inserted_ids)} shop owners")
    print(f"✅ Inserted {len(admin_result.inserted_ids)} admin users")
    print("🎉 Sample data insertion completed successfully!")

    # Display inserted data
    print("\n📋 Inserted Shop Owners:")
    for shop in shop_owners_collection.find():
        print(f"  - {shop['shop_name']} ({shop['district']}) - {shop['email']}")

    print("\n👤 Inserted Admin Users:")
    for admin in admin_collection.find():
        print(f"  - {admin['name']} - {admin['email']} - Districts: {', '.join(admin['district_access'])}")

if __name__ == '__main__':
    insert_sample_data()