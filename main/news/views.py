import io
from django.http import HttpResponse
import openpyxl
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import Articles
from .serializers import ArticlesSerializer


def index(request):
    news = Articles.objects.order_by('-date')
    return render(request, 'main/index.html', {'main': news})

def my_view(request):
    if request.metod == 'POST':
        image = request.FILES.get('image')
        if image:
            Articles.objects.create(image=image)
    context = {
        'objects': Articles.objects.all()
    }
    return render(request, 'main/index.html', context)


class FileDetailNewsAPIView(APIView):
    def get(self, request):
        queryset = Articles.objects.all()
        data = ArticlesSerializer(queryset, many=True).data
        book = openpyxl.Workbook()
        sheet_1 = book.active
        sheet_1.title = 'Самолёты'
        for item in data:
            sheet_1.append([item['title'], item['full_text'], item['image'], item['date']])
        file_stream = io.BytesIO()
        book.save(file_stream)
        file_stream.seek(0)

        response = HttpResponse(file_stream, content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="allnews.xlsx"'

        return response

class NewsModelViewSet(viewsets.ModelViewSet):
    queryset = Articles.objects.all()
    serializer_class = ArticlesSerializer
