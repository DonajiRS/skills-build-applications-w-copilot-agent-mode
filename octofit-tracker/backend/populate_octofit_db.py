#!/usr/bin/env python
"""
Script para poblar la base de datos octofit_db directamente usando PyMongo.
"""

from pymongo import MongoClient
from bson import ObjectId
from datetime import timedelta
import random
import datetime

# Conectar a la base de datos MongoDB
client = MongoClient('localhost', 27017)
db = client['octofit_db']  # Usar octofit_db como nombre de la base de datos

# Eliminar colecciones existentes para evitar duplicados
db.users.drop()
db.teams.drop()
db.activities.drop()
db.leaderboard.drop()
db.workouts.drop()

# Recrear colecciones
db.create_collection('users')
db.create_collection('teams')
db.create_collection('activities')
db.create_collection('leaderboard')
db.create_collection('workouts')

# Datos de prueba
test_data = {
    "users": [
        {
            "username": "thundergod", 
            "email": "thundergod@mhigh.edu",
            "password": "thunderpass123"
        },
        {
            "username": "metalgeek",
            "email": "metalgeek@mhigh.edu",
            "password": "metalpass456"
        },
        {
            "username": "zerocool",
            "email": "zerocool@mhigh.edu",
            "password": "zeropass789"
        },
        {
            "username": "crashoverride",
            "email": "crashoverride@mhigh.edu",
            "password": "crashpass101"
        },
        {
            "username": "sleeptoken",
            "email": "sleeptoken@mhigh.edu",
            "password": "sleeppass202"
        }
    ],
    "teams": [
        {
            "name": "Blue Team"
        },
        {
            "name": "Gold Team"
        }
    ],
    "activities": [
        {
            "user": "thundergod",
            "activity_type": "Cycling",
            "duration_minutes": 60
        },
        {
            "user": "metalgeek",
            "activity_type": "Crossfit",
            "duration_minutes": 120
        },
        {
            "user": "zerocool",
            "activity_type": "Running",
            "duration_minutes": 90
        },
        {
            "user": "crashoverride",
            "activity_type": "Strength",
            "duration_minutes": 30
        },
        {
            "user": "sleeptoken",
            "activity_type": "Swimming",
            "duration_minutes": 75
        }
    ],
    "leaderboard": [
        {
            "score": 100
        },
        {
            "score": 90
        },
        {
            "score": 95
        },
        {
            "score": 85
        },
        {
            "score": 80
        }
    ],
    "workouts": [
        {
            "name": "Cycling Training",
            "description": "Training for a road cycling event",
            "duration_minutes": 60
        },
        {
            "name": "Crossfit",
            "description": "Training for a crossfit competition",
            "duration_minutes": 120
        },
        {
            "name": "Running Training",
            "description": "Training for a marathon",
            "duration_minutes": 90
        },
        {
            "name": "Strength Training",
            "description": "Training for strength",
            "duration_minutes": 30
        },
        {
            "name": "Swimming Training",
            "description": "Training for a swimming competition",
            "duration_minutes": 75
        }
    ]
}

# 1. Insertar usuarios
print("Creando usuarios...")
user_docs = []
user_ids = {}  # Mapear nombres de usuario a IDs para referencias posteriores

for user_data in test_data["users"]:
    user_id = ObjectId()
    user_ids[user_data["username"]] = user_id
    user_docs.append({
        "_id": user_id,
        "username": user_data["username"],
        "email": user_data["email"],
        "password": user_data["password"],  # En producción, esto debería estar hasheado
        "age": random.randint(14, 18)  # Edad aleatoria para estudiantes de secundaria
    })

db.users.insert_many(user_docs)
db.users.create_index("email", unique=True)
print(f"Creados {len(user_docs)} usuarios")

# 2. Insertar equipos
print("Creando equipos...")
team_docs = []
team_ids = []

for team_data in test_data["teams"]:
    team_id = ObjectId()
    team_ids.append(team_id)
    team_docs.append({
        "_id": team_id,
        "name": team_data["name"],
        "members": []  # Inicialmente vacío
    })

db.teams.insert_many(team_docs)
print(f"Creados {len(team_docs)} equipos")

# 3. Asignar usuarios a equipos
print("Asignando usuarios a equipos...")
for idx, (username, user_id) in enumerate(user_ids.items()):
    team_idx = idx % len(team_ids)
    db.teams.update_one(
        {"_id": team_ids[team_idx]},
        {"$push": {"members": user_id}}
    )

# 4. Insertar actividades
print("Creando actividades...")
activity_docs = []
today = datetime.datetime.now().date()

for activity_data in test_data["activities"]:
    username = activity_data["user"]
    user_id = user_ids.get(username)
    
    if user_id:
        activity_docs.append({
            "_id": ObjectId(),
            "user_id": user_id,
            "type": activity_data["activity_type"],
            "duration": activity_data["duration_minutes"],
            "date": today
        })

db.activities.insert_many(activity_docs)
print(f"Creadas {len(activity_docs)} actividades")

# 5. Insertar entradas de tablero de clasificación
print("Creando entradas de tablero de clasificación...")
leaderboard_docs = []

for idx, leaderboard_data in enumerate(test_data["leaderboard"]):
    team_idx = idx % len(team_ids)
    leaderboard_docs.append({
        "_id": ObjectId(),
        "team_id": team_ids[team_idx],
        "points": leaderboard_data["score"],
        "date": today
    })

db.leaderboard.insert_many(leaderboard_docs)
print(f"Creadas {len(leaderboard_docs)} entradas de tablero de clasificación")

# 6. Insertar entrenamientos
print("Creando entrenamientos...")
workout_docs = []

for workout_data in test_data["workouts"]:
    workout_docs.append({
        "_id": ObjectId(),
        "name": workout_data["name"],
        "description": workout_data["description"],
        "duration": workout_data["duration_minutes"]
    })

db.workouts.insert_many(workout_docs)
print(f"Creados {len(workout_docs)} entrenamientos")

print("¡Base de datos octofit_db poblada exitosamente!")
