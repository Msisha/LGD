from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# Default view for root URL
def home(request):
    return HttpResponse("<h1>Welcome to the LGD Project</h1>")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('ldg_app.urls')),  # Include app-specific URLs
    path('', home, name='home'),  # Default root URL
]
