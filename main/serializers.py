from rest_framework import serializers
from .models import OSINTAnalysis

class OSINTInputSerializer(serializers.Serializer):
    domain = serializers.CharField(help_text="Dominio objetivo, por ejemplo: example.com")
    ports = serializers.ListField(child=serializers.IntegerField(min_value=1, max_value=65535))
    whois = serializers.CharField()

class OSINTAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = OSINTAnalysis
        fields = '__all__'
