from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import direct_to_template
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TheAsciiArtDatabase.views.home', name='home'),
    # url(r'^TheAsciiArtDatabase/', include('TheAsciiArtDatabase.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
	 
	#(r'^$', direct_to_template, {'template': 'index.html'}),
	(r'^pagenotfound/$', direct_to_template, {'template': 'pagenotfound.html'}),
	(r'^$', 'artapp.views.ShowAllArt'),
	(r'^register/$', 'artapp.views.ArtistRegistration'),
	(r'^login/$', 'artapp.views.LoginRequest'),
	#(r'^login/(?P<nextURL>.*)$', 'artists.views.LoginRequest'),
	(r'^logout/$', 'artapp.views.LogoutRequest'),
	(r'^resetpassword/passwordsent/$', 'django.contrib.auth.views.password_reset_done'),
	(r'^resetpassword/$', 'django.contrib.auth.views.password_reset'),
	(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
	(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
	(r'^profile/$', 'artapp.views.ProfileRedirect'),
	(r'^user/(?P<artistslug>.*)/$', 'artapp.views.Profile'),
	(r'^art/(?P<artslug>.*)/$', 'artapp.views.ShowSingleArt'),
#	(r'^upvote/(?P<artslug>.*)/$', 'artapp.views.UpvoteArt'),
#	(r'^downvote/(?P<artslug>.*)/$', 'artapp.views.ShowSingleArt'),
	(r'^submit/$', 'artapp.views.SubmitArt'),
	#(r'^loginerror/$', 'artists.views.LoginError'),
	
	
)
