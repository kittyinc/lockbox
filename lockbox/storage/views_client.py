from django.shortcuts import render
from django.views import View


class FileUploadView(View):
    def get(self, request):
        context = {}
        return render(request, "storage/upload.html", context=context)
