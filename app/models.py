from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    USER_TYPE = (('necta', 'necta'), ('admin', 'admin'))
    type = models.CharField(max_length=20, choices=USER_TYPE)
    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'


class Mkoa(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'mkoa'


class Wilaya(models.Model):
    name = models.CharField(max_length=30)
    mkoa_id = models.ForeignKey(Mkoa, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.mkoa_id.name} - {self.name}'

    class Meta:
        db_table = 'wilaya'


class Kata(models.Model):
    name = models.CharField(max_length=30)
    wilaya_id = models.ForeignKey(Wilaya, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'kata'


class School(models.Model):
    my_types = (('ward', 'ward'), ('special', 'special'), ('technical', 'technical'))
    gender = (('male', 'male'), ('female', 'female'), ('mixture', 'mixture'))
    name = models.CharField(max_length=30)
    wilaya_id = models.ForeignKey(Wilaya, on_delete=models.CASCADE)
    type = models.CharField(max_length=30, choices=my_types)
    sex = models.CharField(max_length=20, choices=gender)
    capacity = models.IntegerField()
    avarage_marks = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'school'


class QuantityRequired(models.Model):
    quantity = models.IntegerField()
    school_id = models.ForeignKey(School, on_delete=models.CASCADE)
    year = models.CharField(max_length=4)

    def __str__(self):
        return f'{self.school_id.name} => {str(self.quantity)}'

    class Meta:
        db_table = 'quantity'


class Year(models.Model):
    year = models.CharField(max_length=4)

    def __str__(self):
        return f'{self.year}'

    class Meta:
        db_table = 'year'


class Student(models.Model):
    gender = (('male', 'male'), ('female', 'female'))
    candidate_name = models.CharField(max_length=200)
    candidate_number = models.CharField(max_length=200)
    sex = models.CharField(max_length=20, choices=gender)
    kiswahili = models.CharField(max_length=1)
    english = models.CharField(max_length=1)
    maarifa = models.CharField(max_length=1)
    hisabati = models.CharField(max_length=1)
    science = models.CharField(max_length=1)
    average_grade = models.CharField(max_length=1)
    average_marks = models.FloatField()
    wilaya_id = models.ForeignKey(Wilaya, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.candidate_name} has average score {self.average_marks} which is {self.average_grade}'

    class Meta:
        db_table = 'student'


class StudentSchool(models.Model):
    school_id = models.ForeignKey(School, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.school_id.name} has {self.student_id.candidate_name}'

    class Meta:
        db_table = 'student_school'


class Allocation(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)

    def __str__(self):
        return f''

    class Meta:
        db_table = 'allocation'


class Selection(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)

    def __str__(self):
        return f''

    class Meta:
        db_table = 'selection'
