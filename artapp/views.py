#https://bradmontgomery.net/blog/2008/07/16/django-generating-an-image-with-pil/
#going to use this later on to generate our ascii thumbnails if possible.

from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from artapp.forms import RegistrationForm, LoginForm, SubmitArtForm, VoteForm
from django.contrib.auth import authenticate, login, logout
from artapp.models import Art, Artist
from datetime import datetime
from django.shortcuts import redirect
from django.contrib import messages


@login_required
def SubmitArt(request):
#	if request.user.is_authenticated():
		if request.method == 'POST':
			form = SubmitArtForm(request.POST)
			#myslug=slugify(form.cleaned_data['title'])
			if form.is_valid():
				loggedinartist = Artist.objects.get_or_create(user=request.user)[0]
				art = Art(title=form.cleaned_data['title'], drawing = form.cleaned_data['drawing'], slug=slugify(form.cleaned_data['title']), creator=loggedinartist)
				art.save()	
				return HttpResponseRedirect('/TheAsciiArtDatabase/art/' + art.slug+'/')
			else:
				return render_to_response('submitart.html', {'form': form}, context_instance=RequestContext(request))
		
		else:
			form = SubmitArtForm()
			context = {'form': form}
			return render_to_response('submitart.html', context, context_instance=RequestContext(request))
#	else:
		#urlredirect = request.path|urlencode
#		urlredirect = request.path
#		return HttpResponseRedirect('/TheAsciiArtDatabase/login/')
		#return HttpResponseRedirect('/TheAsciiArtDatabase/login/?next='+urlredirect)
		#redirect('/TheAsciiArtDatabase/login/?next='+urlredirect)


def ShowAllArt(request):
	arts = Art.objects.all().order_by('title')
	#for art in arts:
	form = VoteForm()
	#context = ({'allartsalphabetised': arts})
	context = ({'allartsalphabetised': arts, 'form': form })
	#context = {'form': form}
	return render_to_response('index.html', context, context_instance=RequestContext(request))
	


def ArtistRegistration(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/TheAsciiArtDatabase/profile/')
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(username=form.cleaned_data['username'], email = form.cleaned_data['email'], password = form.cleaned_data['password'])
			user.save()
			artists = Artist(user=user, name=form.cleaned_data['name'], birthday=form.cleaned_data['birthday'], slug=slugify(form.cleaned_data['username']))
			artists.save()
			return HttpResponseRedirect('/TheAsciiArtDatabase/profile/')
		else:
			return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))
	else:
		''' user is not submitting the form, show them a blank registration form '''
		form = RegistrationForm()
		context = {'form': form}
		return render_to_response('register.html', context, context_instance=RequestContext(request))
'''
def UpvoteArt(request, artslug):	
	try:
		art = Art.objects.get(slug=artslug)
	except Art.DoesNotExist:
		return HttpResponseRedirect('/TheAsciiArtDatabase/pagenotfound/')
'''
	
def ShowSingleArt(request, artslug):
	try:
		art = Art.objects.get(slug=artslug)
	except Art.DoesNotExist:
		return HttpResponseRedirect('/TheAsciiArtDatabase/pagenotfound/')
	#except Art.DoesNotExist:
	context = {'art': art}
	return render_to_response('singleart.html', context, context_instance=RequestContext(request))
	#return render_to_response('pagenotfound.html', context, context_instance=RequestContext(request))

def ProfileRedirect(request):
	if not request.user.is_authenticated(): 
		return HttpResponseRedirect('/TheAsciiArtDatabase/login/') #double check
	#loggedinartist = Artist.objects.get_or_create(user=request.user)[0]
	loggedinartist = Artist.objects.get(user=request.user)
	return HttpResponseRedirect('/TheAsciiArtDatabase/user/' + loggedinartist.slug+'/')
	
#def Profile(request, artistslug):
def Profile(request, artistslug):
	#if not request.user.is_authenticated(): 
	#	return HttpResponseRedirect('/TheAsciiArtDatabase/login/') #double check
	try:
		artist = Artist.objects.get(slug=artistslug)
	except Artist.DoesNotExist:
		return HttpResponseRedirect('/TheAsciiArtDatabase/pagenotfound/')
		
	context = {'artist': artist}
#	if artist == Artist.objects.get_or_create(user=request.user)[0]:
	if request.user.is_authenticated() and artist == Artist.objects.get(user=request.user):
		return render_to_response('privateprofile.html', context, context_instance=RequestContext(request))
	else:
		return render_to_response('publicprofile.html', context, context_instance=RequestContext(request))
	
	
	
def LoginRequest(request):
		
		redirect_to = request.REQUEST.get('next', '')
		#if redirect_to == '':
		#	redirect_to= '/TheAsciiArtDatabase/profile/'
		if request.user.is_authenticated():
		#	return HttpResponseRedirect(redirect_to)
			return HttpResponseRedirect('/TheAsciiArtDatabase/profile/')
		if request.method == 'POST':
			form = LoginForm(request.POST)
			if form.is_valid():
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				artists = authenticate(username=username, password=password)
				if artists is not None:
					login(request, artists)
					#next = request.GET.get('next', None)
					#if next:
						#return redirect(next)
					#	return HttpResponseRedirect(next)
					
					return HttpResponseRedirect(redirect_to)
					#return HttpResponseRedirect(next)
				else:
					return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))
			else:
				return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))
		else:
			''' user is not submitting the form, show the login form '''
			
			if redirect_to == '/TheAsciiArtDatabase/submit/' :
				messages.info(request, 'You must log in to submit art!')
			form = LoginForm()
			context = {'form': form}
			return render_to_response('login.html', context, context_instance=RequestContext(request))
			#return render_to_response('login.html', { 'from' : request.GET.get('from', None) })
			
def LogoutRequest(request):
	logout(request)
	return HttpResponseRedirect('/TheAsciiArtDatabase/')