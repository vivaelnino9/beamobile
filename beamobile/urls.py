from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = [
    url(r'^', include('bea_app.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^friendship/', include('friendship.urls'))
]
