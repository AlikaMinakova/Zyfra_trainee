from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from item.models import Item
from item.serializers import ItemSerializer

def hello(request):
    return HttpResponse("Привет, это просто текст!")

@api_view(['GET', 'POST'])
def get_items(request):
    if request.method == 'POST':
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)