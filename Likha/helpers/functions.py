from django.contrib import messages
from django.shortcuts import redirect, render
import datetime

from django.urls import reverse

from datacollection.models import FHSIS, AgeGroup
from helpers import checkers


def fhsis_input(request, url, model, data):

    if checkers.validate_fields(request) > 0:
        messages.error(request, "Please fill up all fields")
        return redirect(url)

    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    fhsis = FHSIS.objects.get(date__month=month, date__year=year)

    age_groups = AgeGroup.objects.all()

    instance_list = []

    for age_group in age_groups:
        instance_list.append({
            age_group.code + "-" + age_group.sex: model(fhsis=fhsis, age_group=age_group)

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

    messages.success(request, data + " data succesfully encoded")
    return redirect('data-collection:fhsis')


def encode_fhsis(request, model, url, data):
    age_groups = AgeGroup.objects.all()
    fields = model._meta.fields

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
        'fields': final_fields,
        'url': reverse(url),
        'data': data
    }

    return render(request, 'datacollection/fhsis_data_input.html', context)


def input_fhsis(request, form, source):

    f = form(request.POST or None)

    month = datetime.datetime.now().month
    year = datetime.datetime.now().year

    fhsis = FHSIS.objects.get(date__year=year, date__month=month)

    if f.is_valid():

        data = f.save(commit=False)
        data.fhsis = fhsis
        data.save()

        messages.success(request, source + " data encoded successfully")
        return redirect('data-collection:fhsis')

    context = {
        'form': f,
        'data': source
    }

    return render(request, 'datacollection/encode_fhsis.html', context)


def input_external_data(request, form, source):

    f = form(request.POST or None)

    if f.is_valid():

        data = f.save(commit=False)
        data.save()

        messages.success(request, source + " data has been successfully encoded!")
        return redirect('data-collection:input-external')

    context = {
        'form': f,
        'data': source
    }

    return render(request, 'datacollection/encode_external_data.html', context)

