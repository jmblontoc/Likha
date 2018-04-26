import datetime
from datetime import datetime as dt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import NutritionalStatus, AgeGroup, Barangay, OperationTimbang, OPTValues, ChildCare, FHSIS, Immunization, \
    Tuberculosis, Malaria, Flariasis, Leprosy, Schistosomiasis
from helpers import global_user, checkers, functions


# Create your views here.
@login_required
def index_bns(request):
    return render(request, 'datacollection/index_bns.html', None)


@login_required
def nutritionist_data_input(request):
    return render(request, 'datacollection/nutritionists-data-input.html', None)


@login_required
def nutritional_status(request):
    return render(request, 'datacollection/ns_index.html', None)


@login_required
def fhsis_index(request):
    return render(request, 'datacollection/fhsis_index.html', None)


# manually encode views here
@login_required
def encode_nutritional_statuses(request):

    nutritional_statuses = NutritionalStatus.objects.all()
    age_groups = AgeGroup.objects.all()
    barangays = Barangay.objects.all()

    context = {
        'nutritional_statuses': nutritional_statuses,
        'age_groups': age_groups,
        'barangays': barangays
    }

    return render(request, 'datacollection/input_nutritional_statuses.html', context)


# Child Care encode
@login_required
def encode_child_care(request):

    return functions.encode_fhsis(request, ChildCare, 'data-collection:store-cc', "Child Care")


# encode Immunization
@login_required
def encode_immunization(request):

    return functions.encode_fhsis(request, Immunization, 'data-collection:store-immunization', "Immunization")


# encode Flariasis
@login_required
def encode_flariasis(request):

    return functions.encode_fhsis(request, Flariasis, 'data-collection:store-flariasis', "Flariasis")


# encode Leprosy
@login_required
def encode_leprosy(request):

    return functions.encode_fhsis(request, Leprosy, 'data-collection:store-leprosy', "Leprosy")


# encode Schistosomiasis
@login_required
def encode_schistosomiasis(request):

    return functions.encode_fhsis(request, Schistosomiasis, 'data-collection:store-schistosomiasis', "Schistosomiasis")


# encode Tuberculosis
@login_required
def encode_tuberculosis(request):

    return functions.encode_fhsis(request, Tuberculosis, 'data-collection:store-tb', "Tuberculosis")


# encode Malaria
@login_required
def encode_malaria(request):

    return functions.encode_fhsis(request, Malaria, 'data-collection:store-malaria', "Malaria")


# VIEWS that store the data to the DB
@login_required
def store_nutritional_statuses(request):

    if checkers.validate_fields(request) > 0:
        messages.error(request, 'Please fill up all fields or enter valid inputs only')
        return redirect('data-collection:encode-ns')

    current_user = global_user.get_user(request.user.username)
    barangay = current_user.barangay

    opt = OperationTimbang(barangay=barangay)
    opt.save()

    for key, value in request.POST.items():
        if key == 'barangay' or key == 'csrfmiddlewaretoken':
            continue

        splits = key.split('-')

        ns_code = splits[0]
        ag_code = splits[1]
        sex_code = splits[2]

        nutritional_status = NutritionalStatus.objects.get(code=ns_code)
        age_group = AgeGroup.objects.get(code=ag_code, sex=sex_code)
        number = float(value)

        OPTValues.objects.create(
            opt=opt,
            nutritional_status=nutritional_status,
            age_group=age_group,
            values=number
        )

    messages.success(request, 'Nutritional statuses successfully encoded!')
    return redirect('data-collection:index')


@login_required
def store_child_care(request):

    url = 'data-collection:encode-cc'

    return functions.fhsis_input(request, url, ChildCare, "Child Care")


@login_required
def store_immunization(request):

    url = 'data-collection:encode-immunization'

    return functions.fhsis_input(request, url, Immunization, "Immmunization")


@login_required
def store_tuberculosis(request):

    url = 'data-collection:encode-tb'

    return functions.fhsis_input(request, url, Tuberculosis, "Tuberculosis")


@login_required
def store_malaria(request):

    url = 'data-collection:encode-malaria'

    return functions.fhsis_input(request, url, Malaria, "Malaria")


@login_required
def store_flariasis(request):

    url = 'data-collection:encode-flariasis'

    return functions.fhsis_input(request, url, Flariasis, "Flariasis")


@login_required
def store_leprosy(request):

    url = 'data-collection:encode-leprosy'

    return functions.fhsis_input(request, url, Leprosy, "Leprosy")


@login_required
def store_schistosomiasis(request):

    url = 'data-collection:encode-schistosomiasis'

    return functions.fhsis_input(request, url, Schistosomiasis, "Schistosomiasis")


@login_required
def create_fhsis(request):

    user = global_user.get_user(request.user.username)

    FHSIS.objects.create(
        barangay=user.barangay
    )

    month = datetime.datetime.now().strftime("%B")

    messages.success(request, "FHSIS generated for " + str(month))
    return redirect('data-collection:fhsis')

