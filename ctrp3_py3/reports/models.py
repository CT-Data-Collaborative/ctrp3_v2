# reports/models.py
from django.db import models
from .helpers import StopsQueryset, DepartmentQueryset


class Department(models.Model):
    TYPE_CHOICES = (
        ('M', 'Municipal'),
        ('T', 'State Police'),
        ('S', 'Special'),
        ('', 'None Set')
    )
    department_id = models.CharField(max_length=40, primary_key=True)
    department_name = models.CharField(max_length=50)
    department_type = models.CharField(max_length=1,
                                       choices=TYPE_CHOICES)

    # objects = PassThroughManager.for_queryset_class(DepartmentQueryset)()
    objects = DepartmentQueryset.as_manager()

    def __str__(self):
        return self.department_name


class DepartmentToOrgCrosswalk(models.Model):
    org_id = models.CharField(max_length=9, primary_key=True)
    department_id = models.ForeignKey(Department)

    def __str__(self):
        return self.org_id


class StopRecord(models.Model):
    RACE_CHOICES = (
        ('A', 'Asian/Pacific Islander'),
        ('B', 'Black'),
        ('I', 'Indian American / Alaskan Native'),
        ('W', 'White'),
        ('', 'No Data Available')
    )

    ETHNICITY_CHOICES = (
        ('H', 'Hispanic'),
        ('M', 'Middle Eastern'),
        ('N', 'Not Applicable'),
        ('', 'No Data Available')
    )

    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('', 'No Data Available')
    )

    REASON_CHOICES = (
        ('I', 'Investigation, Criminal'),
        ('V', 'Violation, Motor Vehicle'),
        ('E', 'Equipment, Motor Vehicle'),
        ('', 'No Data Available')
    )

    org = models.ForeignKey(DepartmentToOrgCrosswalk)
    intervention_id = models.TextField(blank=True, null=True)
    subject_race_code = models.CharField(max_length=1,
                                         choices=RACE_CHOICES,
                                         blank=True, null=True
                                         )

    subject_ethnicity_code = models.CharField(max_length=1,
                                              choices=ETHNICITY_CHOICES,
                                              blank=True, null=True)

    subject_sex_code = models.CharField(max_length=1,
                                        choices=SEX_CHOICES,
                                        blank=True, null=True)
    subject_age = models.IntegerField(null=True, blank=True)
    state_resident = models.NullBooleanField()
    town_resident = models.NullBooleanField()
    intervention_location = models.TextField(blank=True, null=True)
    stop_reason_code = models.CharField(max_length=1,
                                        choices=REASON_CHOICES,
                                        blank=True, null=True
                                        )
    technique_code = models.CharField(max_length=1,blank=True, null=True)
    towed = models.NullBooleanField()
    statute_id = models.TextField(blank=True, null=True)
    statutory_reason_for_stop = models.TextField(blank=True, null=True)
    statutory_citation_post_stop = models.TextField(blank=True, null=True)
    searched = models.NullBooleanField()
    SEARCH_AUTHORITY_CHOICES = (
        ('C', 'Consent'),
        ('I', 'Inventory'),
        ('O', 'Other'),
        ('N', 'Not Applicable'),
        ('', 'No Data Available')
    )
    search_authorization_code = models.CharField(max_length=1,
                                                 choices=SEARCH_AUTHORITY_CHOICES,
                                                 blank=True, null=True)
    contraband_found = models.NullBooleanField()
    custodial_arrest = models.NullBooleanField()
    DISPOSITION_CHOICES = (
        ('U', 'Uniform Arrest Report'),
        ('M', 'Misdemeanor Summons'),
        ('I', 'Infraction Ticket'),
        ('W', 'Written Warning'),
        ('V', 'Verbal Warning'),
        ('N', 'No Disposition'),
        ('', 'No Data Available')
    )
    intervention_disposition_code = models.CharField(max_length=1,
                                                     choices=DISPOSITION_CHOICES,
                                                     blank=True, null=True)
    intervention_datetime = models.DateTimeField(blank=True, null=True)

    objects = StopsQueryset.as_manager()
