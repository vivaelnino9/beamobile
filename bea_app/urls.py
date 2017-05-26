from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings


from bea_app import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^confirm_email/(?P<user_id>[\w|\W]+)/(?P<confirmation_key>[\w|\W]+)/$',views.confirm_email, name='confirm_email'),
    url(r'^resend_email/(?P<email>[\w|\W]+)/$',views.resend_email, name='resend_email'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^challenge_list/$', views.challenge_list, name='challenge_list'),
    url(r'^challenge_detail/(?P<challenge_id>[\w|\W]+)/$', views.challenge_detail, name='challenge_detail'),
    url(r'^accept_challenge/(?P<challenge_id>[\w|\W]+)/$', views.accept_challenge, name='accept_challenge'),
]
