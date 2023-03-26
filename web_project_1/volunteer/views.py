from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Volunteer
from .forms import VolunteerForm ,OrganizationForm
from todo_list.forms import TodoForm
from todo_list.models import Todo
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.db.models import Q

# Create your views here.

@login_required(login_url="login")
def vol_index(request):
    vol_list = Volunteer.objects.all()
    today = DateFormat(datetime.now()).format('Y-m-d H:i')
    todo = Todo.objects.filter(user_id = request.user.id).filter(~Q(vol_id=0)).filter(complete=1)
    vol_id = todo.values("vol_id")
    print(vol_id)
    
    return render(request, "volunteer/index.html", {"vol_list": vol_list,"today":today,"vol_id":vol_id})


@login_required(login_url="login")
def vol_detail(request,pk):
    detail = get_object_or_404(Volunteer,pk=pk)
    return render(request, 'volunteer/vol_detail.html', {'detail':detail})

@login_required(login_url="login")
def sign_vol(request, pk):
    sign_vol = get_object_or_404(Volunteer, pk=pk)
    sign_vol.sign_vol.add(request.user)

    return redirect("vol_detail", pk=pk)

@login_required(login_url="login")
def add_cal(request,pk):
    vol_detail = get_object_or_404(Volunteer,pk=pk)
    Todo.objects.create(
    title= vol_detail.organization.org_name,
    start_date= vol_detail.start_date,
    end_date =  vol_detail.end_date,
    description =  vol_detail.organization.addr,
    user = request.user,
    vol_id = vol_detail.id
    )
    
    return redirect("todo_list")

@login_required(login_url="login")
def create_vol(request):
    if request.method == "POST":
        form = VolunteerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            return redirect("vol_index")
    else:
        form = VolunteerForm()

    return render(request, "volunteer/create_vol.html", {"form": form})

@login_required(login_url="login")
def create_org(request):
    if request.method == "POST":
        form = OrganizationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("vol_index")
    else:
        form = OrganizationForm()

    return render(request, "volunteer/create_org.html", {"form": form})

