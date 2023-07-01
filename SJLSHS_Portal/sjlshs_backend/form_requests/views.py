from django.shortcuts import render
from .models import Request, GoodMoral
from django.views import View
from django.shortcuts import redirect
from .forms import GoodMoralForm


# Create your views here.

def request_view(request):
    requests = Request.objects.all()
    

    context = {
        'requests': requests
    }

    return render(request, 'requests/requests.html', context)



class GoodMoralView(View):
    def get(self, request):
        form = GoodMoralForm(user=request.user)  # Assuming you have a form for this model
        return render(request, 'requests/goodmoral.html', {'form': form})
    
    def post(self, request):
        user = request.user
        form = GoodMoralForm(request.POST, user=user)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.full_name = user
            instance.grade_level = user.grade_year
            instance.lrn = user.lrn
            instance.email = user.email
            instance.save()
            return redirect('request_view')
        return render(request, 'requests/goodmoral.html', {'form': form})