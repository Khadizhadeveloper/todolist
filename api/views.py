from rest_framework.generics import ListAPIView, UpdateAPIView,  CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from tasks.models import Tasks
from .serializers import TasksSerializer
# Create your views here.
class TasksListAPIView(ListAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Tasks.objects.filter(created_by=self.request.user)


class TasksCreateAPIView(CreateAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TasksUpdateAPIView(UpdateAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer


class TasksDeleteAPIView(DestroyAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer






