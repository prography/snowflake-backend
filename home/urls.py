from django.urls import path

from home.views import WelcomeCardListReadView

app_name = 'home'

urlpatterns = [
    path('welcome-cards/', WelcomeCardListReadView.as_view(), name='welcome-cards')
]
