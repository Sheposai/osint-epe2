from django.urls import path
from .views import DeepSeekAnalysisView, OSINTAnalysisListView
from .views import analysis_detail_view, generate_pdf_view

urlpatterns = [
    path('', DeepSeekAnalysisView.as_view(), name='deepseek-analysis'),
    path('analyses/', OSINTAnalysisListView.as_view(), name='analyses-list'),
    path('analysis/<int:analysis_id>/', analysis_detail_view, name='analysis_detail'),
    path('analysis/<int:analysis_id>/pdf/', generate_pdf_view, name='analysis_pdf'),
]
