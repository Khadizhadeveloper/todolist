from django.urls import path, include
from . import views

app_name='tasks'
urlpatterns = [
    path('', views.TasksListView.as_view(), name='tasks'),
    path('create/', views.TasksCreateView.as_view(), name='create_task'),
    path('<int:pk>/update/', views.TasksUpdateView.as_view(), name='update_task'),
    path('<int:pk>/delete/', views.delete_student, name='delete_task'),

]