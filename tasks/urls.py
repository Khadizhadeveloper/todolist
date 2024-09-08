from django.urls import path
from . import views

app_name='tasks'
urlpatterns = [
    path('', views.all_tasks, name='tasks'),
    path('create/', views.create_task, name='create_task'),
    path('<int:pk>/update/', views.update_task, name='update_task'),
    path('<int:pk>/delete/', views.delete_task, name='delete_task'),
]