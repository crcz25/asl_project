from django.shortcuts import render, get_object_or_404, redirect

from .forms import ImageForm
from .models import Image


def index(request):
    # Get the 5 most recent images
    latest_image_list = Image.objects.order_by('-updated_at')[:5]
    # Pass the list of images to the template
    context = {
        'latest_image_list': latest_image_list,
    }
    return render(request, 'image_processing/index.html', context)


def detail(request, image_id):
    # Get the image with the specified id
    image = get_object_or_404(Image, pk=image_id)
    # Pass the image to the template
    context = {
        'image': image,
    }
    return render(request, 'image_processing/detail.html', context)


def upload(request):
    # If the request is a POST, create a form instance and populate it with data from the request
    form = ImageForm(request.POST or None, request.FILES or None)
    # If the request is not a POST, create an empty form
    context = {}
    if form.is_valid():
        form.save()
        return redirect('index')
    context['form'] = form
    return render(request, 'image_processing/upload.html', context)


def delete(request, image_id):
    # Get the image with the specified id
    image = get_object_or_404(Image, pk=image_id)
    # Pass the image to the template
    context = {}
    # If the request is a POST, delete the image
    if request.method == 'POST':
        # First delete the image from the file system
        image.path.delete()
        # Then delete the image from the database
        image.delete()
        return redirect('index')
    return render(request, 'image_processing/delete.html', context)


def update(request, image_id):
    # Get the image with the specified id
    image = get_object_or_404(Image, pk=image_id)
    # Pass the image to the template
    context = {
        'image': image,
    }
    # If the request is a POST, create a form instance and populate it with data from the request
    form = ImageForm(request.POST or None, request.FILES or None, instance=image)
    # If the request is not a POST, create an empty form
    context = {}
    if form.is_valid():
        form.save()
        return redirect('index')
    context['form'] = form
    return render(request, 'image_processing/update.html', context)
