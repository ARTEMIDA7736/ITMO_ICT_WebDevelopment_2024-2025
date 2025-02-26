from django.contrib import admin
from django.urls import path

from project_first_app.views import info_about_car_owner, all_owners, CarList, CarById, create_owner, CarUpdate, \
    CarCreate, CarDelete

urlpatterns = [
    path('admin/', admin.site.urls),
    path('owner/<int:id_owner>', info_about_car_owner),
    path('list_owners/', all_owners),
    path('list_cars/', CarList.as_view()),
    path('car/<int:pk>', CarById.as_view()),
    path('create_owner/', create_owner),
    path('update_car/<int:pk>', CarUpdate.as_view()),
    path('create_car/', CarCreate.as_view()),
    path('delete_car/<int:pk>', CarDelete.as_view())
]
