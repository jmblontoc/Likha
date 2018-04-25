import datetime
from datetime import datetime as dt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import NutritionalStatus, AgeGroup, Barangay, OperationTimbang, OPTValues, ChildCare, FHSIS
from helpers import global_user, checkers


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

    age_groups = AgeGroup.objects.all()
    fields = ChildCare._meta.fields

    final_fields = []

    for field in fields:
        if field.verbose_name == 'ID' or field.verbose_name == 'fhsis' or field.verbose_name == 'age group':
            continue

        splits = str(field).split(".")
        actual_field = splits[2]

        final_fields.append({
            'field': field,
            'string': actual_field
        })

    context = {
        'age_groups': age_groups,
        'fields': final_fields
    }

    return render(request, 'datacollection/fhsis_data_input.html', context)


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

    if checkers.validate_fields(request) > 0:
        messages.error(request, "Please fill up all fields of enter valid inputs only")
        return redirect('data-collection:encode-cc')

    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    fhsis = FHSIS.objects.get(date__month=month, date__year=year)

    age_groups = AgeGroup.objects.all()

    instance_list = []

    for age_group in age_groups:
        instance_list.append({
            age_group.code + "-" + age_group.sex: ChildCare(fhsis=fhsis, age_group=age_group)
        })

    for key, value in request.POST.items():

        if key != 'csrfmiddlewaretoken':
            splits = str(key).split("-")

            code = splits[0] + "-" + splits[2]
            field = splits[1]

            for instance in instance_list:
                k = list(instance.keys())[0]
                v = instance.get(code)

                if k == code:
                    setattr(v, field, value)
                    v.save()

    messages.success(request, "Child care successfully encoded!")
    return redirect('data-collection:fhsis')


@login_required
def create_fhsis(request):

    user = global_user.get_user(request.user.username)

    FHSIS.objects.create(
        barangay=user.barangay
    )

    month = datetime.datetime.now().strftime("%B")

    messages.success(request, "FHSIS generated for " + str(month))
    return redirect('data-collection:fhsis')

