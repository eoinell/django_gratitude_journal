from django.http import HttpResponseRedirect
def index(request):
    return redirect('/logger/')