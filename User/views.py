from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from django.contrib import messages
from Properties.forms.properties_form import *

from Properties.models import Properties
from django.shortcuts import render, redirect, reverse
from User.forms.profile_form import *
from Transactions.models import Transactions


def register(request):
    if request.method == "POST":
        form = RegisterForm(data=request.POST)
        cities_form = CitiesForm(data=request.POST)
        addresses_form = AddressesForm(data=request.POST)
        profile_form = ProfileForm(data=request.POST)

        if cities_form.is_valid() and addresses_form.is_valid() and profile_form.is_valid and form.is_valid():

            country_input = cities_form.cleaned_data['country']
            cities_saved = cities_form.save(commit=False)
            cities_saved.country = country_input
            cities_saved.save()

            form_saved = form.save()
            address_saved = addresses_form.save(commit=False)
            profile_saved = profile_form.save(commit=False)

            address_saved.city = cities_saved
            addresses_form.save()

            profile_saved.address = address_saved
            profile_saved.user = form_saved
            profile_saved.save()

            messages.info(request, 'Your have created a new account successfully!')
            return HttpResponseRedirect('login')
        else:
            request.method = "GET"
            pass

    if request.method == "GET":
        return render(request, 'User/SignUp.html', {
            'form': RegisterForm(),
            'cities_form': CitiesForm(),
            'addresses_form': AddressesForm(),
            'profile_form': ProfileForm(),
        })


@login_required
def edit_account(request):
    user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        # User has some saved information and need to update them
        # Step 1: Parse data from POST.
        user_form = CustomUserChangeForm(instance=user, data=request.POST)

        cities_form = CitiesForm(instance=Cities.objects.get(id=request.user.profile.address.city.id),
                                 data=request.POST)

        addresses_form = AddressesForm(instance=Addresses.objects.get(city=request.user.profile.address.city),
                                       data=request.POST)

        profile_form = ProfileForm(instance=Profile.objects.get(user=request.user,
                                                                address=request.user.profile.address),
                                   data=request.POST)

        # Step 2: Validate parsed data.
        if user_form.is_valid() and cities_form.is_valid() and addresses_form.is_valid() and profile_form.is_valid():

            country_input = cities_form.cleaned_data['country']
            cities_saved = cities_form.save(commit=False)
            cities_saved.country = country_input

            user_form.save()
            cities_saved.save()
            addresses_form.save()
            profile_form.save()
            messages.info(request, 'Your have edited your account successfully!')
            return redirect(reverse('front_page_index'))

        # Validation failed - return same data parsed from POST.
        else:
            return render(request, 'User/ManageAccount.html', {
                'user_form': user_form,
                'cities_form': cities_form,
                'addresses_form': addresses_form,
                'profile_form': profile_form,
            })
    if request.method == "GET":
        # User has logged information and we want to GET all info
        if user.first_name != '':
            profile = Profile.objects.get(user=request.user)
            return render(request, 'User/ManageAccount.html', {
                'user_form': CustomUserChangeForm(instance=user),
                'cities_form': CitiesForm(instance=profile.address.city),
                'addresses_form': AddressesForm(instance=profile.address),
                'profile_form': ProfileForm(instance=profile),
            })


@login_required
def account_transactions(request):
    context = {
        'buy_transactions': Transactions.objects.filter(buyer=request.user.id),
        'sale_transactions': Transactions.objects.filter(property__is_active=False).filter(
            property__user_id=request.user.id)
    }
    print(context)
    return render(request, 'User/AccountTransactions.html', context)
    # })


# Goes to account profile
@login_required
def account(request):
    return render(request, 'User/AccountDetails.html', {
        'user': User.objects.get(pk=request.user.id),
        'properties': Properties.objects.filter(user=request.user).filter(is_active=True)
    })


