from django.db import models
from django.urls import reverse
from authentication.models import CustomUser

class Subject(models.Model):
    subject_code = models.CharField(max_length=7)
    subject_name = models.CharField(max_length=120)
    teacher_name = models.CharField(max_length=100,blank=True)
    description = models.CharField(max_length=1000,blank=True)
    department = models.CharField(max_length=100)
    syllabus = models.TextField(blank=True)
    year = models.DecimalField(max_digits=4, decimal_places=0)
    ltp = models.CharField(max_length=10)
    credit = models.IntegerField()
    semester = models.CharField(max_length=10)
    subject_id = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'subject'
        unique_together = (('subject_code', 'semester', 'year'),)

class Event(models.Model):
    event_name = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.CharField(max_length=1000,blank=True)
    is_recurring = models.BooleanField(default=False)
    event_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)
    time_of_edit = models.DateTimeField()
    user = models.ForeignKey(CustomUser, models.DO_NOTHING)
    subject = models.ForeignKey(Subject, models.DO_NOTHING)

    @property
    def get_html_url(self):
        url = reverse('app:event_edit', args=(self.event_id,))
        return f'<a href="{url}"> {self.event_name} </a>'

class History(models.Model):
    time_of_edit = models.DateTimeField(primary_key=True)
    event_name = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    type = models.CharField(max_length=50)
    is_recurring = models.BooleanField(default=False)
    description = models.CharField(max_length=1000,blank=True)
    event_id = models.IntegerField()
    user = models.OneToOneField(CustomUser, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'history'
        unique_together = (('time_of_edit', 'user'),)


class RegisteredSubjects(models.Model):
    user = models.ForeignKey(CustomUser, models.DO_NOTHING)
    subject = models.ForeignKey(Subject, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'registered_subjects'
        unique_together = (('user', 'subject'),)


# class Event(models.Model):
#     title = models.CharField(max_length=200)
#     subject = models.CharField(max_length=50)
#     description = models.TextField()
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()
#
#     @property
#     def get_html_url(self):
#         url = reverse('app:event_edit', args=(self.id,))
#         return f'<a href="{url}"> {self.title} </a>'