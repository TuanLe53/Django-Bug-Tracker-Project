from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
USER = get_user_model()

class Team(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(USER, related_name="team")
    
    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    members = models.ManyToManyField(USER, related_name="project")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team_project")

    def __str__(self):
        return self.name

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved')
    ]
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High')
    ]
    TYPE_CHOICES = [
        ('Issue', 'Issue'),
        ('Bug', 'Bug'),
        ('Feature request', 'Feature request')
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete= models.CASCADE)
    created_by = models.ForeignKey(USER, on_delete= models.CASCADE, related_name='my_tickets')
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default='New')
    type_of_bug = models.CharField(max_length=15, choices=TYPE_CHOICES, default='Issue')
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default='Low')
    created_at = models.DateTimeField(auto_now_add=True)
    assign = models.ManyToManyField(USER, related_name='my_jobs', blank=True)
    
    def __str__(self):
        return self.name
    
    
class Comment(models.Model):
    created_by = models.ForeignKey(USER, on_delete= models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Comment of {self.created_by}"