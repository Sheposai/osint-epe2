from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OSINTInputSerializer
from .deepseek import analyze_osint

class DeepSeekAnalysisView(APIView):
    def post(self, request):
        serializer = OSINTInputSerializer(data=request.data)
        if serializer.is_valid():
            try:
                input_data = serializer.validated_data
                formatted = f"Dominio: {input_data['domain']}\nPuertos: {input_data['ports']}\nWHOIS: {input_data['whois']}"
                result = analyze_osint(formatted)
                return Response({"result": result})
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
