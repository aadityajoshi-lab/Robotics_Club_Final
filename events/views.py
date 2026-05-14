from sched import Event
from django.shortcuts import render
from .models import Event , EventInfoCard
# Create your views here.

def Events(request):
    events = Event.objects.all().order_by('-date')
    info_cards = EventInfoCard.objects.all()
    return render(request, 
                  'events/events.html', 
                  {'events': events, 
                   'info_cards': info_cards
                   })
    
