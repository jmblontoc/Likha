def validate_fields(request):

    counter = 0

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

    return counter
