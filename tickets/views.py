from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404

from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required

# import mdels and forms
from .models import Ticket, Comment
from .forms import TicketForm, CommentForm



# View for public tickets
@login_required(login_url='/')
def public_tickets(request):
    page_title = "Public Tickets"

    pub_tickets_list = Ticket.objects.filter(ticket_state='Public')
    paginator = Paginator(pub_tickets_list, 10)

    page = request.GET.get('page')
    pub_tickets = paginator.get_page(page)

    context = {
        'title': page_title,
        'ticket_list': pub_tickets,
    }
    return render(request, "tickets/tickets.html", context)



# View for private tickets
@login_required(login_url='/')
def user_tickets(request):
    page_title = "Public Tickets"

    pri_tickets_list = Ticket.objects.filter(ticket_state='Private', user=request.user)
    paginator = Paginator(pri_tickets_list, 10)

    page = request.GET.get('page')
    pri_tickets = paginator.get_page(page)

    context = {
        'title': page_title,
        'ticket_list': pri_tickets,
    }
    return render(request, "tickets/tickets.html", context)



# View for creating tickets
@login_required(login_url='/')
def create_ticket(request):
    page_type = "Create Ticket"
    form = TicketForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        instance.user = request.user
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
        "page_type": page_type
    }
    return render(request, "tickets/form.html", context)



# View for ticket details
@login_required(login_url='/')
def ticket_detail(request, id=None):
    instance = get_object_or_404(Ticket, id=id)

    context = {
        "title": "Detail",
        "instance": instance
    }
    return render(request, "tickets/detail.html", context)



# View for editing ticket
@login_required(login_url='/')
def edit_ticket(request, id=None):
    instance = get_object_or_404(Ticket, id=id)

    if instance.user != request.user:
        raise Http404

    form = TicketForm(
        request.POST or None,
        request.FILES or None,
        instance=instance
    )

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'title': 'Update',
        'instance': instance,
        'form': form
    }
    return render(request, "tickets/form.html", context)



#View for deleting ticket
@login_required(login_url='/')
def delete_ticket(request, id=None):
    instance = get_object_or_404(Ticket, id=id)
    if instance.user != request.user:
        if not request.user.is_staff:
            raise Http404

    instance.delete()
    return redirect("tickets:public_tickets")



@login_required(login_url='/')
def user_admin_ticket(request):
    pass



@login_required(login_url='/')
def ticket_admin_detail(request):
    pass
