from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from notification.models import Notice

@login_required
def inbox(request):
    notices = Notice.objects.notices_for(request.user, sent=True)
    
    extra_content = {'notices':notices}
    return direct_to_template(request,
                              'notification/inbox.html',
                              extra_content)


@login_required
def question(request):
    """
    
    Arguments:
    - `request`:
    """
    pass
