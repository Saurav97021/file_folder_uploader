from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('folders/', views.upload_folder, name='upload_folder'),
    path('folders/download/<int:folder_id>/', views.download_folder, name='download_folder'),
]
