from django.urls import path
from .views import TasksListAPIView, TasksCreateAPIView, TasksUpdateAPIView, TasksDeleteAPIView, TasksDetailAPIView

app_name = 'api'
urlpatterns = [
    path('', TasksListAPIView.as_view(), name='tasks'),
    path('create/', TasksCreateAPIView.as_view(), name='create_task'),
    path('detail/<int:pk>/', TasksDetailAPIView.as_view(), name='detail_task'),
    path('update/<int:pk>/', TasksUpdateAPIView.as_view(), name='update_task'),
    path('delete/<int:pk>/', TasksDeleteAPIView.as_view(), name='delete_task'),

]