# Edits property information
@login_required
def edit_property(request, id):
    property = Properties.objects.get(id=id)
    if request.method == 'POST':
        # User has a property and now needs to post changes
        # Step 2: Validate parsed data.
        tags_form = TagsForm(instance=property.detail.tags, data=request.POST)
        type_form = TypesForm(instance=property.detail.type, data=request.POST)
        cities_form = CitiesForm(instance=property.address.city, data=request.POST)
        addresses_form = AddressesForm(instance=property.address, data=request.POST)
        details_form = DetailsForm(instance=property.detail, data=request.POST)
        properties_form = PropertiesForm(instance=property, data=request.POST)
        # profile_form = ProfileForm(instance=Properties.objects.get(id=id).user, data=request.POST)
        # Step 2: Validate parsed data.

        if tags_form.is_valid() and type_form.is_valid() and cities_form.is_valid() and addresses_form.is_valid() \
                and details_form.is_valid() and properties_form.is_valid():
            # Firstly we need to clean the data
            # username_input =

            country_input = cities_form.cleaned_data['country']

            # We create saved objects where commit == False
            # We can access parameters when fixing constraints on tables
            city_saved = cities_form.save(commit=False)
            # profile_saved = profile_form.save(commit=False)
            address_saved = addresses_form.save(commit=False)
            tags_saved = tags_form.save()
            details_saved = details_form.save(commit=False)
            properties_saved = properties_form.save(commit=False)

            city_saved.country = country_input
            city_saved.save()

            address_saved.city = city_saved
            address_saved.save()

            # profile_saved.address = address_saved
            # profile_form.save()

            details_saved.tags = tags_saved
            details_saved.type = Types.objects.get(id=request.POST['type'])
            details_saved.save()

            properties_saved.address = address_saved
            properties_saved.detail = details_saved
            properties_saved.user = request.user
            properties_saved.is_active = True
            properties_saved.save()

            messages.info(request, 'Your have edited your property successfully!')
            return redirect(reverse('account_properties'))
        # Validation failed - return same data parsed from POST.
        else:
            return render(request, 'Properties/CreateProperty.html', {
                # not sure about having properties here
                'type_form': type_form,
                'cities_form': cities_form,
                'addresses_form': addresses_form,
                'tags_form': tags_form,
                'details_form': details_form,
                'properties_form': properties_form,
            })
    if request.method == "GET":
        # User has logged information and we want to GET all info
        return render(request, 'Properties/CreateProperty.html', {
            'tags_form': TagsForm(instance=property.detail.tags),
            'type_form': TypesForm(instance=property.detail.type),
            'cities_form': CitiesForm(instance=property.address.city),
            'addresses_form': AddressesForm(instance=property.address),
            'details_form': DetailsForm(instance=property.detail),
            'properties_form': PropertiesForm(instance=property),
        })


# Deletes property of site and database
@login_required
def sell_property(request, id):
    property = Properties.objects.get(id=id)
    property.is_active = False
    property.save()
    messages.info(request, 'Property has been bought successfully!')
    return


@login_required
def delete_property(request, id):
    property = Properties.objects.get(pk=id)
    property.delete()
    messages.info(request, 'Your have deleted your property from this system successfully!')
    return HttpResponseRedirect('/')


@login_required
def account_properties(request):
    return render(request, 'User/AccountProperties.html',
                  {'properties': Properties.objects.filter(user=request.user).filter(is_active=True)})


@login_required
def create_property(request):
    if request.method == "POST":
        type_form = TypesForm(data=request.POST)
        cities_form = CitiesForm(data=request.POST)
        addresses_form = AddressesForm(data=request.POST)
        tags_form = TagsForm(data=request.POST)
        details_form = DetailsForm(data=request.POST)
        properties_form = PropertiesForm(data=request.POST)
        if cities_form.is_valid() and addresses_form.is_valid() and type_form.is_valid and tags_form.is_valid() \
                and details_form.is_valid():
            # We need to clean 'country' data
            country_input = cities_form.cleaned_data['country']
            city_saved = cities_form.save(commit=False)
            address_saved = addresses_form.save(commit=False)
            tags_saved = tags_form.save()
            details_saved = details_form.save(commit=False)
            properties_saved = properties_form.save(commit=False)

            city_saved.country = country_input
            city_saved.save()

            address_saved.city = city_saved
            addresses_form.save()

            details_saved.tags = tags_saved
            details_saved.type = Types.objects.get(id=request.POST['type'])
            details_saved.save()

            properties_saved.address = address_saved
            properties_saved.detail = details_saved
            properties_saved.user = request.user
            properties_saved.is_active = True
            properties_saved.save()

            messages.info(request, 'Your have registered your property for sale successfully!')
            return HttpResponseRedirect('account')

        else:
            request.method = "GET"
            pass
    if request.method == "GET":
        return render(request, 'Properties/CreateProperty.html', {
            'type_form': TypesForm(),
            'cities_form': CitiesForm(),
            'addresses_form': AddressesForm(),
            'tags_form': TagsForm(),
            'details_form': DetailsForm(),
            'properties_form': PropertiesForm(),
        })
