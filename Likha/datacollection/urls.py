from django.urls import path
from . import views

app_name = 'data-collection'

urlpatterns = [
    path('', views.index_bns, name='index'),

    # for nutritionists,
    path('nutritionist', views.nutritionist_data_input, name='nutritionist-input'),

    # encode NS
    path('input/nutritional-statuses', views.encode_nutritional_statuses, name='encode-ns'),
    # put NS to DB
    path('store/nutritional-statuses', views.store_nutritional_statuses, name='store-ns')
]

