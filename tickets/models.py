from django.db import models
# from django.url import reverse

from django.conf import settings



# upload_location is the location of media file storage
def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)


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

        TODO:
    [8]: Staff can assign the ticket to a staff member. The staff member it is
         assinged to can then accept or reject it.
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
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    tag = models.CharField(
        max_length=30,
        choices=TAGS,
        default='BUG'
    )

    issue = models.CharField(max_length=300)

    content = models.TextField()

    image = models.ImageField(
        upload_to=upload_location,
        null=True,
        blank=True,
        width_field="width_field",
        height_field="height_field")

    height_field = models.IntegerField(default=0)

    width_field = models.IntegerField(default=0)

    updated = models.DateTimeField(
        auto_now=True,
        auto_now_add=False
    )

    timestamp = models.DateTimeField(
        auto_now=False,
        auto_now_add=True
    )

    ticket_state = models.CharField(
        max_length=10,
        choices=TICKET_STATE,
        default='PUB'
    )

    completion_state = models.CharField(
        max_length=30,
        choices=COMPLETION_STATE,
        default='REC'
    )

    # Meta class to determine the order sequence of tickets
    class Meta:
        ordering = ["-updated", "-timestamp"]


    # Class string as the issue name of ticket
    def __str__(self):
        return self.issue
