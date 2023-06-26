import openpyxl
import json
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from urllib.request import urlopen
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
        url = 'http://127.0.0.1:8000/api/news/'
        response = urlopen(url)
        data = json.loads(response.read())
        book = openpyxl.Workbook()
        book.remove(book.active)
        print(data)
        sheet_1 = book.create_sheet('Самолёты')
        for item in data['posts']:
            sheet_1.append([item['title'], item['full_text'], item['image'], item['date']])
        book.save('allnews.xlsx')
        book.close()
        lst = Articles.objects.all().values()
        return Response({'posts': list(lst)})


class NewsAPIView(APIView):
    def get(self, request):
        lst = Articles.objects.all().values()
        return Response({'posts': list(lst)})


class DetailNewsAPIView(APIView):
    def get(self, request, pk):
        post = Articles.objects.get(pk=pk)
        serializer_class = ArticlesSerializer(post)
        return Response(serializer_class.data)

    def post(self, request, pk):
        post = Articles.objects.get(pk=pk).values()
        serializer_class = ArticlesSerializer(post)
        return Response(serializer_class.data)
