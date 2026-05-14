from django.db import models


class TeamMember(models.Model):

    FACULTY_CHOICES = [
        ('CE', 'Computer Engineering'),
        ('ARCH', 'Architecture'),
        ('CIVIL', 'Civil Engineering'),
        ('ECE', 'Electronics, Communication & Information Engineering'),
        ('EE', 'Electrical Engineering'),
    ]

    name = models.CharField(max_length=100)
    post = models.CharField(max_length=100)

    faculty = models.CharField(max_length=5, choices=FACULTY_CHOICES)

    batch = models.CharField(max_length=20, help_text="Example: 079 Batch")

    photo = models.ImageField(
        upload_to='team_photos/',
        help_text="Upload JPG or PNG image"
    )

    position_order = models.PositiveIntegerField(
        help_text="Lower number appears first (1 = President)"
    )

    # Profile (optional)
    profile_file = models.FileField(
        upload_to='team_files/',
        blank=True,
        null=True,
        help_text="Upload CV or related file (optional)"
    )
    profile_link = models.URLField(
        blank=True,
        null=True,
        help_text="External profile or portfolio link (optional)"
    )

    # ✅ Contact (optional)
    phone_number = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        help_text="Example: +977-98XXXXXXXX"
    )
    email = models.EmailField(
        blank=True,
        null=True,
        help_text="Example: member@gmail.com"
    )

    # ✅ Socials (optional)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['position_order']

    def __str__(self):
        return f"{self.name} | {self.post} | {self.get_faculty_display()} ({self.batch})"
