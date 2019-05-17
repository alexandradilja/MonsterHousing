from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from Properties.forms.properties_form import *
from Properties.forms.search_form import SearchForm



def index(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            # user inputs
            country_input = form.cleaned_data['country']
            zip_input = form.cleaned_data['zip']
            # Type is multi select will be returned as list must iterate when comparing
            type_input_list = form.cleaned_data['type']
            size_input = form.cleaned_data['size']
            max_price_input = form.cleaned_data['max_price']
            tags_input = form.cleaned_data['tags']
            sort_input = form.cleaned_data['sort']
            rooms_input = form.cleaned_data['rooms']
            # print(Properties.objects.filter(
            #     address__city__zip__icontains=zip_input
            # ).values_list('address__city__zip', flat=False))

            print(country_input, str(zip_input), type_input_list, size_input, max_price_input, tags_input, sort_input)
            for prop in Properties.objects.all():
                # property values
                type_id = prop.detail.type_id
                zip = prop.address.city.zip
                size = prop.detail.size
                price = prop.detail.price
                tag_dungeon = prop.detail.tags.dungeon
                tag_elevator = prop.detail.tags.elevator
                tag_garage = prop.detail.tags.garage
                tag_bb = prop.detail.tags.near_bloodbank
                tag_se = prop.detail.tags.secret_entrance

                print('type id:' + str(type_id) + 'type:' + str(type) + 'zip: ' + str(zip) + 'size' + str(
                    size) + 'price' + str(price) + 'tags: ')
                for type_input in type_input_list:
                    print(type_input)
                    print(type_id)
                    if int(type_input) == int(type_id):
                        print(prop)
                        context = {'property': Properties.objects.get(id=18),
                                   'form': form}

                        return render(request, 'Properties/SearchBar.html', context)

    form = SearchForm()

    return render(request, 'Properties/SearchBar.html', {'form': form})


def search(request):
    if request.method == "POST":
        form = SearchForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/properties/search/')
        else:
            request.method = "GET"
            pass
    if request.method == "GET":
        return render(request, 'Properties/SearchBar.html', {
            'form': SearchForm()})


def result(request):

    pass