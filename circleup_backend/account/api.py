from django.http import JsonResponse
from rest_framework.decorators import api_view,authentication_classes, permission_classes

from .forms import SignUpForm


# authentication and permission classes are empty so that we
# we can acces this controller without being logged in
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data=request.data
    message='success'

    # validating incoming data
    form=SignUpForm({
        'email':data.get('email'),
        'name':data.get('name'),
        'password1':data.get('password1'),
        'password2':data.get('password2')
    })

    if form.is_valid():
        form.save()

        # SEND VERIFICATION EMAIL LATER!!

    else: 
        message=form.errors

    return JsonResponse({'status':message})