import json

from collections import OrderedDict

from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.urls import reverse_lazy

from .models import StopRecord, Department
from .helpers import build_month_list, build_api_links


class JSONResponse(HttpResponse):
    '''
    A HttpResponse that renders contents to JSON
    '''

    def __init__(self, data, **kwargs):
        content = json.dumps(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def report_tables(request):
    """View for tables page. Can also be initiated with data if the user comes to page from homepage

    """
    department_by_type = Department.objects.grouped_types()
    start_date = settings.DATA_START_DATE
    end_date = settings.DATA_END_DATE
    month_list = build_month_list(start_date, end_date, humanize=True)
    api_links = build_api_links()
    api_data = OrderedDict()
    for l, u in api_links.items():
        api_data[l] = []

    context = {
        'departments': json.dumps(department_by_type),
        'start_date': month_list[0],
        'end_date': month_list[-1],
        'month_list': json.dumps(month_list),
        'api_links': json.dumps(api_links),
        'api_data': json.dumps(api_data)
    }
    # Probably a ogod idea to consider refactoring this in to a form for proper validation
    if request.method == 'POST':
        try:
            found_dept = Department.objects.get(department_name=request.POST.get('department'))
        except Department.DoesNotExist:
            pass

        if found_dept:
            context['selected_department'] = found_dept.department_name
            context['selected_department_type'] = found_dept.get_department_type_display()

        submitted_start_date = request.POST.get('start_date', None)

        if submitted_start_date and submitted_start_date in month_list:
            context['start_date'] = submitted_start_date

        submitted_end_date = request.POST.get('end_date', None)

        if submitted_end_date and submitted_end_date in month_list:
            context['end_date'] = submitted_end_date

    return render(request, 'reports/tables.html', context)

def scatter_plots(request):
    context = {}
    return render(request, 'reports/plots.html', context)

def department_json_view(request):
    if request.method == 'GET':
        data = Department.objects.types()
    else:
        data = 'fail'
    return JSONResponse(data)

def stop_enforcement_json_view(request):
    if request.method == 'GET':
        data = StopRecord.objects.stop_enforcement(**request.GET)
    else:
        data = 'fail'
    return JSONResponse(data)

def stops_by_age_json_view(request):
    if request:
        data = StopRecord.objects.stops_by_age(**request.GET)
    else:
        data = 'fail'
    return JSONResponse(data)

def nature_of_stops_json_view(request):
    if request:
        data = StopRecord.objects.nature_of_stops(**request.GET)
    else:
        data = 'fail'
    return JSONResponse(data)

def resident_json_view(request):
    if request:
        state = StopRecord.objects.resident(**request.GET)
        town = StopRecord.objects.town_resident(**request.GET)
        data = state + town
    else:
        data = 'fail'
    return JSONResponse(data)

def disposition_json_view(request):
    if request:
        data = StopRecord.objects.disposition_of_stops(**request.GET)
    else:
        data = 'fail'
    return JSONResponse(data)

def statutory_authority_json_view(request):
    if request:
        data = StopRecord.objects.statuatory_authority(**request.GET)
    else:
        data = 'fail'
    return JSONResponse(data)

def monthly_stops_json_view(request):
    if request:
        data = list(StopRecord.objects.stops_by_month(**request.GET))
    else:
        data = 'fail'
    return JSONResponse(data)

def stops_by_hour_json_view(request):
    if request:
        data = list(StopRecord.objects.stops_by_hour(**request.GET))
    else:
        data = 'fail'
    return JSONResponse(data)

def traffic_stops_json_view(request):
    if request:
        data = list(StopRecord.objects.traffic_stops(**request.GET))
    else:
        data = 'fail'
    return JSONResponse(data)

def search_information_json_view(request):
    if request:
        data = list(StopRecord.objects.search_information(**request.GET))
    else:
        data = 'fail'
    return JSONResponse(data)

def search_authority_json_view(request):
    if request:
        data = StopRecord.objects.search_authority()
    else:
        data = 'fail'
    return JSONResponse(data)
