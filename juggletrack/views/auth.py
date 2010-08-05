from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def register(request, juggler_id=None):
    if request.method == 'GET':
        context = {'request':request, 'juggler_id':juggler_id}
        return render_to_response('register.html', context)

    juggler = None
    if 'juggler_id' in request.POST:
        juggler = get_object_or_404(Juggler, pk=request.POST['juggler_id'])
    
    first = request.POST['first']
    last = request.POST['last']
    email = request.POST['email']
    password = request.POST['password']
    
    user = User.objects.create_user(email, email, password)
    user.first_name = first
    user.last_name = last
    user.save()
    
    #if there is a juggler account being claimed, delete the juggler that
    #was just created, unite the existing juggler account with the user,
    #and set the date created for the user account from the existing juggler
    if juggler is not None:
        #detach defunct juggler from user account
        dead_juggler = user.get_profile()
        dead_juggler.user = None
        dead_juggler.save()
        #attach existing juggler object to user
        juggler.user = user
        juggler.name = ''
        juggler.save()
        #copy date created from juggler object to user
        user.date_joined = juggler.date_created
        user.save()
        #delete defunct juggler object
        dead_juggler.delete()
    else:
        juggler = user.get_profile()

    #log the juggler in to their account
    user = authenticate(username=email, password=password)    
    login(request, user)

    #redirect the juggler to their page
    return HttpResponseRedirect(juggler.view())

def login_view(request):
    if request.method == 'GET':
        context = {'request':request}
        return render_to_response('login.html', context)

    #authenticate and login user
    errormsg = None
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(username=email, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            juggler = user.get_profile()
            return HttpResponseRedirect(juggler.view())
        else:
            errormsg = "Your account is not active."
    else:
        errormsg = "Unable to authenticate.  Maybe you mistyped your password."
    
    context = {'request': request, 'errormsg': errormsg}
    return render_to_response('login.html', context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('juggletrack.views.juggler.jugglers'))

