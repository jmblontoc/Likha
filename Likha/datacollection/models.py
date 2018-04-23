from django.db import models
from datetime import datetime

# Create your models here.


class AgeGroup(models.Model):

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    SEX_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)

    def __str__(self):
        return self.name + " | " + self.sex


class NutritionalStatus(models.Model):

    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "nutritional statuses"


class Barangay(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class OperationTimbang(models.Model):

    date = models.DateTimeField(default=datetime.now)
    barangay = models.ForeignKey(Barangay, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.date) + " at " + self.barangay.name


class OPTValues(models.Model):
    opt = models.ForeignKey(OperationTimbang, on_delete=models.CASCADE)
    values = models.DecimalField(decimal_places=0, max_digits=7)
    nutritional_status = models.ForeignKey(NutritionalStatus, on_delete=models.DO_NOTHING)
    age_group = models.ForeignKey(AgeGroup, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = 'OPT Values'

    def __str__(self):
        return self.nutritional_status.name + " " + self.age_group.name


# FHSIS
class FHSIS(models.Model):
    date = models.DateTimeField(default=datetime.now)
    barangay = models.ForeignKey(Barangay, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.date) + " at " + self.barangay.name

    class Meta:
        verbose_name_plural = 'FHSIS'


# data under FHSIS
class Maternal(models.Model):
    fhsis = models.ForeignKey(FHSIS, on_delete=models.CASCADE)

    # pregnant women
    women_with_4_or_more_prenatal_visits = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Pregnant women with 4 or more Prenatal Visits")
    women_given_2_tt_doses = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Pregnant women given 2 doses of Tetanus Toxoid")
    women_given_tt2plus = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Pregnant women given TT2 plus")
    women_given_iron_with_supplementation = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Pregnant women given complete iron with folic acid supplementation")

    # postpartum
    women_with_atleast_2_postpartum_visits = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Postpartum women with at least 2 postpartum visits")
    women_with_vitamin_A = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Postpartum women given Vitamin A supplementation")
    women_breastfed_1_hour_after_delivery = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Postpartum women initiated breastfeeding within 1 hour after delivery")

    # 10-49 years
    women_given_iron = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Women 10-49 years old given iron supplementation")
    deliveries = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Deliveries")

    def __str__(self):
        return "Maternal data for " + self.fhsis.barangay.name + " - " + str(self.fhsis.date)


# STI Surveillance
class STISurveillance(models.Model):

    fhsis = models.ForeignKey(FHSIS, on_delete=models.CASCADE)

    pregnant_women_seen = models.DecimalField(max_digits=4, decimal_places=2)
    pregnant_women_syphilis_positive = models.DecimalField(max_digits=4, decimal_places=2)
    pregnant_women_given_penicillin = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return "STISurveillance data for " + self.fhsis.barangay.name + " - " + str(self.fhsis.date)


# Immunization
class Immunization(models.Model):

    fhsis = models.ForeignKey(FHSIS, on_delete=models.CASCADE)

    immunization_given = models.DecimalField(max_digits=4, decimal_places=2)
    fully_immunized_children = models.DecimalField(max_digits=4, decimal_places=2)

    # child protected at birth
    child_protected = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Child protected at birth")
    infant_breastfed_until_6th_month = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Infant exclusively breastfed until 6th month")

    age_group = models.ForeignKey(AgeGroup, on_delete=models.CASCADE)

    def __str__(self):
        return "Immunization data for " + self.fhsis.barangay.name + " - " + str(self.fhsis.date) + " | " + \
               self.age_group.name


# Malaria
class Malaria(models.Model):

    fhsis = models.ForeignKey(FHSIS, on_delete=models.CASCADE)

    population_at_risk = models.DecimalField(max_digits=4, decimal_places=2)
    confirmed_malaria_cases = models.DecimalField(max_digits=4, decimal_places=2)
    malarial_deaths = models.DecimalField(max_digits=4, decimal_places=2)
    llin_given = models.DecimalField(max_digits=4, decimal_places=2)

    age_group = models.ForeignKey(AgeGroup, on_delete=models.CASCADE)

    def __str__(self):
        return "Malaria data for " + self.fhsis.barangay.name + " - " + str(self.fhsis.date) + " | " + \
            self.age_group.name


# Tuberculosis
class Tuberculosis(models.Model):

    fhsis = models.ForeignKey(FHSIS, on_delete=models.CASCADE)

    underwent_DDSM = models.DecimalField(max_digits=4, decimal_places=2)
    smear_discovered = models.DecimalField(max_digits=4, decimal_places=2)
    smear_cured = models.DecimalField(max_digits=4, decimal_places=2)
    case_detection_rate = models.DecimalField(max_digits=4, decimal_places=2)
    all_forms_identified = models.DecimalField(max_digits=4, decimal_places=2)

    age_group = models.ForeignKey(AgeGroup, on_delete=models.CASCADE)

    def __str__(self):
        return "Tuberculosis data for " + self.fhsis.barangay.name + " - " + str(self.fhsis.date) + " | " + \
            self.age_group.name


# Schistosomiasis
class Schistosomiasis(models.Model):

    fhsis = models.ForeignKey(FHSIS, on_delete=models.CASCADE)

    cases_treated = models.DecimalField(max_digits=4, decimal_places=2)
    positive_cases = models.DecimalField(max_digits=4, decimal_places=2)

    age_group = models.ForeignKey(AgeGroup, on_delete=models.CASCADE)

    def __str__(self):
        return "Schistosomiasis data for " + self.fhsis.barangay.name + " - " + str(self.fhsis.date) + " | " + \
            self.age_group.name


# Flariasis
class Flariasis(models.Model):

    fhsis = models.ForeignKey(FHSIS, on_delete=models.CASCADE)
    age_group = models.ForeignKey(AgeGroup, on_delete=models.CASCADE)

    cases = models.DecimalField(max_digits=4, decimal_places=2)
    clinical_rate = models.DecimalField(max_digits=4, decimal_places=2)
    mfd = models.DecimalField(max_digits=4, decimal_places=2)
    given_mda = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Number of people given MDA")

    def __str__(self):
        return "Flariasis data for " + self.fhsis.barangay.name + " - " + str(self.fhsis.date) + " | " + \
            self.age_group.name


# Leprosy
class Leprosy(models.Model):

    fhsis = models.ForeignKey(FHSIS, on_delete=models.CASCADE)
    age_group = models.ForeignKey(AgeGroup, on_delete=models.CASCADE)

    cases = models.DecimalField(max_digits=4, decimal_places=2)
    cases_cured = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return "Leprosy data for " + self.fhsis.barangay.name + " - " + str(self.fhsis.date) + " | " + \
            self.age_group.name


# Child Care
class ChildCare(models.Model):

    fhsis = models.ForeignKey(FHSIS, on_delete=models.CASCADE)
    age_group = models.ForeignKey(AgeGroup, on_delete=models.CASCADE)

    given_food = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Given complimentary food")
    newborn_screening = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Infant for newborn screening")
    infants_received_vitamin_A = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Infants who received Vitamin A")
    infants_received_iron = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Infants who received Iron")
    infants_received_MNP = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Infants who received MNP")
    sick_children = models.DecimalField(max_digits=4, decimal_places=2)
    given_deworming = models.DecimalField(max_digits=4, decimal_places=2)
    anemic_children = models.DecimalField(max_digits=4, decimal_places=2)
    anemic_with_iron = models.DecimalField(max_digits=4, decimal_places=2)
    diarrhea_cases = models.DecimalField(max_digits=4, decimal_places=2)
    diarrhea_with_ors = models.DecimalField(max_digits=4, decimal_places=2)
    pneumonia_cases = models.DecimalField(max_digits=4, decimal_places=2)
    pneumonia_with_tx = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return "Child Care data for " + self.fhsis.barangay.name + " - " + str(self.fhsis.date) + " | " + \
            self.age_group.name


##################################
# EXTERNAL DATA

class InformalSettlers(models.Model):

    date = models.DateTimeField(default=datetime.now)
    families = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Number of families")

    def __str__(self):
        return str(self.date)


# Health Care Waste Management
class HealthCareWasteManagement(models.Model):

    date = models.DateTimeField(default=datetime.now)

    with_syringe = models.DecimalField(max_digits=4, decimal_places=2)
    with_safe_water = models.DecimalField(max_digits=4, decimal_places=2)
    with_sanitary_toilet = models.DecimalField(max_digits=4, decimal_places=2)
    with_waste_disposal = models.DecimalField(max_digits=4, decimal_places=2)
    with_basic_sanitation = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return str(self.date)


# Unemployment Rate
class UnemploymentRate(models.Model):

    date = models.DateTimeField(default=datetime.now)
    rate = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return str(self.date)


