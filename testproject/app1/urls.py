from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('register/', register),
    path('update/<int:id>', update),
    path('delete/<int:id>', delete),
]
