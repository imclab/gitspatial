from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^v1/', include('gitspatial.api.v1.urls')),
    # Later, we can add a v2/ here to make versioning easier
)
