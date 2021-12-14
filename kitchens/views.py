
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render, HttpResponseRedirect
from .models import Kitchen, Review
from actions.models import Action
from .forms import KitchensForm
from django.contrib import messages
from django.http import JsonResponse
import boto3
from django.contrib.auth import authenticate
from django.template.loader import render_to_string

def index(request):

    actions = Action.objects.all()

    

    return render(request, 'index.html', {'actions': actions})
    
    


def addKitchen(request):

    # dictionary for initial data with
    # field names as keys

    context = {}
    

    # add the dictionary during initialization

    form = KitchensForm(request.POST or None)
    if form.is_valid():

        form.save()
        messages.success(request, 'Form submission successful')
    MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

    mturk = boto3.client('mturk',
    aws_access_key_id = "AKIAZSMOGL4AWXD7N6U6",
   aws_secret_access_key = "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",
   region_name='us-east-1',
   endpoint_url = MTURK_SANDBOX
)
    print("I have $" + mturk.get_account_balance()['AvailableBalance'] + " in my Sandbox account")

    question = render_to_string('questions.xml' )
    new_hit = mturk.create_hit(
    Title = 'Is this Tweet happy, angry, excited, scared, annoyed or upset?',
    Description = 'Read this tweet and type out one word to describe the emotion of the person posting it: happy, angry, scared, annoyed or upset',
    Keywords = 'text, quick, labeling',
    Reward = '0.15',
    MaxAssignments = 1,
    LifetimeInSeconds = 172800,
    AssignmentDurationInSeconds = 600,
    AutoApprovalDelayInSeconds = 14400,
    Question = question,
)

    print("A new HIT has been created. You can preview it here:")
    print("https://workersandbox.mturk.com/mturk/preview?groupId=" + new_hit['HIT']['HITGroupId'])
    print("HITID = " + new_hit['HIT']['HITId'] + " (Use to Get Results)")
    
    context['form'] = form
    return render(request, 'addKitchen.html', context)




def viewKitchen(request):

    kitchens = Kitchen.objects.all()

    return render(request, 'viewKitchen.html', {'kitchens': kitchens})

    



def kitchenDetail(request, id):

    # dictionary for initial data with
    # field names as keys

    context = {}

    # add the dictionary during initialization

    context['data'] = Kitchen.objects.get(id=id)

    return render(request, 'kitchenDetail.html', context)


def kitchenComment(request):
    if request.is_ajax():
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        comment = request.POST['comment']

        try:
            review = Review(first_name=first_name, last_name=last_name,
                            comment=comment)
            review.save()
            return JsonResponse({'success': 'success',
                                'first_name': review.first_name,
                                'comment': review.comment}, status=200)
        except Review.DoesNotExist:
            return JsonResponse({'error': 'there was an error'},
                                status=200)
    else:
        return JsonResponse({'error': 'there was an error'}, status=400)


# update view for details

def editKitchen(request, id):

    if request.method == 'POST':

        kitchen_name = request.POST['kitchen_name']
        kitchen_address = request.POST['kitchen_address']
        kitchen_desc = request.POST['kitchen_desc']
        cuisine_type = request.POST['cuisine_type']

        # kitchen_info = Kitchen( kitchen_name = kitchen_name,kitchen_address = kitchen_address,
        # kitchen_desc = kitchen_desc, cuisine_type = cuisine_type)

        kitchen_info = Kitchen.objects.get(id=id)

        kitchen_info.kitchen_name = kitchen_name
        kitchen_info.kitchen_address = kitchen_address
        kitchen_info.kitchen_desc = kitchen_desc
        kitchen_info.cuisine_type = cuisine_type

        kitchen_info.save()
        messages.info(request, 'Details updated successfully')
        return redirect('/kitchens/kitchenDetail/' + id)
    else:
        return render(request, 'editKitchen.html')


def deleteKitchen(request, id):

    # dictionary for initial data with
    # field names as keys

    context = {}

    # fetch the object related to passed id

    obj = get_object_or_404(Kitchen, id=id)

    if request.method == 'POST':

        # delete object

        obj.delete()

        # after deleting redirect to
        # home page

        return HttpResponseRedirect('/')

    messages.warning(request, 'Kitchen deleted!!')
    return render(request, 'deleteKitchen.html', context)
