from djongo import models
from djongo.models.fields import ObjectIdField

class User(models.Model):
    id = ObjectIdField(primary_key=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    age = models.IntegerField()

    def __str__(self):
        return self.email

    class Meta:
        app_label = 'tracker_app'

class Team(models.Model):
    name = models.CharField(max_length=255)
    members = models.ArrayField(model_container=User)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'tracker_app'

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    duration = models.IntegerField()  # in minutes
    date = models.DateField()

    def __str__(self):
        return f"{self.type} - {self.user.email}"

    class Meta:
        app_label = 'tracker_app'

class Leaderboard(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    points = models.IntegerField()

    def __str__(self):
        return f"{self.team.name} - {self.points} points"

    class Meta:
        app_label = 'tracker_app'

class Workout(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.IntegerField()  # in minutes

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'tracker_app'
