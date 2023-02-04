from django.urls import path, include

from management.views import management_page

urlpatterns = [
    path('<str:page>/', management_page, name='management-page'),
    path('ingredients/', include('management.urls.ingredients')),

]
