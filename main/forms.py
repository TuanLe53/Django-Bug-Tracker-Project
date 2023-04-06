from django.forms import ModelForm
from django import forms
from .models import Ticket, Project, Comment
from django.contrib.auth.models import User


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ["name", "description", "type_of_bug", "priority"]
        
    
        
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description"]

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]