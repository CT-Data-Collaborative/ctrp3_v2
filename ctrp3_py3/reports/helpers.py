    # reports / queryset_helpers.py
from datetime import datetime,timedelta
from itertools import product
from collections import defaultdict, OrderedDict
from functools import reduce

from django.db import models
from django.db.models import Avg, Count, Sum, Q
from django.db import connection
from django.urls import reverse_lazy

import operator
import calendar
import maya

def format_month(date_str):
    return f'{calendar.month_name[date_str.month]} {date_str.year}'

def format_hour(start):
    end = start + 1
    if start >= 12 and start < 24:
        start_str = "PM"
    else:
        start_str = "AM"
    if end >= 12 and end < 24:
        end_str = "PM"
    else:
        end_str = "AM"
    if start % 12 == 0:
        start = 12
    else:
        start = start % 12
    if end % 12 == 0:
        end = 12
    else:
        end = end % 12
    return f'{int(start)}{start_str} to {int(end)}{end_str}'

def build_api_links():
    """Generates a list of dicts containing a descriptive name and url for api view urls.

    Need to call the __str__ method on the reversed string b/c of serialization issues
    """
    url_names = [
        ('Traffic Stops', 'stops'),
        ('Stop Enforcement Method', 'stop_enforcement'),
        ('Nature of the Traffic Stop', 'nature_of_stop'),
        ('Age of the Driver', 'stops_by_age'),
        ('Search Information', 'search_information'),
        ('Disposition of the Traffic Stop', 'disposition'),
        ('Statutory Authority Cited for Stop', 'search_authority'),
        ('Residency Information', 'residency'),
        ('Stops by Month', 'stops_by_month'),
        ('Stops by Hour', 'stops_by_hour')
    ]

    links = OrderedDict()
    for name in url_names:
        links[name[0]] = reverse_lazy(f'reports:{name[1]}').__str__()

    # links = [{'name': name[0], 'url': reverse_lazy(f'reports:{name[1]}').__str__()} for name in url_names]

    return links


def build_month_list(start, end, humanize=False):
    months_choices = [start]
    current = start
    while current <= end:
        months_choices.append(current)
        current = current.add(months=1)
    if humanize:
        return human_month_list(months_choices)
    return months_choices

def human_month_list(month_list):
    return [f'{calendar.month_name[m.month]} {m.year}' for m in month_list]

# Build Q object from filters passed back via view
def qb(**kwargs):
    ql = []
    keys = sorted(kwargs.keys())
    if 'dateStart' in keys:
        start = kwargs['dateStart']
        month, year = start[0].split(' ')
        start_date = maya.when(f'12AM {month} 1, {year}', timezone='US/Eastern').datetime()
    else:
        start = None
    if 'dateEnd' in keys:
        end = kwargs['dateEnd']
        month, year = end[0].split(' ')
        temp = maya.when(f'12AM {month} 1, {year}', timezone='US/Eastern').add(months=1).subtract(days=1)
        endDate = temp.datetime()
    else:
        end = None
    if start and end:
        ql.append(Q(intervention_datetime__range=(start_date, endDate)))
    elif start:
        ql.append(Q(intervention_datetime__gte=start_date))
    elif end:
        ql.append(Q(intervention_datetime__lte=endDate))
    if 'department' in keys:
        p = kwargs['department'][0]
        ql.append(Q(org__department_id__department_name=p))
    return ql

# Take, as parameters, keys of interest
# Return list of objects to merge in
def diff(a, b):
    b = set(b)
    return [aa for aa in a if aa not in b]

# Need to modify to receive lists of possible keys for each of the two options
def find_missing(key1, key2, data):
    list_to_check = list()
    l_key1 = list(set(map(lambda x: x[key1], data)))
    l_key2 = list(set(map(lambda x: x[key2], data)))
    prod = list(product(l_key1,l_key2))
    for i in data:
        list_to_check.append((i[key1],i[key2]))
    return diff(prod, list_to_check)

def new_find_missing(key1, key2, list1, list2, data):
    prod = list(product(list1, list2))
    list_to_check = [(i[key1],i[key2]) for i in data]
    return diff(prod, list_to_check)

