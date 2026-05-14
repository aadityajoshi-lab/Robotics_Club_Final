from django.db import models

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    total_time_of_event = models.TextField() 
    location = models.CharField(max_length=200)
    description = models.TextField()
    register_form = models.URLField(blank=True, null=True)
    image_poster = models.ImageField(upload_to='event_posters/', blank=True, null=True)
    def __str__(self):
        return self.title
    

class EventInfoCard(models.Model):
    event = models.ForeignKey(Event, related_name='info_cards', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    file_link = models.URLField(blank=True, null=True)  # link to PDF, Google Doc, etc.

    def __str__(self):
        return self.title