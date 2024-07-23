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
    
    filter_status = request.GET.get("status")
    if filter_status == "todo":
        tasks = Task.objects.filter(todo__isnull=False, todo__exact="").order_by("todo")
    elif filter_status == "doing":
        tasks = Task.objects.filter(doing__isnull=False, doing__exact="").order_by("doing")
    elif filter_status == "done":
        tasks = Task.objects.filter(done__isnull=False, done__exact="").order_by("done")
    else:
        tasks = Task.objects.order_by("-posted_at")

    if request.GET.get("order") == "due":
        tasks = tasks.order_by("due_at")
    else:
        tasks = tasks.order_by("-posted_at")

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
        task.due_at = make_aware(parse_datetime(request.POST['due_at'])) if request.POST["due_at"] else None
        task.todo = request.POST.get("todo", "")
        task.doing = request.POST.get("doing", "")
        task.done = request.POST.get("done", "")
        task.due_at = make_aware(parse_datetime(request.POST['due_at']))
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
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    task.completed = True
    task.save()
    return redirect(index)
