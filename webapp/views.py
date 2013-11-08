from rango.forms import UserForm, UserProfileForm

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import HttpRequest
from django.template import RequestContext
from django.shortcuts import render_to_response

def register(request):

    context = RequestContext(request)
	# boolean to show if user has registration
	registered = False
    # form data processing
    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        # if valid
        if user_form.is_valid() and profile_form.is_valid():
            # save to database
            user = user_form.save()
            user.set_password(user.password)
            user.save()	
			profile = profile_form.save(commit=False)
            profile.user = user
			if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']
            profile.save()
			registered = True
        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'webapp/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)
			
def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            # is it active?
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/webapp/')
            else:
                return HttpResponse("Disabled account.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        return render_to_response('webapp/index.html', {}, context)
		
@login_required
def restricted(request):
	return HttpResponse("You are logged in!")
	
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/webapp/')