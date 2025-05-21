from django.db import models

class OSINTAnalysis(models.Model):
    domain = models.CharField(max_length=255)
    ports = models.JSONField()
    whois = models.TextField()
    dns = models.JSONField()
    dorks = models.JSONField()
    passive_osint = models.JSONField()
    analysis_summary = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Análisis OSINT de {self.domain} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
