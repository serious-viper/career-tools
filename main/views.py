from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import *
import openpyxl
from django.views.decorators.csrf import csrf_exempt
from main.models import Cutoff
# Create your views here.


class IndexView(TemplateView):
    template_name = "main/index.html"


def cutoff(request):
    context = {
        "course_categorys":Cutoff.objects.all().values_list("category", flat=True).distinct()
    }
    return render(request, "main/cutoff.html", context)


@csrf_exempt
def get_courses(request):
    category_name  = request.POST.get("course_category_name")
    courses = Cutoff.objects.filter(category = category_name).distinct().values_list("course", flat=True).order_by("-course")
    return JsonResponse({'courses':list(courses)})


@csrf_exempt
def get_data(request):
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

def upload(request):
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
    return render(request, "seat_finder/upload.html")
