from django.shortcuts import render
from django.http import HttpResponseNotFound


def management_page(request, page: str = None):
    """View rendering the requested management page"""

    if page and page not in ('ingredients', 'recipes'):
        return HttpResponseNotFound()

    return render(request, 'management/index.html', {'active_path': page})
