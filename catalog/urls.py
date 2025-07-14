from django.urls import re_path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    re_path(r'$', views.mainClass.as_view(), name='main'),
    re_path(r'signup/$', views.signup_view, name='signup'),
    re_path(r'login/$', views.login_view, name='login'),
    re_path(r'logout/$', LogoutView.as_view(next_page='/'), name='logout'),
    re_path("password_reset/$", views.ResetPasswordView.as_view(), name="password_reset"),
    re_path(r'analize/$', views.analize_view, name='analize_file'),
    re_path(r'my-results/$', views.MyResultsListView.as_view(), name='my_results'),
    re_path(r'my-results/(?P<pk>\d+)$', views.MediaDetailView.as_view(), name='media_detail'),
]