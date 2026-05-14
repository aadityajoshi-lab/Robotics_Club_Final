from django.shortcuts import render
from .models import TeamMember
# Create your views here.
def Team(request):
    team_members = TeamMember.objects.all().order_by('position_order')
    return render(request, 'teams/team.html',
                   {'team_members': team_members})


