
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render, \
    HttpResponseRedirect

from .models import Kitchen, Review
from actions.models import Action
from .forms import KitchensForm
from django.contrib import messages
from django.http import JsonResponse


def index(request):

    actions = Action.objects.all()

    return render(request, 'index.html', {'actions': actions})


def addKitchen(request):

    # dictionary for initial data with
    # field names as keys

    context = {}
    user = User.objects.get(username=request.session.get('username'))

    # add the dictionary during initialization

    form = KitchensForm(request.POST or None)
    if form.is_valid():

        form.save()
        messages.success(request, 'Form submission successful')

    action = Action(user=user, verb='add a Kitchen', target=form)

    action.save()
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
