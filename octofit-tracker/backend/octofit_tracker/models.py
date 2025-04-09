from djongo import models
from djongo.models.fields import ObjectIdField
from bson import ObjectId

class User(models.Model):
    id = models.ObjectIdField(primary_key=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.email

    class Meta:
        app_label = 'tracker_app'

class Team(models.Model):
    # Using AutoField for id instead of ObjectIdField to avoid migration issues
    # _id still accesible in MongoDB
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User)  # More compatible than ArrayField

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'tracker_app'

class Activity(models.Model):
    # Using AutoField for id instead of ObjectIdField to avoid migration issues
    # _id still accesible in MongoDB
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    duration = models.IntegerField()  # in minutes
    date = models.DateField()

    def __str__(self):
        return f"{self.type} - {self.user.email}"

    class Meta:
        app_label = 'tracker_app'

class Leaderboard(models.Model):
    # Using AutoField for id instead of ObjectIdField to avoid migration issues
    # _id still accesible in MongoDB
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    points = models.IntegerField()

    def __str__(self):
        return f"{self.team.name} - {self.points} points"

    class Meta:
        app_label = 'tracker_app'

class Workout(models.Model):
    # Using AutoField for id instead of ObjectIdField to avoid migration issues
    # _id still accesible in MongoDB
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField()  # in minutes

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'tracker_app'
