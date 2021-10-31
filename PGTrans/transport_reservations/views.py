from django.shortcuts import render

rides = [
    {
        'driver': 'Correy',
        'date': 'August 27, 2018',
        'dest': 'Javornik',
        'cost': '200'
    },
    {
        'driver': 'Jane',
        'date': 'August 28, 2018',
        'dest': 'Mikulcak',
        'cost': '210'
    },
]


def home(request):
    context = {
        'rides': rides,
        'title': 'Rides offered'
    }
    return render(request, 'transport_reservations/home.html', context)
