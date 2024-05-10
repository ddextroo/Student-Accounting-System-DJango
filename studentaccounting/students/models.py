from django.db import models


class Student(models.Model):
    id_number = models.PositiveIntegerField()
    first_name = models.CharField(max_length=20)
    middle_initial = models.CharField(max_length=2)
    last_name = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    email_address = models.CharField(max_length=50)
    course_name = models.CharField(max_length=250)
    year_level = models.PositiveSmallIntegerField()
    subjects = models.PositiveSmallIntegerField()
    image = models.ImageField()

    def __str__(self) -> str:
        return f"{self.first_name} {self.middle_initial} {self.last_name}"
