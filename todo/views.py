from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from todo.models import Task

def index(request):
    if request.method == "POST":
        task = Task(
            title=request.POST["title"],
            due_at=make_aware(parse_datetime(request.POST["due_at"])) if request.POST["due_at"] else None,
            todo=request.POST.get("todo", ""),
            doing=request.POST.get("doing", ""),
            done=request.POST.get("done", "")
        )
        task.save()
        return redirect('index')

    if request.GET.get("order") == "due":
        tasks = Task.objects.order_by("due_at")
    else:
        tasks = Task.objects.order_by("-posted_at")

    context = {
        "tasks": tasks
    }
    return render(request, "todo/index.html", context)

def detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    context = {
        "task": task,
    }
    return render(request, "todo/detail.html", context)

def update(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == "POST":
        task.title = request.POST['title']
<<<<<<< HEAD
        task.due_at = make_aware(parse_datetime(request.POST['due_at'])) if request.POST["due_at"] else None
        task.todo = request.POST.get("todo", "")
        task.doing = request.POST.get("doing", "")
        task.done = request.POST.get("done", "")
=======
        task.due_at = make_aware(parse_datetime(request.POST['due_at']))
>>>>>>> 7957e5d879af7c85081aaa2344e6b4667dd6c060
        task.save()
        return redirect('detail', task_id=task.id)

    context = {
        'task': task
    }
    return render(request, "todo/edit.html", context)

def delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.delete()
    return redirect('index')

def close(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.completed = True
    task.save()
    return redirect('index')
