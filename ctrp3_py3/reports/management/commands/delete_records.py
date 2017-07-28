# delete data for records
# loader for ctrp3 data

from django.core.management.base import BaseCommand
from ctrp3_py3.reports.models import Department, DepartmentToOrgCrosswalk, StopRecord

class Command(BaseCommand):

    def handle(self, *args, **options):
        Department.objects.all().delete()
        DepartmentToOrgCrosswalk.objects.all().delete()
        StopRecord.objects.all().delete()
