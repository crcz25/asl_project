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
import base64
from tensorflow import keras


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
        # Verify that the image is in the request
        if 'img_base64' not in request.data:
            return Response({'error': 'No image in request'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the encoded image
        img_str_base64 = request.data['img_base64']
        # Decode the image
        data = base64.urlsafe_b64decode(img_str_base64)
        # Convert the image to numpy array
        np_buff = np.frombuffer(data, dtype=np.uint8)
        # Decode the image
        img = cv2.imdecode(np_buff, cv2.IMREAD_COLOR)
        classes = ['a', 'b', 'c', 'close', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'open', 'p',
                    'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        prediction = settings.MODEL_ASL.predict(np.array([img]), verbose=0)
        letter = classes[np.argmax(prediction)]
        confidence = np.max(prediction)
        print(f'Letter: {letter}, Confidence: {confidence}')

        payload = {
            'asl_letter': letter,
            'confidence': confidence
        }

        return Response(payload, status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
