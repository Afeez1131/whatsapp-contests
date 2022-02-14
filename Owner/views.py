from django.http import HttpResponseRedirect
from django.shortcuts import (
    render,
    HttpResponse,
    redirect,
    get_object_or_404,
    get_list_or_404,
)
from django.urls import reverse
from django.contrib import messages
from auth_app.models import BusinessOwner
from base_app.models import Referral, Guest
from .forms import BusinessRegistrationForm, ReferralRegistration
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import re
from base_app.utils import create_shortcode
import urllib.parse


@login_required(login_url="account_login")
def ReferralHomeView(request, shortcode):
    business = BusinessOwner.objects.get(shortcode=shortcode)
    print("business", business)
    # get the instance of the business owner using shortcode

    if request.user.username == business.username:
        # test if the login user is equal to the user Business Owner
        share_message = (
            "Stand a chance of winning a cash/product of #"
            + str(business.cash_price)
            + " by "
            "referring people to " + business.business_name + ".\n Get started here: "
        )

        signup_url = request.build_absolute_uri(
            reverse("referral_register", args=(business.shortcode,))
        )

        if request.method == "POST":
            link = "https://wa.me/?text=" + urllib.parse.quote(
                share_message + signup_url
            )
            print("Link: ", link)
            return HttpResponseRedirect(link)
        return render(
            request,
            "Owner/referral_homepage.html",
            {
                "business": business,
                "share_message": share_message,
                "signup_url": signup_url,
            },
        )
    else:
        # messages.warning(request, "You do not have access to this page")
        return redirect("index")


@login_required(login_url="account_login")
def ReferralList(request, shortcode):
    business = get_object_or_404(BusinessOwner, shortcode=shortcode)
    # get a business owner with the shortcode passed as args
    # obj_list = get_list_or_404(Referral, business_owner=business)
    referral = Referral.objects.filter(business_owner=business)
    # referral = obj_list[0]
    # get the referral associated with the Business Owner
    return render(
        request,
        "Owner/referral_list.html",
        {"referral": referral, "business": business},
    )


# @login_required(login_url="account_login")
def RegisterRefer(request, shortcode):
    business = get_object_or_404(BusinessOwner, shortcode=shortcode)
    # get a business owner with the shortcode passed as args
    # obj_list = get_list_or_404(Referral, business_owner=business)
    referral = Referral.objects.filter(business_owner=business)

    # referral = obj_list[0]
    # get the referral associated with the Business Owner

    if request.method == "POST":
        form = ReferralRegistration(request.POST)
        # the registration form
        if form.is_valid():
            refer_name = form.cleaned_data["refer_name"]
            phone_number = form.cleaned_data["phone_number"]
            # get the refer_name and phone number from the post request
            try:
                # try to get the referral with the provided details
                # referral = Referral.objects.filter(business_owner=business)
                referral_instance = Referral.objects.get(
                    business_owner=business,
                    refer_name=refer_name,
                    phone_number=phone_number,
                )
            except Exception as ObjectDoesNotExist:
                # does not exist, create such referral
                # referral = Referral.objects.filter(business_owner=business)
                referral_instance = Referral(
                    business_owner=business,
                    refer_name=refer_name,
                    phone_number=phone_number,
                )
                shortcode = create_shortcode(referral_instance, size=4)
                referral_instance.ref_shortcode = shortcode
                print(
                    referral_instance.business_owner,
                    referral_instance,
                    referral_instance.ref_shortcode,
                )
                referral_instance.save()
                # save
                return redirect(
                    "referral_profile",
                    business.shortcode,
                    referral_instance.ref_shortcode,
                )
                # return HttpResponseRedirect(referral.referral_url)
            else:
                # if the referral exist, message notification
                messages.warning(
                    request,
                    "Referral "
                    + referral_instance.refer_name
                    + " exists, try again with a different Referral name",
                )
    form = ReferralRegistration()
    return render(
        request,
        "Owner/referral_register.html",
        {
            "form": form,
            "business": business,
            "referral": referral,
        },
    )


def ReferralProfile(request, shortcode, ref_shortcode):
    business = BusinessOwner.objects.get(shortcode=shortcode)
    # get a busines Owner instance using the shortcode args
    referral = Referral.objects.get(ref_shortcode=ref_shortcode)
    # get the referral with the referral shortcode passed as args also
    vote_url = request.build_absolute_uri(
        reverse("referral_home", args=(business.shortcode, referral.ref_shortcode))
    )
    referral_message = (
        "Hello, i am participating in a referral contest, the person with the highest "
        "vote wins the Cash/Gift price. kindly vote for me here:\n"
    )
    if request.method == "POST":
        referral_link = "https://wa.me/?text=" + urllib.parse.quote(
            referral_message + vote_url
        )
        # will encode the text and url to avoid errors

        # will handle the sharing of the message on whatsapp
        return HttpResponseRedirect(referral_link)

    return render(
        request,
        "Owner/referral_profile.html",
        {
            "business": business,
            "referral": referral,
            "vote_url": vote_url,
            "referral_message": referral_message,
        },
    )
