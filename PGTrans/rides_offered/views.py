from django.shortcuts import render

def home(request):
    context = {
        'title': 'Rides offered'
    }
    return render(request, 'rides_offered/home.html', context)
