from django.urls import path, include

from management.urls import apis

from management.views import management_page

urlpatterns = [
    path('api/', include(apis), name='management_APIs'),
]
