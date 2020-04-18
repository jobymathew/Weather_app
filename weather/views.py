from django.shortcuts import render, get_object_or_404, redirect
import requests
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=4b36aef44fa35bd58df44755b4a53cca'

    if request.method == "POST":
        form = CityForm(request.POST)
        form.save()
    
    form = CityForm()
    cities = City.objects.all()

    weather_data = []
    
    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city' : city,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form':form}

    return render(request,'weather/weather.html',context)

def delete(request,pk):
    city = get_object_or_404(City, pk=pk)
    city.delete()
    return redirect('/')
        