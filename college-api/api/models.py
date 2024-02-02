from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.


class Student(models.Model):
    name = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    email = models.EmailField(max_length=30)
    cellphone = models.CharField(max_length=15)


class Career(models.Model):
    name = models.CharField(max_length=20)


class Subject(models.Model):
    name = models.CharField(max_length=20)
    career = models.ForeignKey(Career, on_delete=models.CASCADE)


class Classroom(models.Model):
    name = models.CharField(max_length=10)


class Embedding(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    embedding = ArrayField(models.FloatField(), size=512, default=list)


class SubjectSchedule(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    weekday = models.PositiveSmallIntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()


class AttendanceControl(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateTimeField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assistance = models.BooleanField()


class SubjectInscription(models.Model):
    subject = models.ManyToManyField(Subject)
    student = models.ManyToManyField(Student)
