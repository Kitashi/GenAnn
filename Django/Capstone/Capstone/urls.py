from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'genedb.views.index'),
    url(r'^result/$', 'genedb.views.result'),
    # url(r'^admin/', include(admin.site.urls)),
)
