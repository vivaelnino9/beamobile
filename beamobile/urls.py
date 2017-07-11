from django.conf.urls import include, url
from bea_app.admin import admin_site


urlpatterns = [
    url(r'^', include('bea_app.urls')),
    url(r'^admin/', admin_site.urls),
    url(r'^friendship/', include('friendship.urls'))
]
