from django.shortcuts import render
from django.http import HttpResponse

# import Ticket model from models.py
from .models import Ticket


# View for public tickets
def public_tickets(request):
    pass

# View for private tickets
def user_tickets(request):
    pass

# View for creating tickets
def create_ticket(request):
    pass

# View for ticket details
def ticket_detail(request, id=None):
    pass

# View for editing ticket
def edit_ticket(request, id=None):
    pass

#View for deleting ticket
def delete_ticket(request, id=None):
    pass
