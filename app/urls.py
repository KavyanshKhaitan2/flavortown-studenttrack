from django.urls import include, path
from .views import DashboardView, EditRoutineView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('routine/edit/', EditRoutineView.as_view(), name='routine.edit'),
]
