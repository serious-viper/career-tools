from django.urls import path
from main.views import IndexView, cutoff, upload, get_courses, get_data

app_name = 'main' 


urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('kcet-cutoff', cutoff, name="cutoff"),
    path('upload', upload, name="upload"),


    path("kcet-cutoff/ajax/get-courses", get_courses),
    path("kcet-cutoff/ajax/get-data", get_data)
]