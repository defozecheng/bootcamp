
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()

mongo_uri = os.getenv('MONGODB_ATLAS_CLUSTER_URI')

class DatabaseManager:
    def __init__(self, db_name='example.db', connection_string=mongo_uri):
        self.client = MongoClient(connection_string)
        self.db = self/self.client[db_name]
        self.users_collection = self.db.users
        self.posts_collection = self.db.posts
        self.init_database()

    def init_database(self):
        """Initialize database with collection and indexes"""
        # Create unique index on email for users
        self.users_collection.create_index("email", unique=True)
        # Create index on user_id for poste for better query performance
        self.posts_collection.create_index("user_id")

    def create_user(self, name, email, age):
        """ Create a new user"""
        try:
            user_doc = {
                "name": name,
                "email": email,
                "created_at": datetime.now()
            }
            result = self.users_collection.insert_one(user_doc)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_all_users(self):
        """Get all users"""
        try:
            users = list(self.users_collection.find())
            # Convert ObjectId to string for display
            for user in users:
                user['_id'] = str(user['_id'])
            return users
        except Exception as e:
            print(f"Error fetching users: {e}")
            return[]

    def get_user_posts(self, user_id):
        """Get posts by user"""
        try:
            # Convert string user_id to ObjectedId if it's a valid ObjectId
            if ObjectId.is_valid(user_id):
                user_object_id = ObjectId(user_id)
            else:
                user_object_id = user_id

            posts = list(self.posts_collection.find(
                {"user_id": user_object_id}
            ).sort("created_at"),-1)

            # Convert ObjectId to string for display
            for post in posts:
                post['_id'] = str(post['_id'])
                post['user_id'] = str(post['user_id'])

            return posts
        except Exception as e:
            print(f"Error fetching posts : {e}")
            return[]

        def delete_user(self, user_id):
            """Delete user and their posts"""
            try:
                # Convert string user_id to ObjectId if it's a valid ObjectId
                if ObjectId.is_valid(user_id):
                    user_object_id = ObjectId(user_id)
                else:
                    user_object_id = user_id

                # Delete user's post first
                self.posts_colllection.delete_many({"user_id"=user_object_id})

