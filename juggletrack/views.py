from django.shortcuts import get_object_or_404, render_to_response
from models import Juggler

def index(request):
    jugglers = Juggler.objects.all().order_by('name')
    return render_to_response('index.html', {'jugglers': jugglers})

def juggler(request):
    juggler = get_object_or_404(Juggler, pk=request.GET['id'])
    achievements = juggler.achievement.order_by('points')
    return render_to_response('juggler.html', {'juggler': juggler,
                                               'achievements': achievements})
