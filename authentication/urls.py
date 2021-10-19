# from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from . import views

app_name = "authentication"


urlpatterns = [
	path('signin/', views.SigninView.as_view(), name="signin"),
	path('signup/', views.SignupView.as_view(), name="signup"),
	path('signup/verify/<hashed_otp>/', views.signup_verify, name="signup_verify"),
	path('signout/', auth_views.LogoutView.as_view(), name="signout"),
	path('agents/', views.agent_list, name="agents"),
	path('add-agent/', views.add_agent, name="add_agent"),
	path('inspectors/', views.inspectors_list, name="inspectors"),
	path('add-inspector/', views.add_inspector, name="add_inspector"),

	# PASSWORD RESET URL 
    path('forget-password/', views.forget_password, name="forget_password"),
    path('forget-password/verify/<hashed_otp>/', views.verify_resetpass_email, name='verify_email'),
    path('forget-password/reset/<hashed_otp>/', views.reset_new_pass, name='reset_new'),
    path('forget-password/reset-success/', views.reset_success, name='reset_success'),
    path('resend-code/<hashed_otp>/', views.resend_code, name='resend_code'),

    # api call
    path('api/change-picture/', views.change_picture, name="change_picture"),

	re_path('^agent/details/(?P<id>\d+)/$', views.agent_detail, name="agent_details"),
	re_path('^inspector-details/(?P<id>\d+)/$', views.inspector_details, name="inspector_details"),
	re_path('^agent/delete/(?P<id>\d+)/$', views.delete_agent, name="delete_agent"),
]