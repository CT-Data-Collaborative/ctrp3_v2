    # reports / queryset_helpers.py
from datetime import datetime,timedelta
from itertools import product, chain
from collections import defaultdict, OrderedDict
from functools import reduce

from django.db import models
from django.db.models import Avg, Count, Sum, Q, Value, CharField
from django.db import connection
from django.urls import reverse_lazy

import operator
import calendar
import maya

race_choices = {'A': "Asian Non-Hispanic", "B": "Black Non-Hispanic", "I": "Indian American / Alaskan Native Non-Hispanic", 'W': "White Non-Hispanic"}
race_list = ['Asian Non-Hispanic', 'Black Non-Hispanic', 'Indian American / Alaskan Native Non-Hispanic', 'White Non-Hispanic']
ethnicity_choices = {'H': "Hispanic", "M": "Middle Eastern", "N": "Not Applicable"}
ethnicity_list = ['Hispanic', 'Middle Eastern', 'Not Applicable']
RACE_AND_ETHNICITY_ROWS = ['Total', 'White Non-Hispanic', 'Black Non-Hispanic', 'Asian Non-Hispanic',
                      'Indian American / Alaskan Native Non-Hispanic', 'Hispanic']


def format_month(date_str):
    if date_str is None:
        return 'No Month Recorded'
    return f'{calendar.month_name[date_str.month]} {date_str.year}'

def format_hour(start):
    if start is None:
        return 'No Hour Recorded'
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

def exclude_age_function(row):
    if row['age_bucket'] == 5:
        return True
    else:
        return False

def structure_results(totals_qs, race_qs, ethnicity_qs, final_data_container, totals_lookup, column_getter, exclude=None, count_key=None):

    all_results = list(chain(totals_qs, race_qs, ethnicity_qs))

    for row in all_results:
        if exclude:
            if exclude(row):
                continue

        if count_key:
            count = row[count_key]
        else:
            count = row['count']

        col_val = column_getter(row)

        if 'subject_race_code' in row:
            race_ethnicity = race_choices[row['subject_race_code']]
        elif 'subject_ethnicity_code' in row:
            race_ethnicity = ethnicity_choices[row['subject_ethnicity_code']]
        else:
            race_ethnicity = 'Total'
        total = totals_lookup[race_ethnicity]
        percent = round(count / total * 100, 1)
        try:
            final_data_container[race_ethnicity][col_val]['count'] = count
            final_data_container[race_ethnicity][col_val]['percent'] = percent
        except KeyError:
            pass

    return final_data_container

def build_total_lookup(total_count, totals_by_race, totals_by_ethnicity):
    totals_lookup = {'Total': total_count}
    for t in totals_by_race:
        race = race_choices[t['subject_race_code']]
        totals_lookup[race] = t['count']
    for t in totals_by_ethnicity:
        ethnicity = ethnicity_choices[t['subject_ethnicity_code']]
        totals_lookup[ethnicity] = t['count']
    return totals_lookup

def build_final_data_container(column_list):
    final_data_container = OrderedDict()
    for r in RACE_AND_ETHNICITY_ROWS:
        row = {'race/ethnicity': r}
        for c in column_list:
            row[c] = {'count': -999, 'percent': -999}
        final_data_container[r] = row
    return final_data_container

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
        ('Statutory Authority Cited for Stop', 'stop_authority'),
        ('Residency Information', 'residency'),
        ('Stops by Month', 'stops_by_month'),
        ('Stops by Hour', 'stops_by_hour')
    ]

    links = OrderedDict()
    for name in url_names:
        links[name[0]] = reverse_lazy(f'reports:{name[1]}').__str__()

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


