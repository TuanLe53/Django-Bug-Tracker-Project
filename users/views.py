from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import auth, User, Group, Permission
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from main.models import Team
# Create your views here.
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request, "Credentials Invalid")
            return redirect("/login")
            
    return render(request, "users/login.html")

@login_required
def logout(request):
    auth.logout(request)
    return redirect("/login")

def register(request):
    if request.method =="POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Already Taken")
                return redirect("/register")
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Name Already Taken")
                return redirect("/register")
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                user_login = auth.authenticate(username=username, password=password1)
                auth.login(request, user_login)
                
                if request.POST["role"] == "leader":
                    leader_group = Group.objects.get(name="Leaders")
                    user.groups.add(leader_group)
                    return redirect("/create/team")
            
                else:
                    return redirect("/create/team")
        else:
            messages.info(request, "Password not matching")
            return redirect("/register")
    
    return render(request, "users/register.html")

@login_required
def create_team(request):
    team_list = Team.objects.all()
    
    if request.method == "POST":
        team = Team.objects.create(name=request.POST["name"])
        team.members.add(request.user)
        team.save()
        return redirect("/")
    
    context = {
        "teams": team_list,
    }
    
    return render(request, "users/create_team.html", context)

def join(request, team_name):
    team = Team.objects.get(name=team_name)
    team.members.add(request.user)
    
    return redirect("/")