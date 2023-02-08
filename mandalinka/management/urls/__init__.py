from django.urls import path, include

from management.urls import apis

from management.views import management_page

urlpatterns = [
    path('', management_page, name='management'),
    path('api/', include(apis), name='management_APIs'),
    path('page/<str:page>/', management_page, name='management-page'),
]
