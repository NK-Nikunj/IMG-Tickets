from django.contrib import admin

# Import model to register
from .models import Ticket, Comment


# Changes in the admin panel for better option availability
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
        "issue",
        "content"
    ]


    # Meta class to associate to model Ticket
    class Meta:
        model = Ticket



class CommentModelAdmin(admin.ModelAdmin):

    # display in order
    list_display = [
        "user",
        "comment_on",
        "comment",
        "updated",
        "timestamp"
    ]

    # Filter list tags
    list_filter = [
        "user",
        "comment_on",
        "updated",
        "timestamp"
    ]

    # Add search fields
    search_fields = [
        "comment"
    ]


    # Meta class to associate to model Comment
    class Meta:
        model = Comment


# Register with admin
admin.site.register(Ticket, TicketModelAdmin)
admin.site.register(Comment, CommentModelAdmin)
