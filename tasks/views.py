from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from tasks.models import Tasks
from .forms import  TaskForm
from django.views.generic import ListView, CreateView, UpdateView


class TasksListView(LoginRequiredMixin, ListView):
    model = Tasks
    template_name = 'tasks/tasks_list.html'
    context_object_name = 'tasks'
    paginate_by = 2

    def get_queryset(self):
        query = self.request.GET.get('q')
        status_filter = self.request.GET.get('status')
        due_date = self.request.GET.get('due_date')
        queryset = Tasks.objects.filter(created_by=self.request.user)

        if query:
            queryset = queryset.filter(name__icontains=query)

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        if due_date:
            try:
                due_date_parsed = datetime.strptime(due_date, '%Y-%m-%d').date()
                queryset = queryset.filter(due_date=due_date_parsed)
            except ValueError:
                pass

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Tasks.STATUS_CHOICES
        # Pass status choices to the template
        return context


class TasksUpdateView(LoginRequiredMixin,UpdateView):
    model = Tasks
    form_class = TaskForm
    template_name = 'tasks/update_task.html'
    title_page = 'Изменить данную задачу'
    success_url = reverse_lazy('tasks:tasks')
    permission_required = ('tasks.change_tasks',)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context



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

