from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView

from .serializers import OSINTInputSerializer, OSINTAnalysisSerializer
from .deepseek import analyze_osint
from .dns_utils import get_dns_records
from .dork_search import search_dorks
from .passive_scan import passive_osint
from .models import OSINTAnalysis

from django.utils.dateparse import parse_datetime
from django.db.models import Q

# Nuevos imports para vista web y PDF
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa

# Vista para mostrar un análisis en la web
def analysis_detail_view(request, analysis_id):
    analysis = get_object_or_404(OSINTAnalysis, id=analysis_id)
    return render(request, 'main/analysis_detail.html', {'analysis': analysis})

# Vista para generar PDF del análisis
def generate_pdf_view(request, analysis_id):
    analysis = get_object_or_404(OSINTAnalysis, id=analysis_id)
    template = get_template('main/analysis_detail.html')
    html = template.render({'analysis': analysis})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_{analysis.domain}.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("Error al generar el PDF", status=500)
    return response

# Vista para analizar y guardar
class DeepSeekAnalysisView(APIView):
    def post(self, request):
        serializer = OSINTInputSerializer(data=request.data)
        if serializer.is_valid():
            input_data = serializer.validated_data

            domain = input_data['domain']
            ports = input_data['ports']
            whois = input_data['whois']

            dns_info = get_dns_records(domain)
            dork_results = search_dorks(domain)
            passive_info = passive_osint(domain)

            formatted = (
                f"Dominio: {domain}\n"
                f"Puertos abiertos: {ports}\n"
                f"WHOIS:\n{whois}\n\n"
                f"DNS:\n"
            )
            for rtype, values in dns_info.items():
                formatted += f"  {rtype}: {', '.join(values) if values else 'No encontrados'}\n"

            formatted += "\nGoogle Dorks encontrados:\n"
            for d in dork_results:
                formatted += f"  {d['dork']}: {', '.join(d['matches']) if d['matches'] else 'Sin resultados'}\n"

            formatted += "\nDatos pasivos:\n"
            formatted += f"  IP: {passive_info.get('ip')}\n"
            formatted += f"  Headers: {passive_info.get('http_headers')}\n"
            formatted += f"  WHOIS Info: {passive_info.get('whois_info')}\n"
            formatted += f"  Geolocalización IP: {passive_info.get('ip_geolocation')}\n"

            result = analyze_osint(formatted)

            OSINTAnalysis.objects.create(
                domain=domain,
                ports=ports,
                whois=whois,
                dns=dns_info,
                dorks=dork_results,
                passive_osint=passive_info,
                analysis_summary=result
            )

            return Response({
                "input": {
                    "domain": domain,
                    "ports": ports,
                    "whois": whois,
                    "dns": dns_info,
                    "dorks": dork_results,
                    "passive_osint": passive_info,
                },
                "analysis_summary": result
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista GET para obtener los análisis existentes
class OSINTAnalysisListView(ListAPIView):
    serializer_class = OSINTAnalysisSerializer

    def get_queryset(self):
        queryset = OSINTAnalysis.objects.all().order_by('-created_at')
        domain = self.request.query_params.get('domain')
        created_after = self.request.query_params.get('created_after')

        if domain:
            queryset = queryset.filter(domain__icontains=domain)
        if created_after:
            try:
                fecha = parse_datetime(created_after)
                if fecha:
                    queryset = queryset.filter(created_at__gte=fecha)
            except:
                pass

        return queryset
