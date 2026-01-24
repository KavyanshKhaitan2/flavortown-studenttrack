from django.urls import include, path
from .views import DashboardView, EditRoutineView, NewTasksView, TaskActionView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('routine/edit/', EditRoutineView.as_view(), name='routine.edit'),
    path('tasks/new/', NewTasksView.as_view(), name='tasks.new'),
    path('tasks/action/<int:pk>/', TaskActionView.as_view(), name='tasks.action'),
]
