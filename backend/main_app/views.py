from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer


class MainPage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'

    def get(self, _):
        return Response({})


class TestAPI(APIView):
    def get(self, _):
        return Response({"success": True, "data": "Test API success"})
