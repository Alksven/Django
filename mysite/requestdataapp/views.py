from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from . forms import UsserBioForm, UploadFileForm

def process_get_views(request: HttpRequest) -> HttpResponse:
    a = request.GET.get("a", "")
    b = request.GET.get("b", "")
    result = a + b

    context = {
        "a": a,
        "b": b,
        "result": result,
    }
    return render(request, "requestdataapp/request-query-params.html", context=context)


def user_form(request: HttpRequest) -> HttpResponse:
    context = {
         "form": UsserBioForm()
         
    }
    return render(request, "requestdataapp/user-bio-form.html", context=context)


def handle_file_upload(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # myfile = request.FILES["myfile"]
            myfile = form.cleaned_data["file"]
            fs = FileSystemStorage()
            file_size = myfile.size
            max_file_size = 1 * 1024 * 1024
            try:
                if file_size > max_file_size:
                    raise Exception("File size exceeded.")
            except Exception as es:
                    return render(request, "requestdataapp/error-file.html", {"error": es})
            else:
                filename = fs.save(myfile.name, myfile)
                print("saved file", filename)
    else:
         form = UploadFileForm()
    context = {
         "form": form
    }
    return render(request, "requestdataapp/file-upload.html", context=context)
