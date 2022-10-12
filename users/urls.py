from django.urls import path
from . import views


app_name = 'users'

urlpatterns = [
    path('user-index', views.user_index, name='user-index'),
    path('file-complaint', views.file_complaint, name='file-complaint'),
    path('complaint-history', views.complaint_history, name='complaint-history'),
    path('user-profile', views.user_profile, name='user-profile'),
    path('user-password', views.user_password, name='user-password'),
    path('user-login', views.login_user, name='user-login'),
    path('user-logout', views.logoutUser, name='user-logout'),
    path('user-register', views.register_user, name='user-register'),
    path('complaint-type', views.complaint_type, name='complaint-type'),
    path('pending', views.pending, name='pending'),
    path('closed', views.closed, name='closed'),
    path('processed', views.processed, name='processed'),
    path('rejected', views.rejected, name='rejected'),
    path('manage-users', views.manage_users, name='manage-users'),
    path('admin-password', views.admin_password, name='admin-password'),
    path('admin-login', views.login_admin, name='admin-login'),
    path('homepage', views.homepage, name='homepage'),
    
    path('<int:complaint_id>/deletehistory/', views.hist_delete, name='deletehistory'),
    path('<int:complainttype_id>/deletectype/', views.complainttype_delete, name='deletectype'),
    
    
    
    path('<int:pending_id>/updatepending/', views.updatepending, name='updatepending'),
    path('<int:process_id>/updateprocess/', views.updateprocess, name='updateprocess'),
    path('<int:solved_id>/updatesolved/', views.updatesolved, name='updatesolved'),
    path('<int:rejected_id>/updaterejected/', views.updaterejected, name='updaterejected'),
]