from django.db import models
from cloudinary_storage.storage import RawMediaCloudinaryStorage

class LearningResource(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(
        upload_to='learning_resources/',
        storage=RawMediaCloudinaryStorage(),  # 👈 Explicitly define raw file storage
        help_text="Upload PDF, DOCX, ZIP"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class WorkshopResource(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(
        upload_to='workshop_resources/',
        storage=RawMediaCloudinaryStorage(),  # 👈 Explicitly define raw file storage
        help_text="Upload PDF, DOCX, ZIP"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject