from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^index/$', 'input_parameters.views.index', name='index'),
    url(r'^search/$', 'input_parameters.views.search', name='search_criteria'),
    url(r'^content/$', 'input_parameters.views.content', name='content'),
    url(r'^details/$', 'input_parameters.views.details', name='details'),
    url(r'^addtional_info/$', 'input_parameters.views.additional_info', name='addtional_info'),

    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
