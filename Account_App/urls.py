from django.urls import path
from .views import AccountLoginView, AccountLogoutView, UserAccountUpdateView, BusinessAccountUpdateView

urlpatterns = [
    path('account/update/user/', UserAccountUpdateView.as_view(), name='user-account-update'),
    path('account/update/business/', BusinessAccountUpdateView.as_view(), name='business-account-update'),
    path('account/login/', AccountLoginView.as_view(), name='account-login'),
    path('account/logout/', AccountLogoutView.as_view(), name='account-logout'),
]
