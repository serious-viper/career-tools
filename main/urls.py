from django.urls import path
from main.views import *

 

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('disclaimer', TemplateView.as_view(template_name="disclaimer.html"), name="disclaimer"),
    
    # KCET CUTOFF ROUTES
    path('kcet-cutoff', CutoffAnalyserView().main, name="kcet-cutoff"),
    path('kcet-cutoff/upload', CutoffAnalyserView().upload, name="cutoff-upload"),
    path("kcet-cutoff/ajax/get-courses", CutoffAnalyserView().get_courses),
    path("kcet-cutoff/ajax/get-data", CutoffAnalyserView().get_data),


    # College Seat Analyser
    path("seat-analyser", SeatAnalyserView().main, name = "seat-analyser"),
    path('seat-analyser/upload', SeatAnalyserView().upload, ),
    path('seat-analyser/ajax/get-courses', SeatAnalyserView().get_courses),
    path('seat-analyser/ajax/get-districts', SeatAnalyserView().get_districts),
    path('seat-analyser/ajax/get-colleges', SeatAnalyserView().get_colleges),
    path('seat-analyser/ajax/get-seat-matrix', SeatAnalyserView().get_seat_matrix),
]