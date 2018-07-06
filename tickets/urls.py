from django.urls import path

# import views to associate urls
from . import views

app_name = 'tickets'
urlpatterns = [
    path('', views.public_tickets, name='public_tickets'),
    path('private/', views.user_tickets, name='user_tickets'),
    path('create/', views.create_ticket, name='create_ticket'),
    path('<int:id>', views.ticket_detail, name='ticket_detail'),
    path('<int:id>/edit', views.edit_ticket, name='edit_ticket'),
    path('<int:id>/delete', views.delete_ticket, name='delete_ticket'),
    path('admin/', views.user_admin_ticket, name='user_admin_ticket'),
    path('admin/<int:id>', views.ticket_admin_detail, name='ticket_admin_detail'),
]
