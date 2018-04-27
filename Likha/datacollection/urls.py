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
    path('store/child-care', views.store_child_care, name='store-cc'),

    # encode Immunization
    path('input/immunization', views.encode_immunization, name='encode-immunization'),
    # put immunization to db
    path('store/immunization', views.store_immunization, name='store-immunization'),

    # encode TB
    path('input/tuberculosis', views.encode_tuberculosis, name='encode-tb'),
    path('store/tuberculosis', views.store_tuberculosis, name='store-tb'),

    # encode malaria
    path('input/malaria', views.encode_malaria, name='encode-malaria'),
    path('store/malaria', views.store_malaria, name='store-malaria'),

    # encode flariasis
    path('input/flariasis', views.encode_flariasis, name='encode-flariasis'),
    path('store/flariasis', views.store_flariasis, name='store-flariasis'),

    # encode schistosomiasis
    path('input/schistosomiasis', views.encode_schistosomiasis, name='encode-schistosomiasis'),
    path('store/schistosomiasis', views.store_schistosomiasis, name='store-schistosomiasis'),

    # encode leprosy
    path('input/leprosy', views.encode_leprosy, name='encode-leprosy'),
    path('store/leprosy', views.store_leprosy, name='store-leprosy'),

    # maternal
    path('input/maternal', views.encode_maternal, name='encode-maternal'),

    # sti surveillance
    path('input/sti_surveillance', views.encode_sti_surveillance, name='encode-sti'),

    # EXTERNAL DATA

    # external data input
    path('external_data/', views.input_external_data, name='input-external'),

    # input health care waste management
    path('external_data/hcwm/input/', views.encode_health_care_waste_management, name='encode-healthcare'),

    # informal settlers
    path('external_data/informal_settlers/input', views.encode_informal_settlers, name='encode-informal-settlers'),

    # unemployment rate
    path('external_data/unemployment_rate/input', views.encode_unemployment_rate, name='encode-ur'),


]

