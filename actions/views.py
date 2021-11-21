from django.shortcuts import render
from actions.models import Action
from django.contrib.auth.models import User
# Create your views here.
def viewFeed(request, username) :

    print("Name:",User.username)
    user = User.objects.get(username=username)

    action = Action(user=user, verb='added a Kitchen')

    action.save()
    return render(request, 'viewFeed.html', {'action': action})