from seat_finder.views import *
from django.urls import path

app_name = 'seat_finder'

urlpatterns = [

    path("", seat_finder, name = "index"),
    path('upload', upload, name="upload"),
    

    # AJAX REQUESTS MANAGEMENTS
    path('seat-finder/ajax/get-courses', get_courses, name="get_courses"),
    path('seat-finder/ajax/get-districts', get_districts, name="get_districts"),
    path('seat-finder/ajax/get-colleges', get_colleges, name="get_colleges"),
    path('seat-finder/ajax/get-seat-matrix', get_seat_matrix, name="get_seat_matrix"),

    ]