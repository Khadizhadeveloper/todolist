from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import TaskForm
from .models import Tasks


# Create your views here.

def create_task(request):
    tasks=Tasks.objects.all()
    if request.method == 'POST':
        form=TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:tasks')
    else:
        form=TaskForm()
        return render(request,'tasks/create_task.html',{'form':form})



def all_tasks(request):
    tasks=Tasks.objects.all()
    return render(request,'tasks/tasks_list.html',{'tasks':tasks})



def update_task(request,pk):
    tasks=Tasks.objects.get(pk=pk)
    if request.method =='POST':
        form=TaskForm(request.POST,request.FILES,instance=tasks)
        if form.is_valid():
            form.save()
            return redirect('tasks:tasks')
    else:
        form=TaskForm(instance=tasks)
        return render(request,'tasks/update_task.html',{'tasks':tasks,'form':form})


def delete_task(request,pk):
    tasks=Tasks.objects.get(pk=pk)
    tasks.delete()
    messages.success(request,'Task deleted successfully', messages.SUCCESS)
    return redirect('tasks:tasks')









