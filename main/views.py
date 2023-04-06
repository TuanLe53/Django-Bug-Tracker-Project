from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TicketForm, ProjectForm, CommentForm
from django.contrib.auth.models import User
from .models import Project, Ticket, Comment, Team
from .serializers import TicketSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
@login_required
def home(request):
    user = request.user
    
    try:
        team = Team.objects.get(name=user.team.all()[0])
    except IndexError:
        return redirect("/create/team")
    
    team = Team.objects.get(name=user.team.all()[0])
    project_list = Project.objects.filter(team=team)
    
    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            usernames = request.POST.getlist("members")
            members = User.objects.filter(username__in=usernames)
            
            project = form.save(commit=False)
            project.team = team
            project.save()
            
            project.members.set(members)
            return redirect("/")
    else:
        form = ProjectForm()
    
    context = {
        "form": form, 
        "projects": project_list,
        "team": team
        }
    
    return render(request, "main/home.html", context)

@login_required
def tickets(request, team_name):
    team = Team.objects.get(name=team_name)
    team_projects = Project.objects.filter(team=team)
    ticket_list = [x for x in Ticket.objects.all() if x.project in team_projects]
    
    if request.method == "POST":
        form = TicketForm(request.POST)

        if form.is_valid():
            usernames = request.POST.getlist("members")
            members = User.objects.filter(username__in=usernames)
            project = Project.objects.get(name=request.POST["project"])
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.status = "New"
            ticket.project = project
            ticket.save()
            ticket.assign.set(members)
            
            return redirect(f"/team/{team_name}/tickets")
        
    else:
        form = TicketForm()
    
    context = {
        "form":form,
        "tickets": ticket_list,
        "team": team
        }
    
    return render(request, "main/tickets.html", context)

@login_required
def project_detail(request, pk):
    team = Team.objects.get(name=request.user.team.all()[0])
    
    project = Project.objects.get(id=pk)
    ticket_list = Ticket.objects.filter(project=project)
    not_project_members = [x for x in team.members.all() if x not in User.objects.filter(project=project.id)]

    if request.method == "POST":
        
        if "add_ticket" in request.POST:
            form = TicketForm(request.POST)
            
            if form.is_valid():
                usernames = request.POST.getlist("members")
                members = User.objects.filter(username__in=usernames)
                ticket = form.save(commit=False)
                ticket.project = project
                ticket.created_by = request.user
                ticket.status = "New"
                ticket.save()
            
                ticket.assign.set(members)
            
                return redirect(f"/project/{pk}")
        
        
        if "edit_team" in request.POST:            
            if request.POST.get("add_member", False):
                add_member = User.objects.get(username=request.POST["add_member"])
                project.members.add(add_member)
                
            if request.POST.get("rm_member", False):
                rm_member = User.objects.get(username= request.POST["rm_member"])
                project.members.remove(rm_member)

            return redirect(f"/project/{pk}")
    else:
        form = TicketForm()
    
    context ={
        "project":project,
        "tickets":ticket_list,
        "add_ticket": form,
        "available_dev": not_project_members,
        "team": team
        }
    
    return render(request, "main/p_detail.html", context)

@login_required
def ticket_detail(request, pk):
    team = Team.objects.get(name=request.user.team.all()[0])
    
    ticket = Ticket.objects.get(id=pk)
    status_choices = [x for x in Ticket.STATUS_CHOICES if x != (ticket.status, ticket.status)]
    priority_choices = [x for x in Ticket.PRIORITY_CHOICES if x != (ticket.priority, ticket.priority)]
    dev_not_assign = [x for x in team.members.all() if x not in ticket.assign.all()]
    
    comment_list = Comment.objects.filter(ticket=ticket)
    
    if request.method == "POST":
        
        if "add_comment" in request.POST:
            comment_form  = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.ticket = ticket
                comment.created_by = request.user
                comment.save()
            
            return redirect(f"/ticket/{pk}")
        
        if "edit_ticket" in request.POST:
            
            if request.POST.get("add_dev", False):
                add_dev = User.objects.get(username=request.POST["add_dev"])
                ticket.assign.add(add_dev)
                
            if request.POST.get("remove_dev", False):
                rm_dev = User.objects.get(username=request.POST["remove_dev"])
                ticket.assign.remove(rm_dev)
            
            ticket.status = request.POST["status"]
            ticket.priority = request.POST["priority"]
            ticket.save()
            return redirect(f"/ticket/{pk}")
            
    else:
        comment_form = CommentForm()
    
    context = {
        "ticket":ticket,
        "comments": comment_list,
        "comment_form": comment_form,
        "status_choices": status_choices,
        "priority_choices": priority_choices,
        "available_dev": dev_not_assign,
    }
    
    return render(request, "main/t_detail.html", context)

@login_required
def team(request, team_name):
    team = Team.objects.get(name=team_name)
    add_dev = [x for x in User.objects.all() if x not in team.members.all()]
    context ={
        "team": team,
        "available_dev": add_dev
    }
    
    return render(request, "main/team.html", context)

def kickout(request, team_name, pk):
    team = Team.objects.get(name=team_name)
     
    rm_user = User.objects.get(id=pk)
    rm_user_tickets = rm_user.my_jobs.all()
    
    for ticket in rm_user_tickets:
        ticket.assign.remove(rm_user)
    
    team.members.remove(rm_user)
    
    return redirect(f"/team/{team_name}")

@login_required
def personal(request, pk):
    user = User.objects.get(id=pk)
    tickets = Ticket.objects.filter(assign=user)
    projects = Project.objects.filter(members=user)
    
    context = {
        "tickets": tickets,
        "projects": projects,
    }

    return render(request, "main/personal.html",context)

@api_view(["GET"])
def TicketInfo(request, team_name):
    team = Team.objects.get(name=team_name)
    projects = Project.objects.filter(team=team)

    if request.method == "GET":
        dict = {
            "priority": {"Low": 0, "Medium": 0, "High": 0},
            "status": {"New":0, "In Progress": 0, "Resolved": 0},
            "type_of_bug": {"Issue": 0, "Bug": 0, "Feature request": 0},
        }
        
        tickets = Ticket.objects.filter(project__in=projects)
        serializer = TicketSerializer(tickets, many=True)
        for i in serializer.data:
            dict["priority"][i["priority"]] += 1
            dict["status"][i["status"]] += 1
            dict["type_of_bug"][i["type_of_bug"]] += 1

        return Response(dict)
    
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)