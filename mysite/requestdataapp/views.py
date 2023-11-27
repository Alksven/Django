from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from requestdataapp.forms import UserBioForm


def process_get_view(request: HttpRequest) -> HttpResponse:
    context = {

    }
    return render(request, "requestdataapp/request-query-params.html", context=context)


def user_form(request: HttpRequest) -> HttpResponse:
    context = {
        "form": UserBioForm()
    }
    return render(request, "requestdataapp/user-bio-form.html", context=context)


def handle_file_uploads(request: HttpRequest) -> HttpResponse:
    if request.method == "POST" and request.FILES.get("myfile"):
        myfile = request.FILES["myfile"]
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        print("saved file", filename)
    return render(request, "requestdataapp/file-upload.html")

