from rest_framework import serializers
from .models import Ticket, Project

class TicketSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ticket
        fields = ["name", "status", "type_of_bug", "priority"]