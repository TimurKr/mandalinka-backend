from django.urls import path, include

urlpatterns = [
    path('ingredients/', include('management.urls.ingredients')),
]
