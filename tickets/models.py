from django.db import models
from django.urls import reverse

from django.conf import settings



# upload_location is the location of media file storage
def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)


# Ticket model for the ticketing app
class Ticket(models.Model):

    """
    Ticket model gives the following features to the user and staff:

    [1]: Creating a ticket links the ticket to the user creating the ticket.
    [2]: User can add images to the ticket (in case they wish to).
    [3]: User can open/close/reopen the ticket as per their will.
    [4]: User 'HAS' to add a brief summary of the issue as well. Adding issue
         will not suffice.
    [5]: User can add tags (Bug report/Account Issue/Feature Request/ Other)
         in their ticket.
    [6]: User can create private tickets if they wish to. Created tickets will
         default to public.
    [7]: There are various states of a ticket namely Received -> Already working
         -> Resolved. In case an issue is infeasible/non-reasonable then staff
         can assign it a state of 'not possible'. States can ONLY be assigned by
         staff.
    [8]: User has the right to edit/delete his/her post at any time. Doing so
         will update time accordingly. For this reason this model has 2
         DateTimeField instead of 1.

        TODO:
    [1]: Staff can assign the ticket to a staff member. The staff member it is
         assinged to can then accept or reject it.
    [2]: Show edit history of ticket raised so that others can look into
         previous versions of the ticket.
    """

    # choice for tags
    TAGS = (
        ('BUG', 'Bug Reports'),
        ('ACC_ISSUE', 'Account Issue'),
        ('F_REQ', 'Feature Request'),
        ('O', 'Any other Request'),
    )

    # choice for Ticket
    TICKET_STATE = (
        ('PUB', 'Public'),
        ('PRI', 'Private'),
    )

    # choice for State (only for Staff)
    COMPLETION_STATE = (
        ('REC', 'Received'),
        ('WOR', 'Already working'),
        ('RES', 'Resolved'),
        ('N_POS', 'Not Possible'),
    )

    # Model fields starts here

    # Reference to User on Ticket creation
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    # Tag for ticket
    tag = models.CharField(
        max_length=30,
        choices=TAGS,
        default='BUG'
    )

    # Issue that is bothering
    issue = models.CharField(max_length=300)

    # Brief expanation of the issue
    content = models.TextField()

    # Image reference to the issue
    image = models.ImageField(
        upload_to=upload_location,
        null=True,
        blank=True,
        width_field="width_field",
        height_field="height_field")

    height_field = models.IntegerField(default=0)

    width_field = models.IntegerField(default=0)

    # Updated timestamp for Ticket
    updated = models.DateTimeField(
        auto_now=True,
        auto_now_add=False
    )

    # Created timestamp for Ticket
    timestamp = models.DateTimeField(
        auto_now=False,
        auto_now_add=True
    )

    # Status of Ticket
    ticket_state = models.CharField(
        max_length=10,
        choices=TICKET_STATE,
        default='PUB'
    )

    # Completion state of Ticket
    completion_state = models.CharField(
        max_length=30,
        choices=COMPLETION_STATE,
        default='REC'
    )


    # Meta class to determine the order sequence of tickets
    class Meta:
        ordering = [
            "-updated",
            "-timestamp"
        ]


    # Class string as the issue name of ticket
    def __str__(self):
        return self.issue


    # function for reversing
    def get_absolute_url(self):
        return reverse("tickets:ticket_detail", kwargs={"id": self.id})



# Comments model for the ticketing app
class Comment(models.Model):

    """
    Comment feature provides the following features to the User and Staff:

    [1]: Creating a comment references itself with User and Ticket raised.
    [2]: User/Staff can create/edit/delete comments. In addition,
         Staff can delete comments of other users provided they are not
         staff as well.

        TODO:
    [1]: Provide version history of edited comments for better understanding.
    [2]: Provide a way to reference one comment with some other ticket
         (something similar to GitHub's reference system).
    """

    # Ticket reference to comment
    comment_on = models.ForeignKey(
        'tickets.Ticket',
        on_delete=models.CASCADE,
    )

    # User reference to comment
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    # Comment for the ticket
    comment = models.TextField()

    # Updated timestamp for Comment
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    # Created at timestamp for Comment
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)


    # Meta class for ordering
    class Meta:
        ordering = [
            "-updated",
            "-timestamp"
        ]

    # Class string as the comment iself
    def __str__(self):
        return self.comment
