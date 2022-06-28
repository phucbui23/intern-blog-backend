from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from tag.models import Tag, BlogTag
from tag.serializers import TagSerializer, BlogTagSerializer

@api_view(['GET','POST'])
def create_tag(request):
    if request.method == 'GET':
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def create_blogtag(request):
    if request.method == 'GET':
        blogtags = BlogTag.objects.all()
        serializer = BlogTagSerializer(blogtags, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = BlogTagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)