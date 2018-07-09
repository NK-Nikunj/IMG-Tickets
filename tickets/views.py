from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404

from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required

# import mdels and forms
from .models import Ticket, Comment
from .forms import TicketForm, CommentForm, UpdateTicketForm



# View for public tickets
@login_required(login_url='/')
def public_tickets(request):
    if request.user.is_staff:
        return redirect('admin/')

    page_title = "Public Tickets"

    open_tickets_list = Ticket.objects.filter(open_state='Open', ticket_state='Public')
    closed_tickets_list = Ticket.objects.filter(open_state='Closed', ticket_state='Public')

    paginator_open = Paginator(open_tickets_list, 2)
    paginator_closed = Paginator(closed_tickets_list, 2)

    page_open = request.GET.get('page_open')
    open_tickets = paginator_open.get_page(page_open)

    page_closed = request.GET.get('page_closed')
    closed_tickets = paginator_closed.get_page(page_closed)

    context = {
        'title': page_title,
        'open_ticket_list': open_tickets,
        'closed_ticket_list': closed_tickets,
    }
    return render(request, "tickets/tickets.html", context)



# View for private tickets
@login_required(login_url='/')
def user_tickets(request):
    page_title = "Public Tickets"

    open_tickets_list = Ticket.objects.filter(
        open_state='Open',
        ticket_state='Public',
        user=request.user
    )
    closed_tickets_list = Ticket.objects.filter(
        open_state='Closed',
        ticket_state='Public',
        user=request.user
    )

    paginator_open = Paginator(open_tickets_list, 2)
    paginator_closed = Paginator(closed_tickets_list, 2)

    page_open = request.GET.get('page_open')
    open_tickets = paginator_open.get_page(page_open)

    page_closed = request.GET.get('page_closed')
    closed_tickets = paginator_closed.get_page(page_closed)

    context = {
        'title': page_title,
        'open_ticket_list': open_tickets,
        'closed_ticket_list': closed_tickets,
    }
    return render(request, "tickets/tickets.html", context)



# View for creating tickets
@login_required(login_url='/')
def create_ticket(request):
    page_type = "Create Ticket"
    form = TicketForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
        "page_type": page_type
    }
    return render(request, "tickets/form.html", context)



# View for ticket details
@login_required(login_url='/')
def ticket_detail(request, id=None):
    if request.user.is_staff:
        url = "admin/" + str(id)
        return redirect(url)

    instance = get_object_or_404(Ticket, id=id)

    form = CommentForm(request.POST or None)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.comment_on = instance
        comment.save()
        return HttpResponseRedirect(instance.get_absolute_url())

    comments = Comment.objects.filter(comment_on=id)

    context = {
        "title": "Detail",
        "instance": instance,
        "form": form,
        "comments": comments,
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



# View for admin. Admin can see everyone's public and private tickets
@login_required(login_url='/')
def user_admin_ticket(request):
    if not request.user.is_staff:
        raise Http404

    page_title = "All Tickets"

    open_tickets_list = Ticket.objects.filter(open_state='Open')
    closed_tickets_list = Ticket.objects.filter(open_state='Closed')

    paginator_open = Paginator(open_tickets_list, 2)
    paginator_closed = Paginator(closed_tickets_list, 2)

    page_open = request.GET.get('page_open')
    open_tickets = paginator_open.get_page(page_open)

    page_closed = request.GET.get('page_closed')
    closed_tickets = paginator_closed.get_page(page_closed)

    context = {
        'title': page_title,
        'open_ticket_list': open_tickets,
        'closed_ticket_list': closed_tickets,
    }
    return render(request, "tickets/tickets.html", context)



@login_required(login_url='/')
def ticket_admin_detail(request, id=None):
    if not request.user.is_staff:
        raise Http404

    instance = get_object_or_404(Ticket, id=id)
    update_ticket_status = UpdateTicketForm(
        request.POST or None,
        instance=instance
    )

    if update_ticket_status.is_valid():
        instance = update_ticket_status.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())

    form = CommentForm(request.POST or None)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.comment_on = instance
        comment.save()
        return HttpResponseRedirect(instance.get_absolute_url())

    comments = Comment.objects.filter(comment_on=id)

    context = {
        "title": "Detail",
        "instance": instance,
        "form": form,
        "update_ticket": update_ticket_status,
        "comments": comments,
    }

    return render(request, "tickets/detail_admin.html", context)