class DepartmentQueryset(models.QuerySet):
    def types(self):
        qs = self.all()
        l = [{'name': x.department_name, 'department_type': x.get_department_type_display()} for x in qs]
        return l

    def grouped_types(self):
        qs = self.all()
        grouped_departments = defaultdict(list)
        choice_lookup = None
        for dept in qs:
            if choice_lookup is None:
                choice_lookup = {c[0]:c[1] for c in dept.TYPE_CHOICES if c[0] != ''}
            department_type = choice_lookup[dept.department_type]
            grouped_departments[department_type].append({'name': dept.department_name, 'type': department_type})
        return grouped_departments

race_choices = {'A': "Asian Non-Hispanic", "B": "Black Non-Hispanic", "I": "Indian American / Alaskan Native Non-Hispanic", 'W': "White Non-Hispanic"}
race_list = ['Asian Non-Hispanic', 'Black Non-Hispanic', 'Indian American / Alaskan Native Non-Hispanic', 'White Non-Hispanic']
ethnicity_choices = {'H': "Hispanic", "M": "Middle Eastern", "N": "Not Applicable"}
ethnicity_list = ['Hispanic', 'Middle Eastern', 'Not Applicable']
datastructure_list = ['Total', 'White Non-Hispanic', 'Black Non-Hispanic', 'Asian Non-Hispanic',
                      'Indian American / Alaskan Native Non-Hispanic', 'Hispanic']

