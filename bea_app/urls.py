from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings


from bea_app import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/(?P<friend_id>[\w|\W]+)/(?P<organization_id>[\w|\W]+)/$', views.register, name='register'),
    url(r'^confirm_email/(?P<user_id>[\w|\W]+)/(?P<confirmation_key>[\w|\W]+)/$',views.confirm_email, name='confirm_email'),
    url(r'^resend_email/(?P<email>[\w|\W]+)/$',views.resend_email, name='resend_email'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^challenge_list/$', views.challenge_list, name='challenge_list'),
    url(r'^challenge_detail/(?P<challenge_id>[\w|\W]+)/$', views.challenge_detail, name='challenge_detail'),
    url(r'^accept_challenge/(?P<challenge_id>[\w|\W]+)/$', views.accept_challenge, name='accept_challenge'),
    url(r'^act_entry/$', views.act_entry, name='act_entry'),
    url(r'^my_activity/$', views.my_activity, name='my_activity'),
    url(r'^friend_request/$', views.friend_request, name='friend_request'),
    url(r'^friend_activity/$', views.friend_activity, name='friend_activity'),
    url(r'^accept_reject_request/(?P<request_id>[\w|\W]+)/(?P<accept>\d+)/$', views.accept_reject_request, name='accept_reject_request'),
    url(r'^remove_friend/(?P<friend_id>[\w|\W]+)/$', views.remove_friend, name='remove_friend'),
    url(r'^redeem_points/$', views.redeem_points, name='redeem_points'),
    url(r'^redeem_confirmation/(?P<discount_code>[\w|\W]+)/(?P<value>[\w|\W]+)/(?P<points>[\w|\W]+)/$', views.redeem_confirmation, name='redeem_confirmation'),
]
