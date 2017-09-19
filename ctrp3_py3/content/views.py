import json
from django.shortcuts import render
from django.conf import settings
from .models import HomePage
from ctrp3_py3.reports.models import Department
from ctrp3_py3.reports.helpers import build_month_list

def home_page(request):
    home_page_content = HomePage.load()
    department_by_type = Department.objects.grouped_types()
    start_date = settings.DATA_START_DATE
    end_date = settings.DATA_END_DATE
    month_list = build_month_list(start_date, end_date, humanize=True)
    context = {
        # 'about': home_page_content.about__markdownify
        'start': start_date.datetime(),
        'end': end_date.datetime(),
        'departments': json.dumps(department_by_type),
        'start_date': start_date.iso8601(),
        'end_date': end_date.iso8601(),
        'month_list': json.dumps(month_list),

    }
    return render(request, 'content/home.html', context)
