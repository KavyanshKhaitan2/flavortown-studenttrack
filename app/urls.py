from django.urls import include, path
from .views import DashboardView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
]
