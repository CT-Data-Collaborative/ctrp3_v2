# loader for ctrp3 data
import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from ctrp3_py3.reports.models import StopRecord
from postgres_copy import CopyMapping


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file_path', nargs="+", type=str)
        parser.add_argument('mapping', nargs="+", type=str)

    def handle(self, *args, **options):
        for file_path in options['file_path']:
            data_path = os.path.join(settings.ROOT_DIR.root, file_path)
            for map in options['mapping']:
                json_path = os.path.join(settings.ROOT_DIR.root, map)
                with open(json_path, 'r') as jsonfile:
                    filemap = json.load(jsonfile)
                    c = CopyMapping(
                        StopRecord,
                        data_path,
                        filemap
                    )
                    c.save()
