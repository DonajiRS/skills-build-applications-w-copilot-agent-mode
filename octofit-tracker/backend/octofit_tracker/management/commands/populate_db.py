from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from bson import ObjectId
from datetime import timedelta
from django.conf import settings
from pymongo import MongoClient
from django.utils import timezone
import random

# Datos de prueba definidos localmente
test_data = {
    "users": [
        {
            "_id": ObjectId(),
            "username": "thundergod", 
            "email": "thundergod@mhigh.edu"
        },
        {
            "_id": ObjectId(),
            "username": "metalgeek",
            "email": "metalgeek@mhigh.edu"
        },
        {
            "_id": ObjectId(),
            "username": "zerocool",
            "email": "zerocool@mhigh.edu"
        },
        {
            "_id": ObjectId(),
            "username": "crashoverride",
            "email": "crashoverride@mhigh.edu"
        },
        {
            "_id": ObjectId(),
            "username": "sleeptoken",
            "email": "sleeptoken@mhigh.edu"
        }
    ],
    "teams": [
        {
            "_id": ObjectId(),
            "name": "Blue Team"
        },
        {
            "_id": ObjectId(),
            "name": "Gold Team"
        }
    ],
    "activities": [
        {
            "_id": ObjectId(),
            "user": "thundergod",
            "activity_type": "Cycling",
            "duration": timedelta(hours=1)
        },
        {
            "_id": ObjectId(),
            "user": "metalgeek",
            "activity_type": "Crossfit",
            "duration": timedelta(hours=2)
        },
        {
            "_id": ObjectId(),
            "user": "zerocool",
            "activity_type": "Running",
            "duration": timedelta(hours=1, minutes=30)
        },
        {
            "_id": ObjectId(),
            "user": "crashoverride",
            "activity_type": "Strength",
            "duration": timedelta(minutes=30)
        },
        {
            "_id": ObjectId(),
            "user": "sleeptoken",
            "activity_type": "Swimming",
            "duration": timedelta(hours=1, minutes=15)
        }
    ],
    "leaderboard": [
        {
            "_id": ObjectId(),
            "score": 100
        },
        {
            "_id": ObjectId(),
            "score": 90
        },
        {
            "_id": ObjectId(),
            "score": 95
        },
        {
            "_id": ObjectId(),
            "score": 85
        },
        {
            "_id": ObjectId(),
            "score": 80
        }
    ],
    "workouts": [
        {
            "_id": ObjectId(),
            "name": "Cycling Training",
            "description": "Training for a road cycling event"
        },
        {
            "_id": ObjectId(),
            "name": "Crossfit",
            "description": "Training for a crossfit competition"
        },
        {
            "_id": ObjectId(),
            "name": "Running Training",
            "description": "Training for a marathon"
        },
        {
            "_id": ObjectId(),
            "name": "Strength Training",
            "description": "Training for strength"
        },
        {
            "_id": ObjectId(),
            "name": "Swimming Training",
            "description": "Training for a swimming competition"
        }
    ]
}

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        # Drop existing collections and their indexes to avoid duplicate key errors
        db.tracker_app_user.drop()
        db.tracker_app_team.drop()
        db.tracker_app_activity.drop()
        db.tracker_app_leaderboard.drop()
        db.tracker_app_workout.drop()

        # Recreate collections without indexes
        db.create_collection('tracker_app_user')
        db.create_collection('tracker_app_team')
        db.create_collection('tracker_app_activity')
        db.create_collection('tracker_app_leaderboard')
        db.create_collection('tracker_app_workout')

        # Insertar usuarios directamente usando PyMongo
        self.stdout.write("Creating users...")
        user_docs = []
        for idx, user_data in enumerate(test_data["users"]):
            # Crear un ID único para cada usuario
            user_id = ObjectId()
            user_docs.append({
                "_id": user_id,
                "email": user_data["email"],
                "name": user_data["username"],
                "age": random.randint(14, 18)  # Random age for high school students
            })
        
        # Insertar directamente en la colección de MongoDB
        db.tracker_app_user.insert_many(user_docs)
        db.tracker_app_user.create_index("email", unique=True)
        self.stdout.write(f"Created {len(user_docs)} users")
        
        # Mapear nombres de usuario a IDs para uso posterior
        username_to_id = {doc["name"]: doc["_id"] for doc in user_docs}
        
        # Insertar equipos directamente usando PyMongo
        self.stdout.write("Creating teams...")
        team_docs = []
        team_ids = []
        for team_data in test_data["teams"]:
            team_id = ObjectId()
            team_ids.append(team_id)
            team_docs.append({
                "_id": team_id,
                "name": team_data["name"],
                "members": []  # Inicialmente sin miembros
            })
        
        db.tracker_app_team.insert_many(team_docs)
        self.stdout.write(f"Created {len(team_docs)} teams")
        
        # Asignar usuarios a equipos alternando
        for idx, user_id in enumerate(username_to_id.values()):
            team_idx = idx % len(team_ids)
            db.tracker_app_team.update_one(
                {"_id": team_ids[team_idx]},
                {"$push": {"members": user_id}}
            )
        
        # Insertar actividades directamente usando PyMongo
        self.stdout.write("Creating activities...")
        activity_docs = []
        today = timezone.now().date().isoformat()
        
        for activity_data in test_data["activities"]:
            username = activity_data["user"]
            user_id = username_to_id.get(username)
            
            if user_id:
                # Convertir timedelta a minutos
                duration_minutes = int(activity_data["duration"].total_seconds() / 60)
                activity_docs.append({
                    "_id": ObjectId(),
                    "user_id": user_id,
                    "type": activity_data["activity_type"],
                    "duration": duration_minutes,
                    "date": today
                })
        
        db.tracker_app_activity.insert_many(activity_docs)
        self.stdout.write(f"Created {len(activity_docs)} activities")

        # Insertar entradas de tablero de clasificación directamente usando PyMongo
        self.stdout.write("Creating leaderboard entries...")
        leaderboard_docs = []
        
        # Asignar entradas a equipos alternadamente
        for idx, leaderboard_data in enumerate(test_data["leaderboard"]):
            team_idx = idx % len(team_ids)
            leaderboard_docs.append({
                "_id": ObjectId(),
                "team_id": team_ids[team_idx],
                "points": leaderboard_data["score"]
            })
        
        db.tracker_app_leaderboard.insert_many(leaderboard_docs)
        self.stdout.write(f"Created {len(leaderboard_docs)} leaderboard entries")

        # Insertar entrenamientos directamente usando PyMongo
        self.stdout.write("Creating workouts...")
        workout_docs = []
        for workout_data in test_data["workouts"]:
            # Extraer duración del nombre (asumiendo un formato como "Cycling Training")
            if "Cycling" in workout_data["name"]:
                duration = 60
            elif "Crossfit" in workout_data["name"]:
                duration = 120
            elif "Running" in workout_data["name"]:
                duration = 90
            elif "Strength" in workout_data["name"]:
                duration = 30
            else:  # Swimming
                duration = 75
                
            workout_docs.append({
                "_id": ObjectId(),
                "name": workout_data["name"],
                "description": workout_data["description"],
                "duration": duration
            })
        
        db.tracker_app_workout.insert_many(workout_docs)
        self.stdout.write(f"Created {len(workout_docs)} workouts")

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
