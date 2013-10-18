from django.conf.urls import patterns, include, url

from django.conf import settings


from django.contrib import admin
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url("", include('django_socketio.urls')),
    # Examples:
    # url(r'^$', 'rpi_web.views.home', name='home'),
    
    url(r'^$', 'index.views.to_index'),
    url(r'^index$', 'index.views.index'),

    url(r'^mando$', 'mando.views.mando'),

    url(r'^log$', 'logger.views.log'),

    url(r'^navigation$', 'navigation.views.navigation'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
