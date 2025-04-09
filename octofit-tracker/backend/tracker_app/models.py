from djongo import models

# Eliminando el modelo User duplicado para evitar conflictos
# from djongo.models.fields import ObjectIdField

# class User(models.Model):
#     id = ObjectIdField(primary_key=True)
#     email = models.EmailField(unique=True)
#     name = models.CharField(max_length=100)
#     age = models.IntegerField()

#     def __str__(self):
#         return self.email
