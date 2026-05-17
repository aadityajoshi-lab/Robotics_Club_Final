from django.contrib import admin
from .models import LearningResource, WorkshopResource, ContactMessage
# Register your models here.
from .models import GalleryImage

admin.site.register(GalleryImage)
admin.site.register(LearningResource)
admin.site.register(WorkshopResource)
admin.site.register(ContactMessage)