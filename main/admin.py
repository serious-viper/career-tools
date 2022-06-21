from django.contrib import admin
from main.models import Cutoff, SeatMatrix
# Register your models here.

@admin.register(Cutoff)
class CutoffAdmin(admin.ModelAdmin):
    list_filter = ("round",)

@admin.register(SeatMatrix)
class SeatMatrixAdmin(admin.ModelAdmin):
    list_filter = ('course_type',)


