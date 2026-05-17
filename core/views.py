from .models import LearningResource, WorkshopResource
from django.shortcuts import render, redirect, get_object_or_404
from .models import ContactMessage
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import GalleryImage
# Create your views here.
def home(request):
    gallery_images = GalleryImage.objects.all()

    context = {
        'gallery_images': gallery_images,
    }

    return render(request, 'core/index.html',context)


def Resources(request):
        learning_resources = LearningResource.objects.all()
        workshop_resources = WorkshopResource.objects.all()
        return render(request,
                       'core/resources.html',
                         {'learning_resources': learning_resources,
                          'workshop_resources': workshop_resources})

@login_required(login_url='login')
def access_resource(request, resource_type, pk):

    if resource_type == "learning":
        resource = get_object_or_404(LearningResource, pk=pk)
    else:
        resource = get_object_or_404(WorkshopResource, pk=pk)

    
    return redirect(resource.file.url)



def Contact(request):
    # PAGE LOAD
    if request.method == "GET":
        return render(request, "core/contact.html")

    # AJAX SUBMIT
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        if not all([name, email, subject, message]):
            return JsonResponse({
                "success": False,
                "message": "All fields are required."
            })

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        send_mail(
            subject=f"Contact Form: {subject}",
            message=f"From {name} <{email}>\n\n{message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=True
        )

        return JsonResponse({
            "success": True,
            "message": "Message sent successfully!"
        })