from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Todo
from .forms import TodoForm
import json
# Create your views here.


@login_required(login_url="login")
def index(request):
    todos = Todo.objects.filter(user=request.user)

    todo_list = []

    for todo in todos:
        if todo.complete:
            todo_list.append({'id': todo.id, 'title': todo.title, 'start': str(
                todo.start_date), 'end': str(todo.end_date), 'color': 'gray'})
        elif todo.important:
            todo_list.append({'id': todo.id, 'title': todo.title, 'start': str(
                todo.start_date), 'end': str(todo.end_date), 'color': 'red'})
        else:
            todo_list.append({'id': todo.id, 'title': todo.title, 'start': str(
                todo.start_date), 'end': str(todo.end_date), })

    todoJson = json.dumps(todo_list)
    return render(request, "todo_list/cal.html", {"todoJson": todoJson})


@login_required(login_url="login")
def add_event(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            # 이동
            return redirect("todo_list")
    else:
        form = TodoForm()

    return render(request, "todo_list/add_event.html", {"form": form})


@login_required(login_url="login")
def event_detail(request, pk):

    detail = get_object_or_404(Todo, pk=pk)
    return render(request, "todo_list/event_detail.html", {"detail": detail})


@login_required(login_url="login")
def event_edit(request, pk):

    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        print(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            # 이동
            return redirect("event_detail", pk=todo.id)
        # pass
    else:
        form = TodoForm(instance=todo)

    return render(request, 'todo_list/event_edit.html', {'form': form})


@login_required(login_url="login")
def event_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.delete()
    return redirect("todo_list")
