from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse

from tasks.models import Tasks
from .forms import Tasks, TaskForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class TasksListView(LoginRequiredMixin, ListView):
    model = Tasks
    template_name = 'tasks/tasks_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = self.get_queryset()
        context['menu'] = None
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return Tasks.objects.filter(created_by=self.request.user)


class TasksUpdateView(LoginRequiredMixin,UpdateView):
    model = Tasks
    form_class = TaskForm
    # fields = '__all__'
    template_name = 'tasks/update_task.html'
    title_page = 'Изменить данную задачу'
    success_url = reverse_lazy('tasks:tasks')
    permission_required = ('tasks.change_tasks',)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


    def get_success_url(self):
        return reverse_lazy('tasks:tasks')


class TasksCreateView(LoginRequiredMixin, CreateView):
    model = Tasks
    form_class = TaskForm
    template_name = "tasks/create_task.html"

    def form_valid(self, form):
        task = form.save(commit=False)
        task.created_by = self.request.user
        task.save()
        return super().form_valid(form)


def delete_student(request, pk):
    task=Tasks.objects.get(pk=pk)
    task.delete()
    return redirect('tasks:tasks')

