from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import UploadedFile
from .forms import FileUploadForm
import os, zipfile
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect
from .models import UploadedFolder
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.conf import settings



def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = FileUploadForm()
    files = UploadedFile.objects.all()
    return render(request, 'upload.html', {'form': form, 'files': files})

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.conf import settings
import os
from mimetypes import guess_type

def download_file(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id)
    file_path = os.path.join(settings.MEDIA_ROOT, file.file.name)

    # Guess the file's MIME type
    mime_type, _ = guess_type(file_path)

    # Open the file for reading in binary mode
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type=mime_type or 'application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file.file.name)}"'
        return response

def upload_folder(request):
    if request.method == 'POST':
        folder_name = request.POST.get('folder_name', 'uploaded_folder')
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'folders', folder_name)

        os.makedirs(upload_dir, exist_ok=True)

        for file in request.FILES.getlist('folder[]'):
            file_path = os.path.join(upload_dir, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

        # Save folder record in the database
        UploadedFolder.objects.create(name=folder_name, folder=upload_dir)

    folders = UploadedFolder.objects.all()  # Retrieve all folders
    return render(request, 'upload_folder.html', {'folders': folders})



def download_folder(request, folder_id):
    folder = get_object_or_404(UploadedFolder, id=folder_id)
    folder_path = folder.folder.path  # The path to the folder

    zip_file_path = os.path.join(settings.MEDIA_ROOT, 'temp', f"{folder.name}.zip")
    os.makedirs(os.path.dirname(zip_file_path), exist_ok=True)

    # Create the ZIP file dynamically
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=folder_path)  # Preserve folder structure
                zipf.write(file_path, arcname=arcname)

    # Return the ZIP file as a response
    response = FileResponse(open(zip_file_path, 'rb'), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{folder.name}.zip"'
    return response