class StopsQueryset(models.QuerySet):

    # TODOS Refactor traffic_stops, stop_enforcement to use new query structure
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
        query_parameters = qb(**kwargs)

        try:
            filtered_partial = self.filter(reduce(operator.and_, query_parameters))
        except TypeError:
            filtered_partial = self


        total_count = filtered_partial.exclude(state_resident=None).count()
        if total_count == 0:
            return [{'column': 'CT Resident', 'count': -999, 'percent': -999}]

        resident_count = filtered_partial.filter(state_resident=True).count()

        final_results = [{'column': 'CT Resident',
                          'count': resident_count,
                          'percent': round(100*resident_count / total_count, 1)}]

        return final_results

    def town_resident(self, **kwargs):
        query_parameters = qb(**kwargs)

        try:
            filtered_partial = self.filter(reduce(operator.and_, query_parameters))
        except TypeError:
            filtered_partial = self

        total_count = filtered_partial.exclude(town_resident=None).count()
        if total_count == 0:
            return [{'column': 'Town/City Resident', 'count': -999, 'percent': -999}]
        resident_count = filtered_partial.filter(town_resident=True).count()

        final_results = [{'column': 'Town/City Resident',
                          'count': resident_count,
                          'percent': round(100*resident_count / total_count, 1)}]
        return final_results

    def nature_of_stops(self, **kwargs):
        reason_choices = {'I': "Investigative", "V": "Motor Vehicle", "E": "Equipment"}
        column_list = ['Investigative', 'Motor Vehicle', 'Equipment']
        query_parameters = qb(**kwargs)

        final_data_container = build_final_data_container(column_list)

        try:
            filtered_partial = self.filter(reduce(operator.and_, query_parameters))
        except TypeError:
            filtered_partial = self

        total_count = filtered_partial.exclude(stop_reason_code='').count()
        if total_count == 0:
            return [v for k, v in final_data_container.items()]

        totals = filtered_partial.exclude(stop_reason_code='').\
            values('stop_reason_code').\
            annotate(count=Count('stop_reason_code'))
        rqs = filtered_partial.exclude(stop_reason_code='')\
            .values('stop_reason_code', 'subject_race_code')\
            .annotate(count=Count('stop_reason_code'))
        eqs = filtered_partial.exclude(stop_reason_code='')\
            .exclude(subject_ethnicity_code='N')\
            .values('stop_reason_code', 'subject_ethnicity_code')\
            .annotate(count=Count('stop_reason_code'))

        totals_lookup = {x['stop_reason_code']: x['count'] for x in totals}

        totals_by_stop_reason = [{'count': x['count'], 'column': reason_choices[x['stop_reason_code']], \
               'race/ethnicity': 'Total', 'percent': 100.0}
              for x in totals]

        race_by_stop_reason = [{'count': x['count'], 'column': reason_choices[x['stop_reason_code']],
               'race/ethnicity': race_choices[x['subject_race_code']],
               'percent': round(100.0 * (1.0 * x['count']) / totals_lookup[x['stop_reason_code']], 1)}
              for x in rqs]

        ethnicity_by_stop_reason = [{'count': x['count'], 'column': reason_choices[x['stop_reason_code']],
               'race/ethnicity': ethnicity_choices[x['subject_ethnicity_code']],
               'percent': round(100.0 * (1.0 * x['count']) / totals_lookup[x['stop_reason_code']], 1)}
              for x in eqs]

        for row in totals_by_stop_reason+race_by_stop_reason+ethnicity_by_stop_reason:
            race = row['race/ethnicity']
            stop_reason = row['column']
            try:
                final_data_container[race][stop_reason]['count'] = row['count']
                final_data_container[race][stop_reason]['percent'] = row['percent']
            except KeyError:
                pass

        return [v for k,v in final_data_container.items()]

    def disposition_of_stops(self, **kwargs):

        disposition_code_key = {'V': 'Verbal Warning', 'W':'Written Warning', 'I':'Infraction', 'U':'UAR', 'N': 'No Disposition', 'M': 'Mis. Summons'}
        column_list = ['Verbal Warning', 'Written Warning', 'Infraction', 'UAR', 'Mis. Summons', 'No Disposition']

        query_parameters = qb(**kwargs)

        final_data_container = build_final_data_container(column_list)

        try:
            filtered_partial = self.filter(reduce(operator.and_, query_parameters)).\
                exclude(intervention_disposition_code='').\
                exclude(intervention_disposition_code=None)
        except TypeError:
            filtered_partial = self

        total_count = filtered_partial.count()
        if total_count == 0:
            return [v for k, v in final_data_container.items()]

        totals_by_race = filtered_partial.\
            values('subject_race_code').annotate(count=Count('subject_race_code'))
        totals_by_ethnicity = filtered_partial.\
            values('subject_ethnicity_code').annotate(count=Count('subject_ethnicity_code'))
        totals_qs = filtered_partial.\
            values('intervention_disposition_code').\
            annotate(count=Count('intervention_disposition_code'))
        race_qs = filtered_partial.exclude(subject_ethnicity_code='H').\
            values('intervention_disposition_code', 'subject_race_code').\
            annotate(count=Count('intervention_disposition_code'))
        ethnicity_qs = filtered_partial.\
            values('intervention_disposition_code', 'subject_ethnicity_code').\
            annotate(count=Count('intervention_disposition_code'))

        totals_lookup = build_total_lookup(total_count, totals_by_race, totals_by_ethnicity)

        final_data_container =  structure_results(totals_qs, race_qs, ethnicity_qs, final_data_container, totals_lookup,
                                                  lambda x: disposition_code_key[x['intervention_disposition_code']])

        return [v for k, v in final_data_container.items()]

    def statuatory_authority(self,**kwargs):

        column_list = ['Registration', 'Seatbelt', 'Equipment Violation', 'Cell Phone', 'Suspended License',
                       'Speed Related', 'Other', 'Moving Violation', 'Defective Lights', 'Display of Plates',
                       'Traffic Control Signal', 'Stop Sign', 'Window Tint']
        query_parameters = qb(**kwargs)

        final_data_container = build_final_data_container(column_list)

        try:
            filtered_partial = self.filter(reduce(operator.and_, query_parameters)).\
                exclude(statutory_reason_for_stop='')
        except TypeError:
            filtered_partial = self

        total_count = filtered_partial.count()
        if total_count == 0:
            return [v for k,v in final_data_container.items()]

        totals_by_race = filtered_partial.exclude(subject_ethnicity_code='H').\
            values('subject_race_code').\
            annotate(count=Count('subject_race_code'))

        totals_by_ethnicity = filtered_partial.\
            values('subject_ethnicity_code').\
            annotate(count=Count('subject_ethnicity_code'))

        totals_qs = filtered_partial.\
            values('statutory_reason_for_stop').\
            annotate(count=Count('statutory_reason_for_stop'))

        race_qs = filtered_partial.exclude(subject_ethnicity_code='H').\
            values('statutory_reason_for_stop', 'subject_race_code').\
            annotate(count=Count('statutory_reason_for_stop'))

        ethnicity_qs = filtered_partial.\
            values('statutory_reason_for_stop', 'subject_ethnicity_code').\
            annotate(count=Count('statutory_reason_for_stop'))

        totals_lookup = build_total_lookup(total_count, totals_by_race, totals_by_ethnicity)

        final_data_container = structure_results(totals_qs, race_qs, ethnicity_qs, final_data_container,
                                                 totals_lookup, lambda x: x['statutory_reason_for_stop'])


        return [v for k,v in final_data_container.items()]

    def stops_by_month(self,**kwargs):
        query_parameters = qb(**kwargs)
        truncate_date = connection.ops.date_trunc_sql('month', '"intervention_datetime"')

        try:
            filtered_partial = self.filter(reduce(operator.and_, query_parameters))
        except TypeError:
            filtered_partial = self

        count = filtered_partial.count()
        if count == 0:
            return [{'Results': 'No Results Found'}]

        results_queryset = filtered_partial.\
            extra({'month':truncate_date}).\
            values('month').annotate(Count('pk')).\
            order_by('month')

        final_results = [{'count': x['pk__count'], 'month': format_month(x['month'])} for x in results_queryset]
        return final_results

    def stops_by_hour(self, **kwargs):
        query_parameters = qb(**kwargs)

        try:
            filtered_partial = self.filter(reduce(operator.and_, query_parameters))
        except TypeError:
            filtered_partial = self

        count = filtered_partial.count()

        if count == 0:
            return [{'Results': 'No Results Found'}]

        results_queryset = filtered_partial.\
            extra({'hour': 'EXTRACT(hour from "intervention_datetime")'}). \
            values('hour').annotate(Count('pk')).order_by('hour')

        final_results = [{'count': x['pk__count'], 'hour': format_hour(x['hour'])} for x in results_queryset]
        return final_results

    def stops_by_age(self, **kwargs):

        age_buckets = {1: "16 to 25", 2: "25 to 40", 3: "40 to 60", 4: "60+", 5: "None"}
        column_list = ["16 to 25", "25 to 40", "40 to 60", "60+"]

        query_parameters = qb(**kwargs)

        try:
            filtered_partial = self.filter(reduce(operator.and_, query_parameters))
        except TypeError:
            filtered_partial = self

        final_data_container = build_final_data_container(column_list)

        total_count = filtered_partial.count()
        if total_count == 0:
            return [v for k, v in final_data_container.items()]

        totals_by_race = filtered_partial.\
            exclude(subject_ethnicity_code='H').\
            values('subject_race_code').\
            annotate(count=Count('subject_race_code'))

        totals_by_ethnicity = filtered_partial.\
            values('subject_ethnicity_code').\
            annotate(count=Count('subject_ethnicity_code'))

        totals_qs = filtered_partial.\
            extra(select={
                'age_bucket': '(case when "subject_age" >= 16 and "subject_age" < 25 then 1 \
                    when "subject_age" >= 25 and "subject_age" < 40 then 2 \
                    when "subject_age" >= 40 and "subject_age" < 60 then 3 \
                    when "subject_age" > 60 then 4 \
                    else 5 \
                    end)'}).\
            values('age_bucket').\
            annotate(Count('pk'))

        race_qs = filtered_partial.\
            exclude(subject_ethnicity_code='H').\
            extra(select={
                'age_bucket': '(case when "subject_age" >= 16 and "subject_age" < 25 then 1 \
                    when "subject_age" >= 25 and "subject_age" < 40 then 2 \
                    when "subject_age" >= 40 and "subject_age" < 60 then 3 \
                    when "subject_age" > 60 then 4 \
                    else 5 \
                    end)'}).\
            values('age_bucket','subject_race_code').\
            annotate(Count('pk'))

        ethnicity_qs = filtered_partial.\
            extra(select={
                'age_bucket': '(case when "subject_age" >= 16 and "subject_age" < 25 then 1 \
                    when "subject_age" >= 25 and "subject_age" < 40 then 2 \
                    when "subject_age" >= 40 and "subject_age" < 60 then 3 \
                    when "subject_age" > 60 then 4 \
                    else 5 \
                    end)'}).\
            values('age_bucket','subject_ethnicity_code').\
            annotate(Count('pk'))

        totals_lookup = build_total_lookup(total_count, totals_by_race, totals_by_ethnicity)

        final_data_container = structure_results(totals_qs,
                                                 race_qs,
                                                 ethnicity_qs,
                                                 final_data_container,
                                                 totals_lookup,
                                                 lambda x: age_buckets[x['age_bucket']],
                                                 exclude=exclude_age_function,
                                                 count_key='pk__count')

        return [v for k, v in final_data_container.items()]

    def search_information(self, **kwargs):
        column_list = ['Cars Searched', 'Consent', 'Inventory', 'Other', 'Contraband Found']

        final_data_container = build_final_data_container(column_list)

        query_parameters = qb(**kwargs)

        try:
            filtered_partial = self.filter(reduce(operator.and_, query_parameters))
        except TypeError:
            filtered_partial = self

        total_count = filtered_partial.exclude(searched__isnull=True).count()
        if total_count == 0:
            return [v for k, v in final_data_container.items()]

        totals_by_race = filtered_partial.\
            exclude(subject_ethnicity_code='H').\
            exclude(searched__isnull=True).\
            values('subject_race_code').\
            annotate(count=Count('subject_race_code'))

        totals_by_ethnicity = filtered_partial.\
            exclude(searched__isnull=True).\
            values('subject_ethnicity_code').\
            annotate(count=Count('subject_ethnicity_code'))

        totals_lookup = build_total_lookup(total_count, totals_by_race, totals_by_ethnicity)

        total_searched = filtered_partial.filter(searched=True).count()

        cars_searched_race_qs = filtered_partial.\
            exclude(subject_ethnicity_code='H').\
            filter(searched=True).\
            values('subject_race_code').\
            annotate(Count('subject_race_code')).\
            annotate(row_type=Value('Cars Searched', output_field=CharField()))

        cars_searched_ethnicity_qs = filtered_partial.\
            filter(searched=True).\
            values('subject_ethnicity_code').\
            annotate(Count('subject_ethnicity_code')). \
            annotate(row_type=Value('Cars Searched', output_field=CharField()))

        consent_total = filtered_partial.\
            filter(searched=True).\
            filter(search_authorization_code__exact='C').\
            count()

        inventory_total = filtered_partial.\
            filter(searched=True).\
            filter(search_authorization_code__exact='I').\
            count()

        other_total = filtered_partial.\
            filter(searched=True).\
            filter(search_authorization_code__exact='O').\
            count()

        contraband_found_total = filtered_partial.\
            filter(contraband_found=True).\
            count()

        # Todo: Handles 0
        final_data_container['Total']['Cars Searched']['count'] = total_searched
        final_data_container['Total']['Cars Searched']['percent'] = 100
        final_data_container['Total']['Consent']['count'] = consent_total
        final_data_container['Total']['Consent']['percent'] = 100
        final_data_container['Total']['Inventory']['count'] = inventory_total
        final_data_container['Total']['Inventory']['percent'] = 100
        final_data_container['Total']['Other']['count'] = other_total
        final_data_container['Total']['Other']['percent'] = 100
        final_data_container['Total']['Contraband Found']['count'] = contraband_found_total
        final_data_container['Total']['Contraband Found']['percent'] = 100

        consent_race = filtered_partial.\
            filter(searched=True).\
            filter(search_authorization_code__exact='C').\
            values('subject_race_code').\
            annotate(Count('subject_race_code')). \
            annotate(row_type=Value('Consent', output_field=CharField()))

        consent_ethnicity = filtered_partial. \
            filter(searched=True). \
            filter(search_authorization_code__exact='C'). \
            values('subject_ethnicity_code'). \
            annotate(Count('subject_ethnicity_code')). \
            annotate(row_type=Value('Consent', output_field=CharField()))

        inventory_race = filtered_partial.\
            filter(searched=True).\
            filter(search_authorization_code__exact='I').\
            values('subject_race_code').\
            annotate(Count('subject_race_code')). \
            annotate(row_type=Value('Inventory', output_field=CharField()))

        inventory_ethnicity = filtered_partial. \
            filter(searched=True). \
            filter(search_authorization_code__exact='I'). \
            values('subject_ethnicity_code'). \
            annotate(Count('subject_ethnicity_code')). \
            annotate(row_type=Value('Inventory', output_field=CharField()))

        other_race = filtered_partial.\
            filter(searched=True).\
            filter(search_authorization_code__exact='O').\
            values('subject_race_code').\
            annotate(Count('subject_race_code')). \
            annotate(row_type=Value('Other', output_field=CharField()))

        other_ethnicity = filtered_partial.\
            filter(searched=True). \
            filter(search_authorization_code__exact='O').\
            values('subject_ethnicity_code').\
            annotate(Count('subject_ethnicity_code')). \
            annotate(row_type=Value('Other', output_field=CharField()))

        contraband_found_race = filtered_partial.\
            filter(contraband_found=True).\
            values('subject_race_code').\
            annotate(Count('subject_race_code')). \
            annotate(row_type=Value('Contraband Found', output_field=CharField()))

        contraband_found_ethnicity= filtered_partial.\
            filter(contraband_found=True).\
            values('subject_ethnicity_code').\
            annotate(Count('subject_ethnicity_code')). \
            annotate(row_type=Value('Contraband Found', output_field=CharField()))

        results = list(chain(
            cars_searched_race_qs,
            cars_searched_ethnicity_qs,
            consent_race,
            consent_ethnicity,
            inventory_race,
            inventory_ethnicity,
            other_race,
            other_ethnicity,
            contraband_found_race,
            contraband_found_ethnicity
        ))

        for row in results:
            row_type = row['row_type']

            if 'subject_race_code' in row:
                race_ethnicity = race_choices[row['subject_race_code']]
                count = row['subject_race_code__count']
            elif 'subject_ethnicity_code' in row:
                race_ethnicity = ethnicity_choices[row['subject_ethnicity_code']]
                count = row['subject_ethnicity_code__count']

            total = totals_lookup[race_ethnicity]
            percent = round(count / total * 100, 1)
            try:
                final_data_container[race_ethnicity][row_type]['count'] = count
                final_data_container[race_ethnicity][row_type]['percent'] = percent
            except KeyError:
                pass

        return [v for k,v in final_data_container.items()]