import csv
import os
from ..app.models import Subject

os.chdir(os.getcwd())
with open('subject_details.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        p = Subject(subject_code = row['subject_code'], subject_name = row['subject_name'], teacher_name = row['teacher_name'], description = row['description'], department = row['department'], syllabus = row['syllabus'], year = row['year'], semester = row['semester'], ltp = row['ltp'], credit = row['credit'])
        p.save()