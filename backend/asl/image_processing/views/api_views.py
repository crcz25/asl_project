from image_processing.models import Image
from image_processing.serializers import ImageSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import cv2
import os
import numpy as np


# ImageList class for creating a list of images
class ImageList(APIView):
    """
    List all images, or create a new image.
    """

    def get(self, request, format=None):
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ImageDetail class for creating a detail view of an image
class ImageDetail(APIView):
    """
    Retrieve, update or delete an image.
    """

    def get_object(self, pk):
        try:
            return Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        image = self.get_object(pk)
        serializer = ImageSerializer(image)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        image = self.get_object(pk)
        serializer = ImageSerializer(image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        image = self.get_object(pk)
        # First delete the image from the file system
        image.path.delete()
        # Then delete the image from the database
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ImageDetect class for detecting the ASL sign in an image
class ImageDetect(APIView):
    """
    Detect the ASL sign in an image.
    """

    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            print("TUT")
            # Save the image to the database
            # serializer.save()
            # Get the latest image from the database
            img_latest = Image.objects.latest('updated_at')
            # Get the path to the image
            path = os.path.join(settings.MEDIA_ROOT, str(img_latest.path))
            print(img_latest.path.url)
            # Read the image using opencv
            img = cv2.imread(path)
            # PROCESS THE IMAGE HERE
            print(img.shape)

            # print(str(img_latest.path).replace('/', '\\'))
            # print(img_latest)
            # print(settings.MEDIA_ROOT)
            # Open the image using opencv
            # print(request.FILES['path'])
            # print(serializer)
            # print(serializer.data['path'])

            # Using REQUEST
            # data = request.FILES['path'].read()
            # img = np.asarray(bytearray(data), dtype="uint8")
            # img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    
            payload = {
                'image': img,
                'asl_letter': 'A',
            }
            print("TUT")
            return Response(payload, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
