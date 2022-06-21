from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import *
import openpyxl
from django.views.decorators.csrf import csrf_exempt
from main.models import Cutoff, SeatMatrix
# Create your views here.


class IndexView(TemplateView):
    template_name = "index.html"

class CutoffAnalyserView(object):
    def __init__(self) -> None:
        pass

    def main(self, request):
        context = {
            "course_categorys":Cutoff.objects.all().values_list("category", flat=True).distinct()
        }
        return render(request, "cutoff.html", context)

    @csrf_exempt
    def get_courses(self, request):
        category_name  = request.POST.get("course_category_name")
        courses = Cutoff.objects.filter(category = category_name).distinct().values_list("course", flat=True).order_by("-course")
        return JsonResponse({'courses':list(courses)})


    @csrf_exempt
    def get_data(self, request):
        course_name = request.POST.get("course")
        rank = request.POST.get("rank")
        reservation = request.POST.get("reservation")
        round = request.POST.get("round")
        cutoff_obj = Cutoff.objects.filter(**{
            "round": round, 
            "course":course_name,
            reservation+"__gte": rank
            })
        data = cutoff_obj.values_list("code", reservation, "college", "H"+reservation)
        return JsonResponse({"data":list(data.order_by(reservation).reverse())})


    def upload(self, request):
        if request.method == "POST":
            Cutoff.objects.all().delete()
            file = request.FILES.get("upload_file")
            wb = openpyxl.load_workbook(file).active
            fields = [i.name for i in Cutoff._meta.fields]
            fields.remove("id")
            for row in wb.iter_rows(min_row=2):
                values = [i.value for i in row]
                nary = dict(zip(fields,values))
                Cutoff.objects.get_or_create(**nary)
        return render(request, "cutoff-upload.html")



class SeatAnalyserView(object):

    def __init__(self) -> None:
        pass

    def main(self, request):    
        context = dict()
        context["category"] = SeatMatrix.objects.all().values("course_type").distinct().order_by("course_type") 
        return render(request, "seat-finder.html", context)


    @csrf_exempt
    def get_courses(self, request):
        category_name  = request.POST.get("category_name")
        courses = SeatMatrix.objects.filter(course_type = category_name).distinct().values_list("course_code", flat=True).order_by("-course_code")
        return JsonResponse({'courses':list(courses)})


    @csrf_exempt
    def get_districts(self, request):
        course_name = request.POST.get("course_name")
        category_name = request.POST.get("category_name")
        filter_dict = {}
        if course_name is not None:
            filter_dict["course_code"] = course_name
        if category_name is not None:
            filter_dict["course_type"] = category_name
        districts = SeatMatrix.objects.filter( **filter_dict).distinct().values_list("district", flat=True).order_by("district")
        return JsonResponse({'districts':list(districts)})


    @csrf_exempt
    def get_colleges(self, request):
        course_name = request.POST.get("course_name")
        category_name = request.POST.get("category_name")
        district_name = request.POST.get("district_name")
        filter_dict = {}
        if course_name is not None:
            filter_dict["course_code"] = course_name
        if category_name is not None:
            filter_dict["course_type"] = category_name
        if district_name is not None:
            filter_dict["district"] = district_name
        college_names = SeatMatrix.objects.filter(**filter_dict).distinct().values_list("college_full_name", flat=True).order_by("college_full_name")
        return JsonResponse({'colleges':list(college_names)})


    @csrf_exempt
    def get_seat_matrix(self, request):
        college_name = request.POST.get("college_name")
        course_name = request.POST.get("course_name")
        reservation_category = request.POST.get("reservation_category")
        reserved_seats_obj  = SeatMatrix.objects.filter(college_full_name = college_name, course_code = course_name)
        
        reserved_seats = reserved_seats_obj.values_list(reservation_category)[0][0]
        ga = list(reserved_seats_obj.values_list())[0][8:]
        total_seats = sum([int(i) for i in ga])

        seat_matrix_data = dict()
        seat_matrix_data["college_name"] = college_name
        seat_matrix_data["course_name"] = course_name
        seat_matrix_data["reservation_category"] = reservation_category.upper().replace("_", "")
        seat_matrix_data["total_seats"] = total_seats
        seat_matrix_data["reserved_seats"] = reserved_seats

        return JsonResponse({
            "seat_matrix_data":seat_matrix_data
        })



    def upload(self, request):
        if request.method == "POST":
            SeatMatrix.objects.all().delete()
            file = request.FILES.get("upload_file")
            wb = openpyxl.load_workbook(file)["Sheet1"]
            fields = [i.name for i in SeatMatrix._meta.fields]
            fields.remove("id")
            for row in wb.iter_rows(min_row=2):
                values = [i.value for i in row]
                nary = dict(zip(fields,values))
                SeatMatrix.objects.get_or_create(**nary)
        return render(request, "seat-upload.html")