class StopsQueryset(models.QuerySet):
    def traffic_stops(self, **kwargs):
        q_list = qb(**kwargs)
        column_list = ["Traffic Stops"]
        sex_code_dict = {'M': 'Male', 'F': 'Female'}
        if q_list:
            total_count = self.filter(reduce(operator.and_,q_list)).count()
            if total_count == 0:
                return [{'Results': 'No Results Found'}]
            total_countby_race = self.exclude(subject_ethnicity_code='H').filter(reduce(operator.and_,q_list)).\
                values('subject_race_code').annotate(count=Count('subject_race_code'))
            total_countby_ethnicity = self.filter(reduce(operator.and_,q_list)).\
                values('subject_ethnicity_code').annotate(count=Count('subject_ethnicity_code'))
            total_count_by_gender = self.filter(reduce(operator.and_,q_list)).exclude(subject_sex_code='').\
                values('subject_sex_code').annotate(count=Count('subject_sex_code'))
        else:
            total_count = self.count()
            total_countby_race = self.exclude(subject_ethnicity_code='H').\
                values('subject_race_code').annotate(count=Count('subject_race_code'))
            total_countby_ethnicity = self.\
                values('subject_ethnicity_code').annotate(count=Count('subject_ethnicity_code'))
            total_count_by_gender = self.values('subject_sex_code').exclude(subject_sex_code='').\
                    annotate(count=Count('subject_sex_code'))

        gl = [{'count': x['count'], 'column': 'Traffic Stops',
                'race/ethnicity': sex_code_dict[x['subject_sex_code']], 'percent': round(100.0*(1.0*x['count'])/ total_count,1)}
            for x in total_count_by_gender]
        rl = [{'count': x['count'], 'column': 'Traffic Stops',
                'race/ethnicity': race_choices[x['subject_race_code']],
                'percent': round(100.0*(1.0*x['count'])/ total_count,1)}
            for x in total_countby_race]
        el = [{'count': x['count'], 'column': 'Traffic Stops',\
                'race/ethnicity': ethnicity_choices[x['subject_ethnicity_code']],
                'percent': round(100.0*(1.0*x['count'])/ total_count,1)}
            for x in total_countby_ethnicity]
        tl = [{'count': total_count, 'column': 'Traffic Stops', 'race/ethnicity': 'Total', 'percent': 100.0}]
        missing_gender = new_find_missing('column', 'race/ethnicity', column_list, ['Male', 'Female'], gl)
        missing_race = new_find_missing('column', 'race/ethnicity', column_list, race_list, rl)
        missing_ethnicity = new_find_missing('column', 'race/ethnicity', column_list, ethnicity_list, el)
        for e in missing_gender:
            gl.append({'count': -999, 'column': e[0], 'race/ethnicity': e[1], 'percent': -999})
        for e in missing_race:
            rl.append({'count': -999, 'column': e[0], 'race/ethnicity': e[1], 'percent': -999})
        for e in missing_ethnicity:
            el.append({'count': -999, 'column': e[0], 'race/ethnicity': e[1], 'percent': -999})
        l = tl + rl + el + gl
        return l

    def stop_enforcement(self,**kwargs):
        """Generate counts of enforcement by technique_code

        Keyword arguments:
        department -- the plain text department name
        dateRange -- a list of datetime.datetime objects
        """
        code_choices = {'G': "General", "B": "Blind", "S": "Spot-Check"}
        q_list = qb(**kwargs)
        if q_list:
            total_count = self.filter(reduce(operator.and_,q_list)).exclude(technique_code="").count()
            if total_count == 0:
                return [{'Results': 'No Results Found'}]
            qs = self.filter(reduce(operator.and_,q_list)).exclude(technique_code="").values('technique_code')\
                .annotate(num_by_tech=Count('technique_code'))
            qs = [x for x in qs if x['technique_code'] is not None]
        else:
            total_count = self.exclude(technique_code="").count()
            qs = self.exclude(technique_code="").values('technique_code')\
                .annotate(num_by_tech=Count('technique_code'))
            qs = [x for x in qs if x['technique_code'] is not None]
        l = [{'column': code_choices[x['technique_code']], 'count': x['num_by_tech'], 'percent': round(100.0*(1.0*x['num_by_tech']) / total_count, 1)}
            for x in qs]
        return l

    def resident(self, **kwargs):
        q_list = qb(**kwargs)
        if q_list:
            total_count = self.filter(reduce(operator.and_,q_list)).exclude(state_resident=None).count()
            if total_count == 0:
                return [{'Results': 'No Results Found'}]
            qs = self.filter(reduce(operator.and_,q_list)).filter(state_resident=True).count()
        else:
            total_count = self.exclude(state_resident=None).count()
            qs = self.filter(state_resident=True).count()
        l = [{'column': 'CT Resident', 'count': qs, 'percent': round(100.0*(1.0*qs) / total_count, 1)}]
        return l

    def town_resident(self, **kwargs):
        q_list = qb(**kwargs)
        if q_list:
            total_count = self.filter(reduce(operator.and_,q_list)).exclude(town_resident=None).count()
            if total_count == 0:
                return [{'Results': 'No Results Found'}]
            qs = self.filter(reduce(operator.and_,q_list)).filter(town_resident=True).count()
        else:
            total_count = self.exclude(town_resident=None).count()
            qs = self.filter(town_resident=True).count()
        l = [{'column': 'Town/City Resident', 'count': qs, 'percent': round(100.0*(1.0*qs) / total_count, 1)}]
        return l

    def nature_of_stops(self, **kwargs):
        reasonChoices = {'I': "Investigative", "V": "Motor Vehicle", "E": "Equipment"}
        column_list = ['Investigative', 'Motor Vehicle', 'Equipment']
        q_list = qb(**kwargs)
        if q_list:
            total_count = self.filter(reduce(operator.and_,q_list)).exclude(stop_reason_code='').count()
            if total_count == 0:
                return [{'Results': 'No Results Found'}]
            total_countby_race = self.filter(reduce(operator.and_,q_list)).exclude(stop_reason_code='').\
                exclude(subject_ethnicity_code='H').values('subject_race_code').annotate(count=Count('subject_race_code'))
            total_countby_ethnicity = self.filter(reduce(operator.and_,q_list)).exclude(stop_reason_code='').\
                values('subject_ethnicity_code').annotate(count=Count('subject_ethnicity_code'))
            totals = self.filter(reduce(operator.and_,q_list)).exclude(stop_reason_code='').\
                values('stop_reason_code').\
                annotate(count=Count('stop_reason_code'))
            rqs = self.filter(reduce(operator.and_,q_list)).exclude(stop_reason_code='')\
                .values('stop_reason_code', 'subject_race_code')\
                .annotate(count=Count('stop_reason_code'))
            eqs = self.filter(reduce(operator.and_,q_list)).exclude(stop_reason_code='')\
                .exclude(subject_ethnicity_code='N')\
                .values('stop_reason_code', 'subject_ethnicity_code')\
                .annotate(count=Count('stop_reason_code'))
        else:
            total_count = self.exclude(stop_reason_code='').count()
            total_countby_race = self.exclude(stop_reason_code='').exclude(subject_ethnicity_code='H').\
                values('subject_race_code').annotate(count=Count('subject_race_code'))
            total_countby_ethnicity = self.exclude(stop_reason_code='').\
                values('subject_ethnicity_code').annotate(count=Count('subject_ethnicity_code'))
            totals = self.exclude(stop_reason_code='').\
                values('stop_reason_code').\
                annotate(count=Count('stop_reason_code'))
            rqs = self.exclude(stop_reason_code='').exclude(subject_ethnicity_code='H').\
                values('stop_reason_code', 'subject_race_code').\
                annotate(count=Count('stop_reason_code'))
            eqs = self.exclude(stop_reason_code='')\
                .exclude(subject_ethnicity_code='N')\
                .values('stop_reason_code', 'subject_ethnicity_code')\
                .annotate(count=Count('stop_reason_code'))


        totals_lookup = {x['stop_reason_code']: x['count'] for x in totals}
        tl = [{'count': x['count'], 'column': reasonChoices[x['stop_reason_code']], \
               'race/ethnicity': 'Total', 'percent': 100.0}
              for x in totals]

        missing_total = new_find_missing('column', 'race/ethnicity', column_list, ['Total'], tl)
        for e in missing_total:
            tl.append({'count': -999, 'column': e[0], 'race/ethnicity': e[1], 'percent': -999})

        rl = [{'count': x['count'], 'column': reasonChoices[x['stop_reason_code']],
               'race/ethnicity': race_choices[x['subject_race_code']],
               'percent': round(100.0 * (1.0 * x['count']) / totals_lookup[x['stop_reason_code']], 1)}
              for x in rqs]
            # 'percent': round(100.0*(1.0*x['count'])/ tcr[x['subject_race_code']],1)}

        missing_race = new_find_missing('column', 'race/ethnicity', column_list, race_list, rl)
        for e in missing_race:
            rl.append({'count': -999, 'column': e[0], 'race/ethnicity': e[1], 'percent': -999})

        el = [{'count': x['count'], 'column': reasonChoices[x['stop_reason_code']],
               'race/ethnicity': ethnicity_choices[x['subject_ethnicity_code']],
               'percent': round(100.0 * (1.0 * x['count']) / totals_lookup[x['stop_reason_code']], 1)}
              for x in eqs]
               # 'percent': round(100.0*(1.0*x['count'])/ tce[x['subject_ethnicity_code']],1)}

        missing_ethnicity = new_find_missing('column', 'race/ethnicity', column_list, ethnicity_list, el)
        for e in missing_ethnicity:
            el.append({'count': -999, 'column': e[0], 'race/ethnicity': e[1], 'percent': -999})

        final_data = OrderedDict()
        for r in datastructure_list:
            row = { 'race/ethnicity': r }
            for c in column_list:
                row[c] = { 'count': -999, 'percent': -999 }
            final_data[r] = row
        for row in tl+rl+el:
            race = row['race/ethnicity']
            stop_reason = row['column']
            try:
                final_data[race][stop_reason]['count'] = row['count']
                final_data[race][stop_reason]['percent'] = row['percent']
            except KeyError:
                pass

        return [v for k,v in final_data.items()]

    def disposition_of_stops(self, **kwargs):
        dispositionCodeKey = {'V': 'Verbal Warning', 'W':'Written Warning', 'I':'Infraction', 'U':'UAR', 'N': 'No Disposition', 'M': 'Mis. Summons'}
        exclude_list = ['', None]
        q_list = qb(**kwargs)
        filters = reduce(operator.and_,q_list)
        if q_list:
            total_count = self.filter(filters).exclude(intervention_disposition_code='').exclude(intervention_disposition_code=None).count()
            if total_count == 0:
                return [{'Results': 'No Results Found'}]
            total_countby_race = self.exclude(subject_ethnicity_code='H').filter(filters).exclude(intervention_disposition_code='').exclude(intervention_disposition_code=None).\
                values('subject_race_code').annotate(count=Count('subject_race_code'))
            total_countby_ethnicity = self.filter(filters).exclude(intervention_disposition_code='').exclude(intervention_disposition_code=None).\
                values('subject_ethnicity_code').annotate(count=Count('subject_ethnicity_code'))
            totals = self.filter(filters).exclude(intervention_disposition_code='').exclude(intervention_disposition_code=None).\
                values('intervention_disposition_code').\
                annotate(count=Count('intervention_disposition_code'))
            rqs = self.exclude(subject_ethnicity_code='H').filter(filters).exclude(intervention_disposition_code='').exclude(intervention_disposition_code=None).\
                values('intervention_disposition_code', 'subject_race_code').\
                annotate(count=Count('intervention_disposition_code'))
            eqs = self.filter(filters).exclude(intervention_disposition_code='').exclude(intervention_disposition_code=None).\
                values('intervention_disposition_code', 'subject_ethnicity_code').\
                annotate(count=Count('intervention_disposition_code'))
        else:
            total_count = self.exclude(intervention_disposition_code='').exclude(intervention_disposition_code=None).count()
            total_countby_race = self.exclude(subject_ethnicity_code='H').exclude(intervention_disposition_code='').exclude(intervention_disposition_code=None).\
                values('subject_race_code').annotate(count=Count('subject_race_code'))
            total_countby_ethnicity = self.exclude(intervention_disposition_code='').exclude(intervention_disposition_code=None).\
                values('subject_ethnicity_code').annotate(count=Count('subject_ethnicity_code'))
            totals = self.exclude(intervention_disposition_code='').exclude(intervention_disposition_code=None).\
                values('intervention_disposition_code').\
                annotate(count=Count('intervention_disposition_code'))
            rqs = self.exclude(subject_ethnicity_code='H').exclude(intervention_disposition_code='').exclude(intervention_disposition_code=None).\
                values('intervention_disposition_code', 'subject_race_code').\
                annotate(count=Count('intervention_disposition_code'))
            eqs = self.exclude(intervention_disposition_code='').exclude(intervention_disposition_code=None).\
                values('intervention_disposition_code', 'subject_ethnicity_code').\
                annotate(count=Count('intervention_disposition_code'))
        totals = [x for x in totals if x['intervention_disposition_code'] is not None]
        tcr = dict((x['subject_race_code'], x['count']) for x in total_countby_race)
        tce = dict((x['subject_ethnicity_code'], x['count']) for x in total_countby_ethnicity)
        tl = [{'count': x['count'], 'column': dispositionCodeKey[x['intervention_disposition_code']],\
                'race/ethnicity': 'Total', 'percent': round(100.0*(1.0*x['count'])/ total_count,1)}
            for x in totals]
        rl = [{'count': x['count'], 'column': dispositionCodeKey[x['intervention_disposition_code']],\
                'race/ethnicity': race_choices[x['subject_race_code']], 'percent': round(100.0*(1.0*x['count'])/ tcr[x['subject_race_code']],1)}
            for x in rqs]
        el = [{'count': x['count'], 'column': dispositionCodeKey[x['intervention_disposition_code']],\
                'race/ethnicity': ethnicity_choices[x['subject_ethnicity_code']], 'percent': round(100.0*(1.0*x['count'])/ tce[x['subject_ethnicity_code']],1)}
            for x in eqs]
        column_list = ['Verbal Warning', 'Written Warning', 'Infraction', 'UAR', 'No Disposition', 'Mis. Summons']
        missing_total = new_find_missing('column', 'race/ethnicity', column_list, ['Total'], tl)
        missing_race = new_find_missing('column', 'race/ethnicity', column_list, race_list, rl)
        missing_ethnicity = new_find_missing('column', 'race/ethnicity', column_list, ethnicity_list, el)
        for e in missing_total:
            tl.append({'count': -999, 'column': e[0], 'race/ethnicity': e[1], 'percent': -999})
        for e in missing_race:
            rl.append({'count': -999, 'column': e[0], 'race/ethnicity': e[1], 'percent': -999})
        for e in missing_ethnicity:
            el.append({'count': -999, 'column': e[0], 'race/ethnicity': e[1], 'percent': -999})
        l = tl + rl + el
        return l

    def statuatory_authority(self,**kwargs):
        q_list = qb(**kwargs)
        if q_list:
            total_count = self.filter(reduce(operator.and_,q_list)).exclude(statutory_reason_for_stop='').count()
            if total_count == 0:
                return [{'Results': 'No Results Found'}]
            total_countby_race = self.exclude(subject_ethnicity_code='H').filter(reduce(operator.and_,q_list)).exclude(statutory_reason_for_stop='').\
                values('subject_race_code').annotate(count=Count('subject_race_code'))
            total_countby_ethnicity = self.filter(reduce(operator.and_,q_list)).exclude(statutory_reason_for_stop='').\
                values('subject_ethnicity_code').annotate(count=Count('subject_ethnicity_code'))
            totals = self.filter(reduce(operator.and_,q_list)).exclude(statutory_reason_for_stop='').\
                values('statutory_reason_for_stop').\
                annotate(count=Count('statutory_reason_for_stop'))
            rqs = self.exclude(subject_ethnicity_code='H').filter(reduce(operator.and_,q_list)).exclude(statutory_reason_for_stop='').\
                values('statutory_reason_for_stop', 'subject_race_code').\
                annotate(count=Count('statutory_reason_for_stop'))
            eqs = self.filter(reduce(operator.and_,q_list)).exclude(statutory_reason_for_stop='').\
                values('statutory_reason_for_stop', 'subject_ethnicity_code').\
                annotate(count=Count('statutory_reason_for_stop'))
        else:
            total_count = self.exclude(statutory_reason_for_stop='').count()
            total_countby_race = self.exclude(subject_ethnicity_code='H').exclude(statutory_reason_for_stop='').\
                values('subject_race_code').annotate(count=Count('subject_race_code'))
            total_countby_ethnicity = self.exclude(statutory_reason_for_stop='').\
                values('subject_ethnicity_code').annotate(count=Count('subject_ethnicity_code'))
            totals = self.exclude(statutory_reason_for_stop='').\
                values('statutory_reason_for_stop').\
                annotate(count=Count('statutory_reason_for_stop'))
            rqs = self.exclude(subject_ethnicity_code='H').exclude(statutory_reason_for_stop='').\
                values('statutory_reason_for_stop', 'subject_race_code').\
                annotate(count=Count('statutory_reason_for_stop'))
            eqs = self.exclude(statutory_reason_for_stop='').\
                values('statutory_reason_for_stop', 'subject_ethnicity_code').\
                annotate(count=Count('statutory_reason_for_stop'))
        column_list = ['Registration', 'Seatbelt', 'Equipment Violation','Cell Phone','Suspended License', 'Speed Related', 'Other', 'Moving Violation', 'Defective Lights', 'Display of Plates', 'Traffic Control Signal', 'Stop Sign', 'Window Tint']
        tcr = dict((x['subject_race_code'], x['count']) for x in total_countby_race)
        tce = dict((x['subject_ethnicity_code'], x['count']) for x in total_countby_ethnicity)
        tl = [{'count': x['count'], 'column': x['statutory_reason_for_stop'],\
                'race/ethnicity': 'Total', 'percent': round(100.0*(1.0*x['count'])/ total_count,1)}
            for x in totals]
        missing_total = new_find_missing('column', 'race/ethnicity', column_list, ['Total'], tl)
        for e in missing_total:
            tl.append({'count': -999, 'column': e[0], 'race/ethnicity': e[1], 'percent': -999})
        rl = [{'count': x['count'], 'column': x['statutory_reason_for_stop'], 'race/ethnicity': race_choices[x['subject_race_code']], 'percent': round(100.0*(1.0*x['count'])/ tcr[x['subject_race_code']],1)}
            for x in rqs]
        el = [{'count': x['count'], 'column': x['statutory_reason_for_stop'], 'race/ethnicity': ethnicity_choices[x['subject_ethnicity_code']], 'percent': round(100.0*(1.0*x['count'])/ tce[x['subject_ethnicity_code']],1)}
            for x in eqs]
        missing_race = new_find_missing('column', 'race/ethnicity', column_list, race_list, rl)
        missing_ethnicity = new_find_missing('column', 'race/ethnicity', column_list, ethnicity_list, el)
        for e in missing_race:
            rl.append({'count': -999, 'column': e[0], 'race/ethnicity': e[1], 'percent': -999})
        for e in missing_ethnicity:
            el.append({'count': -999, 'column': e[0], 'race/ethnicity': e[1], 'percent': -999})
        l = tl + rl + el
        return l

    def stops_by_month(self,**kwargs):
        q_list = qb(**kwargs)
        truncate_date = connection.ops.date_trunc_sql('month', '"intervention_datetime"')
        if q_list:
            count = self.filter(reduce(operator.and_,q_list)).count()
            if count == 0:
                return [{'Results': 'No Results Found'}]
            qs = self.filter(reduce(operator.and_,q_list)).extra({'month':truncate_date}).\
                values('month').annotate(Count('pk')).order_by('month')
        else:
            qs = self.extra({'month':truncate_date}).values('month').\
                annotate(Count('pk')).order_by('month')
        # l = [{'count': x['pk__count'], 'month': str(x['month'])} for x in qs]
        l = [{'count': x['pk__count'], 'month': format_month(x['month'])} for x in qs]
        return l


    def stops_by_hour(self, **kwargs):
        q_list = qb(**kwargs)

        if q_list:
            count = self.filter(reduce(operator.and_,q_list)).count()
            if count == 0:
                return [{'Results': 'No Results Found'}]
            qs = self.filter(reduce(operator.and_,q_list)).extra({'hour': 'EXTRACT(hour from "intervention_datetime")'}).\
                values('hour').annotate(Count('pk')).order_by('hour')

        else:
            qs = self.extra({'hour': 'EXTRACT(hour from "intervention_datetime")'}).values('hour').\
                annotate(Count('pk')).order_by('hour')
        l = [{'count': x['pk__count'], 'hour': format_hour(x['hour'])} for x in qs]
        return l


    def stops_by_age(self, **kwargs):
        age_buckets = {1: "16 to 25", 2: "25 to 40", 3: "40 to 60", 4: "60+", 5: "None"}
        race_choices = {'A': "Asian Non-Hispanic", "B": "Black Non-Hispanic", "I": "Indian American / Alaskan Native Non-Hispanic", 'W': "White Non-Hispanic"}
        ethnicity_choices = {'H': "Hispanic", "M": "Middle Eastern", "N": "Not Applicable"}
        q_list = qb(**kwargs)
        if q_list:
            total_count = self.filter(reduce(operator.and_,q_list)).count()
            if total_count == 0:
                return [{'Results': 'No Results Found'}]
            total_countby_race = self.filter(reduce(operator.and_,q_list)).exclude(subject_ethnicity_code='H').\
                values('subject_race_code').annotate(count=Count('subject_race_code'))
            total_countby_ethnicity = self.filter(reduce(operator.and_,q_list)).\
                values('subject_ethnicity_code').annotate(count=Count('subject_ethnicity_code'))
            tqs = self.filter(reduce(operator.and_,q_list)).extra(select={
                    'age_bucket': '(case when "subject_age" >= 16 and "subject_age" < 25 then 1 \
                        when "subject_age" >= 25 and "subject_age" < 40 then 2 \
                        when "subject_age" >= 40 and "subject_age" < 60 then 3 \
                        when "subject_age" > 60 then 4 \
                        else 5 \
                        end)'}).values('age_bucket').annotate(Count('pk'))
            rqs = self.filter(reduce(operator.and_,q_list)).exclude(subject_ethnicity_code='H').extra(select={
                    'age_bucket': '(case when "subject_age" >= 16 and "subject_age" < 25 then 1 \
                        when "subject_age" >= 25 and "subject_age" < 40 then 2 \
                        when "subject_age" >= 40 and "subject_age" < 60 then 3 \
                        when "subject_age" > 60 then 4 \
                        else 5 \
                        end)'}).values('age_bucket','subject_race_code').annotate(Count('pk'))
            eqs = self.filter(reduce(operator.and_,q_list)).extra(select={
                    'age_bucket': '(case when "subject_age" >= 16 and "subject_age" < 25 then 1 \
                        when "subject_age" >= 25 and "subject_age" < 40 then 2 \
                        when "subject_age" >= 40 and "subject_age" < 60 then 3 \
                        when "subject_age" > 60 then 4 \
                        else 5 \
                        end)'}).values('age_bucket','subject_ethnicity_code').annotate(Count('pk'))
        else:
            total_count = self.count()
            total_countby_race = self.values('subject_race_code').exclude(subject_ethnicity_code='H').annotate(count=Count('subject_race_code'))
            total_countby_ethnicity = self.values('subject_ethnicity_code').annotate(count=Count('subject_ethnicity_code'))
            tqs = self.extra(select={
                    'age_bucket': '(case when "subject_age" >= 16 and "subject_age" < 25 then 1 \
                        when "subject_age" >= 25 and "subject_age" < 40 then 2 \
                        when "subject_age" >= 40 and "subject_age" < 60 then 3 \
                        when "subject_age" > 60 then 4 \
                        else 5 \
                        end)'}).values('age_bucket')\
                    .annotate(Count('pk'))
            rqs = self.exclude(subject_ethnicity_code='H').extra(select={
                    'age_bucket': '(case when "subject_age" >= 16 and "subject_age" < 25 then 1 \
                        when "subject_age" >= 25 and "subject_age" < 40 then 2 \
                        when "subject_age" >= 40 and "subject_age" < 60 then 3 \
                        when "subject_age" > 60 then 4 \
                        else 5 \
                        end)'}).values('age_bucket', 'subject_race_code')\
                    .annotate(Count('pk'))
            eqs = self.extra(select={
                    'age_bucket': '(case when "subject_age" >= 16 and "subject_age" < 25 then 1 \
                        when "subject_age" >= 25 and "subject_age" < 40 then 2 \
                        when "subject_age" >= 40 and "subject_age" < 60 then 3 \
                        when "subject_age" > 60 then 4 \
                        else 5 \
                        end)'}).values('age_bucket', 'subject_ethnicity_code')\
                    .annotate(Count('pk'))
        # First we filter out age values that are "bad"
        # Then we restructure the list, calculate percents, and remap ages to strings
        tcr = dict((x['subject_race_code'], x['count']) for x in total_countby_race)
        tce = dict((x['subject_ethnicity_code'], x['count']) for x in total_countby_ethnicity)

        column_list = ["16 to 25", "25 to 40", "40 to 60", "60+"]

        tl = [item for item in tqs if(item['age_bucket'] < 5)]
        tl = [{'count': x['pk__count'], 'age': age_buckets[x['age_bucket']],\
         'race/ethnicity': 'Total', \
         'percent': round(100.0*(1.0*x['pk__count'])/ total_count,1)}
            for x in tl]

        rl = [item for item in rqs if(item['age_bucket'] < 5)]
        rl = [{'count': x['pk__count'], 'age': age_buckets[x['age_bucket']],\
         'race/ethnicity': race_choices[x['subject_race_code']], \
         'percent': round(100.0*(1.0*x['pk__count'])/ tcr[x['subject_race_code']],1)}
            for x in rl]
        missing_race = new_find_missing('age', 'race/ethnicity', column_list, race_list, rl)
        for e in missing_race:
            rl.append({'count': -999, 'age': e[0], 'race/ethnicity': e[1], 'percent': -999})
        el = [item for item in eqs if(item['age_bucket'] < 5)]
        el = [{'count': x['pk__count'], 'age': age_buckets[x['age_bucket']],\
         'race/ethnicity': ethnicity_choices[x['subject_ethnicity_code']],\
          'percent': round(100.0*(1.0*x['pk__count'])/ tce[x['subject_ethnicity_code']],1)}
            for x in el]
        missing_ethnicity = new_find_missing('age', 'race/ethnicity', column_list, ethnicity_list, el)
        for e in missing_ethnicity:
            el.append({'count': -999, 'age': e[0], 'race/ethnicity': e[1], 'percent': -999})
        l = {'total': tl, 'race': rl, 'ethnicity': el}
        return l
