from django.contrib import admin
from django.urls import include, path  # Include the include function

urlpatterns = [
    path('admin/', admin.site.urls),
    path('analyze/', include('sentiment_analysis.urls')),  # Add this line
]
