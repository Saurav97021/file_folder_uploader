from django import forms
from .models import UploadedFile

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ('name', 'file',)

from .models import UploadedFile, UploadedFolder

class FolderUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFolder
        fields = ('name', 'folder',)