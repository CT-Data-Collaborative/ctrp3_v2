# load departments for ctrp3
# loader for ctrp3 data

import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from ctrp3_py3.reports.models import Department

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file_path', nargs="+", type=str)

    def handle(self, *args, **options):
        self.stdout.write("Loading departments")
        for file_path in options['file_path']:
            data_path = os.path.join(settings.ROOT_DIR.root, file_path)
            with open(data_path, "r") as dept_file:
                csv_reader = csv.DictReader(dept_file)
                for row in csv_reader:
                    # print(row)
                    dept = Department()
                    dept.department_id = row['department_id']
                    dept.department_name = row['department_name']
                    dept.department_type =row['department_type']
                    dept.save()


