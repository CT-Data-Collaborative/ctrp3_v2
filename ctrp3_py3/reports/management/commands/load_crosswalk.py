# load orgMap for ctrp3
# loader for ctrp3 data

import os
from django.core.management.base import BaseCommand
from django.conf import settings
from postgres_copy import CopyMapping
from ctrp3_py3.reports.models import DepartmentToOrgCrosswalk

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file_path', nargs="+", type=str)

    def handle(self, *args, **options):
        for file_path in options['file_path']:
            data_path = os.path.join(settings.ROOT_DIR.root, file_path)
            c = CopyMapping(
                DepartmentToOrgCrosswalk,
                data_path,
                dict(org_id='org_id', department_id='department_id')
            )
            c.save()
