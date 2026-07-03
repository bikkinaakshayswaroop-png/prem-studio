from django.db import models
from django.contrib.auth.models import User


class Booking(models.Model):

    EVENT_CHOICES = [
        ("Wedding", "Wedding"),
        ("Pre Wedding", "Pre Wedding"),
        ("Engagement", "Engagement"),
        ("Birthday", "Birthday"),
        ("Baby Shoot", "Baby Shoot"),
        ("Maternity", "Maternity"),
        ("Other", "Other"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    full_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=15)

    email = models.EmailField()

    event_type = models.CharField(
        max_length=50,
        choices=EVENT_CHOICES
    )

    event_date = models.DateField()

    location = models.CharField(max_length=200)

    message = models.TextField(blank=True)

    STATUS_CHOICES = [
    ("Pending", "Pending"),
    ("Approved", "Approved"),
    ("Completed", "Completed"),
    ("Cancelled", "Cancelled"),
    ]

    status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default="Pending"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.full_name
class Album(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.name}"

class Gallery(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    album_name = models.CharField(
    max_length=100,
    default="General"
)
    title = models.CharField(max_length=200)

    image = models.ImageField(
        upload_to="gallery/"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.user.username} - {self.album_name}"

    
class Video(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)

    video = models.FileField(upload_to="videos/")

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    profile_photo = models.ImageField(
        upload_to="profiles/",
        default="default.png",
        blank=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.user.username
    
