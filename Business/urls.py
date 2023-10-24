from django.urls import path
from .views import FindBusinessAccounts

urlpatterns = [
    path('find_business_accounts/', FindBusinessAccounts.as_view(), name='find-business-accounts'),
]
