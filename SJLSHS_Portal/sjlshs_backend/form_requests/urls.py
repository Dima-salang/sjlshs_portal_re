from django.urls import path
from .views import request_view, GoodMoralView

urlpatterns = [
    path('requests', request_view, name='request_view'),
    path('good_moral', GoodMoralView.as_view(), name='good_moral'),
    
]