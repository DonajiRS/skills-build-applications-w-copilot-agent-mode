from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from bson import ObjectId
from datetime import timedelta
from django.conf import settings
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Asegúrate de que las colecciones se vacíen completamente
        client = MongoClient(host=settings.DATABASES['default'].get('HOST', 'localhost'), port=int(settings.DATABASES['default'].get('PORT', 27017)))
        db = client[settings.DATABASES['default']['NAME']]
        db.users.drop()
        db.teams.drop()
        db.activity.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Elimina índices antes de insertar datos
        db.users.drop_indexes()
        db.teams.drop_indexes()
        db.activity.drop_indexes()
        db.leaderboard.drop_indexes()
        db.workouts.drop_indexes()

        # Elimina todos los índices de la colección `users` antes de recrearla
        db.users.drop_indexes()

        # Elimina el índice `email` antes de insertar datos
        db.users.drop_index("email_1")

        # Elimina y recrea la colección `users` para garantizar que esté limpia
        db.drop_collection("users")
        db.create_collection("users")

        # Elimina todos los documentos de la colección `users` y recrea los índices después de insertar datos
        db.users.delete_many({})

        # Create users
        users = [
            User(id=ObjectId(), email='thundergod@mhigh.edu', name='Thor', age=30),
            User(id=ObjectId(), email='metalgeek@mhigh.edu', name='Tony Stark', age=35),
            User(id=ObjectId(), email='zerocool@mhigh.edu', name='Steve Rogers', age=32),
            User(id=ObjectId(), email='crashoverride@mhigh.edu', name='Natasha Romanoff', age=28),
            User(id=ObjectId(), email='sleeptoken@mhigh.edu', name='Bruce Banner', age=40),
        ]
        User.objects.bulk_create(users)
        db.users.create_index("email", unique=True)

        # Create teams
        team1 = Team(name='Blue Team')
        team2 = Team(name='Gold Team')
        team1.save()
        team2.save()

        # Create activities
        activities = [
            Activity(user=users[0], type='Cycling', duration=60, date='2025-04-09'),
            Activity(user=users[1], type='Crossfit', duration=120, date='2025-04-08'),
            Activity(user=users[2], type='Running', duration=90, date='2025-04-07'),
            Activity(user=users[3], type='Strength', duration=30, date='2025-04-06'),
            Activity(user=users[4], type='Swimming', duration=75, date='2025-04-05'),
        ]
        Activity.objects.bulk_create(activities)

        # Create leaderboard entries
        leaderboard_entries = [
            Leaderboard(team=team1, points=100),
            Leaderboard(team=team2, points=90),
        ]
        Leaderboard.objects.bulk_create(leaderboard_entries)

        # Create workouts
        workouts = [
            Workout(name='Cycling Training', description='Road cycling event training', duration=60),
            Workout(name='Crossfit', description='Crossfit competition training', duration=120),
            Workout(name='Running Training', description='Marathon training', duration=90),
            Workout(name='Strength Training', description='Strength improvement training', duration=30),
            Workout(name='Swimming Training', description='Swimming competition training', duration=75),
        ]
        Workout.objects.bulk_create(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
