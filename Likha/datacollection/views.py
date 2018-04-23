from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from . models import NutritionalStatus, AgeGroup, Barangay, OperationTimbang, OPTValues
from helpers import global_user


# Create your views here.
@login_required
def index_bns(request):
    return render(request, 'datacollection/index-bns.html', None)


@login_required
def nutritionist_data_input(request):
    return render(request, 'datacollection/nutritionists-data-input.html', None)


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
def encode_child_care(request):

    age_groups = AgeGroup.objects.all()


# VIEWS that store the data to the DB
@login_required
def store_nutritional_statuses(request):

    counter = 0

    # data validation! sorry for the long code HAHAHAHA
    for key, value in request.POST.items():
        if key == 'barangay' or key == 'csrfmiddlewaretoken':
            continue

        if value == '':
            counter = counter + 1
        else:
            if float(value) < 0:
                counter = counter + 1
            if 'e' in value:
                counter = counter + 1

    if counter > 0:
        messages.error(request, 'Please fill up all fields or enter valid inputs only')
        print('waaah')
        return redirect('data-collection:encode-ns')

    # store values in DB

    # barangay_post = request.POST.get('barangay')
    # barangay = Barangay.objects.get(name=barangay_post)

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
