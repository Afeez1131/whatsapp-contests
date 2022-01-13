from django.urls import path
from . import views

urlpatterns = [
    path("<shortcode>/<ref_shortcode>", views.ReferralHome, name="referral_home"),
    path(
        "ref/<shortcode>/<ref_shortcode>",
        views.ReferRedirect,
        name="referral_redirect",
    ),
]
