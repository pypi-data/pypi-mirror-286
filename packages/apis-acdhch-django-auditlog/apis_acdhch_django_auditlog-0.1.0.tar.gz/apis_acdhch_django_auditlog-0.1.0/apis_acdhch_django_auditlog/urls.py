from django.urls import path
from apis_acdhch_django_auditlog.views import UserAuditLog


urlpatterns = [path("auditlog", UserAuditLog.as_view()),]
