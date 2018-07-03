from django.contrib import admin

# Import model to register
from .models import Ticket


class TicketModelAdmin(admin.ModelAdmin):

    # display in the order
    list_display = [
        "user",
        "tag",
        "__str__",
        "ticket_state",
        "completion_state",
        "updated",
        "timestamp"
    ]

    # Filter list tags
    list_filter = [
        "tag",
        "ticket_state",
        "completion_state",
        "updated",
        "timestamp"
    ]

    # Add search fields
    search_fields = [
        "question",
        "content"
    ]


    # Meta class to associate to model Ticket
    class Meta:
        model = Ticket



# Register with admin
admin.site.register(Ticket, TicketModelAdmin)
