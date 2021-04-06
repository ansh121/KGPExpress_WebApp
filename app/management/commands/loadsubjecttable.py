from django.core.management.base import BaseCommand
import csv
import os
from app.models import Subject

class Command(BaseCommand):
    help = 'Fill "Subject" table from "<project_dir>/utils/subject_details.csv" file'

    def handle(self, *args, **kwargs):
        file_path='./utils/subject_details.csv'
        with open(file_path,'r',encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row['subject_code'])
                try:
                    p = Subject.objects.update_or_create(subject_code = row['subject_code'], subject_name = row['subject_name'], teacher_name = row['teacher_name'], description = row['description'], department = row['department'], syllabus = row['syllabus'], year = row['year'], semester = row['semester'], ltp = row['ltp'], credit = row['credit'])
                except:
                    print(row['subject_code'],row['syllabus'])
                                