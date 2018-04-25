from django.urls import path
from . import views

app_name = 'data-collection'

urlpatterns = [
    path('', views.index_bns, name='index'),

    # for nutritionists,
    path('nutritionist', views.nutritionist_data_input, name='nutritionist-input'),

    # index of nutritional statuses
    path('nutritional-status', views.nutritional_status, name='nutritional-status'),

    # fhsis index
    path('fhsis', views.fhsis_index, name='fhsis'),

    # create FHSIS
    path('fhsis/create', views.create_fhsis, name='create-fhsis'),

    # encode NS
    path('nutritional-status/input', views.encode_nutritional_statuses, name='encode-ns'),
    # put NS to DB
    path('nutritional-status/store', views.store_nutritional_statuses, name='store-ns'),

    # encode Child Care
    path('input/child-care', views.encode_child_care, name='encode-cc'),
    # put child care to db
    path('store/child-care', views.store_child_care, name='store-cc')
]

