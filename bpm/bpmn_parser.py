from bpm.models import *
from rest_framework.views import APIView
from bpm.serializers import *
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
import logging
from bpm.utils.services import parse_and_sync_xml

import xml.etree.ElementTree as ET

logger = logging.getLogger('bpm')

class ProcessViewSet(ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        logger.info(f"Received create request: {request.data}")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        process_instance = serializer.save()
        parse_and_sync_xml(process_instance)
        return Response(serializer.data, status=201)

    def update(self, request, *args, **kwargs):
        logger.info(f"Received update request: {request.data}")
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        process_instance = serializer.save()
        parse_and_sync_xml(process_instance)
        return Response(serializer.data)


class ProcessUpdateXmlView(APIView):

    def put(self, request, pk):
        logger.debug(f"request.data: {request.data}")
        try:
            process_instance = Process.objects.get(pk=pk)
        except Process.DoesNotExist:
            logger.error(f"Процесс с id={pk} не найден")
            return Response({"error": f"Процесс с id={pk} не найден"}, status=404)

        xml_str = request.data.get("xml")
        if not xml_str:
            logger.error("XML не передан в теле запроса")
            return Response({"error": "XML не передан"}, status=400)

        logger.debug(f"Обновляем XML для процесса {process_instance.id}")
        process_instance.bpmn_xml.xml = xml_str
        process_instance.bpmn_xml.save()
        parse_and_sync_xml(process_instance)
        return Response({"message": "XML обновлён и элементы синхронизированы"})

