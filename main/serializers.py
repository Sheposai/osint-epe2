from rest_framework import serializers

class OSINTInputSerializer(serializers.Serializer):
    domain = serializers.CharField()
    ports = serializers.ListField(child=serializers.IntegerField())
    whois = serializers.CharField()
