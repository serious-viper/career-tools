from django.contrib import admin
from seat_finder.models import SeatMatrix
# Register your models here.


class SeatMatrixAdmin(admin.ModelAdmin):
    list_filter = ('course_type',)

admin.site.register(SeatMatrix, SeatMatrixAdmin)