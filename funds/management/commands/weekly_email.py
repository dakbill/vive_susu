from django.core.management.base import NoArgsCommand
from django.core.mail import send_mail
from funds.models import Member


class Command(NoArgsCommand):
    help = "Send weekly email to clients."

    def handle_noargs(self, **options):
        email = Member.objects.get(username='dakbill').email
        send_mail('Vive-susu weekly transaction', 'Here is the another message.', 'taichobill@gmail.com',
                  [email], fail_silently=False)
