from django.urls import path
from .views import DeepSeekAnalysisView

urlpatterns = [
    path('', DeepSeekAnalysisView.as_view(), name='deepseek'),
]
