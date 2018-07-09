from django import forms

from .models import Ticket, Comment

from pagedown.widgets import PagedownWidget

# Form for Ticket
class TicketForm(forms.ModelForm):
    """
    Basic Design for the Ticket form
    """

    content = forms.CharField(widget=PagedownWidget)
    # Meta class to associate to model and add desired fields
    class Meta:
        model = Ticket
        fields = [
            "tag",
            "issue",
            "content",
            "image",
            "ticket_state"
        ]


# Update form for admin
class UpdateTicketForm(forms.ModelForm):
    """
    Basic Design for the Ticket form
    """
    class Meta:
        model = Ticket
        fields = [
            "completion_state",
            "open_state",
        ]



# Form for Comment
class CommentForm(forms.ModelForm):
    """
    Basic design for the Comment form
    """

    # Meta class to associate to model and add desired fields
    class Meta:
        model = Comment
        fields = [
            "comment"
        ]
