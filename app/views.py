from urllib import request

from django.shortcuts import render, redirect
from .forms import BookingForm
from .models import Booking, Gallery,Video,Profile
from.forms import BookingForm,ProfileForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Gallery
from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import os
import zipfile
from django.http import HttpResponse
from django.conf import settings
import random
from .forms import BookingForm, ProfileForm, GalleryForm

from django.core.mail import send_mail

from django.contrib import messages


def home(request):

    form = BookingForm()

    if request.method == "POST":

        form = BookingForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("/")

    return render(request, "home.html", {
        "form": form
    })


def booking(request):

    form = BookingForm()

    if request.method == "POST":

        form = BookingForm(request.POST)

        if form.is_valid():

            booking = form.save(commit=False)

            if request.user.is_authenticated:
                booking.user = request.user

            booking.save()

            return redirect("/booking/")

    return render(request, "booking.html", {
        "form": form
    })


def register(request):

    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            return render(request, "auth/register.html", {
                "error": "Username already exists"
            })

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect("login")

    return render(request, "auth/register.html")


def user_login(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("dashboard")

        return render(request, "auth/login.html", {
            "error": "Invalid Username or Password"
        })

    return render(request, "auth/login.html")

@login_required
def dashboard(request):

    bookings = Booking.objects.filter(user=request.user)
    gallery = Gallery.objects.filter(user=request.user)
    videos = Video.objects.filter(user=request.user)

    context = {
        "bookings": bookings,
        "gallery": gallery,
        "total_bookings": bookings.count(),
        "total_photos": gallery.count(),
        "total_videos": videos.count(),
    }

    return render(
        request,
        "customer/dashboard.html",
        context
    )

@login_required
def customer_gallery(request):

    photos = Gallery.objects.filter(user=request.user)
    return render(
        request,
        "customer/gallery.html",
        {
            "photos": photos
        }
    )
    
@login_required
def customer_videos(request):

    videos = Video.objects.filter(user=request.user)

    return render(
        request,
        "customer/videos.html",
        {
            "videos": videos
        }
    )
    
@login_required
def download_album(request):

    photos = Gallery.objects.filter(user=request.user)

    zip_path = os.path.join(
        settings.MEDIA_ROOT,
        f"{request.user.username}_album.zip"
    )

    with zipfile.ZipFile(zip_path, "w") as zipf:

        for photo in photos:

            if photo.image:
                zipf.write(
                    photo.image.path,
                    os.path.basename(photo.image.path)
                )

    with open(zip_path, "rb") as f:

        response = HttpResponse(
            f.read(),
            content_type="application/zip"
        )

        response["Content-Disposition"] = (
            f'attachment; filename="{request.user.username}_album.zip"'
        )

        return response
    
@login_required
def profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect("profile")

    else:

        form = ProfileForm(instance=profile)

    return render(
        request,
        "customer/profile.html",
        {
            "form": form
        }
    )
    
@staff_member_required
def admin_dashboard(request):

    context = {

        "total_bookings": Booking.objects.count(),

        "total_customers": User.objects.count(),

        "total_photos": Gallery.objects.count(),

        "total_videos": Video.objects.count(),

        "recent_bookings": Booking.objects.order_by("-created_at")[:5],

    }

    return render(
        request,
        "adminpanel/dashboard.html",
        context
    )
    
from django.http import JsonResponse


def booking_events(request):

    bookings = Booking.objects.all()

    events = []

    for booking in bookings:

        events.append({

            "title": booking.event_type,

            "start": str(booking.event_date),

            "color": "#dc3545",

        })

    return JsonResponse(events, safe=False)
def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get("email")

        user = User.objects.filter(email=email).first()

        if not user:
            messages.error(request, "Email not registered.")
            return render(request, "auth/forgot_password.html")

        otp = random.randint(100000, 999999)

        request.session["reset_otp"] = str(otp)
        request.session["reset_email"] = email

        send_mail(
            "Prem Studio Password Reset OTP",
            f"Your OTP is: {otp}",
            "premstudio3033@gmail.com",
            [email],
            fail_silently=False,
        )

        messages.success(request, "OTP has been sent to your email.")
        return redirect("verify_otp")

    return render(request, "auth/forgot_password.html")

def verify_otp(request):

    if request.method == "POST":

        entered_otp = request.POST.get("otp")
        saved_otp = request.session.get("reset_otp")

        print("Entered OTP:", entered_otp)
        print("Saved OTP:", saved_otp)

        if str(entered_otp).strip() == str(saved_otp).strip():
            print("OTP MATCHED")
            return redirect("reset_password")
        else:
            print("OTP NOT MATCHED")
            messages.error(request, "Invalid OTP")

    return render(request, "auth/verify_otp.html")

def reset_password(request):

    email = request.session.get("reset_email")

    if not email:
        return redirect("forgot_password")

    if request.method == "POST":

        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:

            messages.error(request, "Passwords do not match.")

            return redirect("reset_password")

        user = User.objects.filter(email=email).first()

        if not user:
            messages.error(request, "Email not found.")
            return redirect("forgot_password")

        user.set_password(password)

        user.save()

        # Session cleanup
        request.session.pop("reset_email", None)
        request.session.pop("reset_otp", None)

        messages.success(request, "Password reset successful. Please login.")

        return redirect("login")

    return render(request, "auth/reset_password.html")
from django.contrib.auth.decorators import user_passes_test

def admin_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.is_staff:

            login(request, user)

            return redirect("admin_dashboard")

        return render(
            request,
            "adminpanel/login.html",
            {
                "error": "Invalid Admin Credentials"
            }
        )

    return render(request, "adminpanel/login.html")
@staff_member_required
def customers(request):

    users = User.objects.filter(is_staff=False).order_by("-date_joined")

    return render(
        request,
        "adminpanel/customers.html",
        {
            "users": users
        }
    )
    
    
@staff_member_required
def admin_bookings(request):

    bookings = Booking.objects.all().order_by("-created_at")

    return render(
        request,
        "adminpanel/bookings.html",
        {
            "bookings": bookings
        }
    )

@staff_member_required
def update_booking_status(request, booking_id, status):

    print("Booking ID:", booking_id)
    print("Status Received:", status)

    booking = Booking.objects.get(id=booking_id)

    print("Before Save:", booking.status)

    booking.status = status
    booking.save()

    booking.refresh_from_db()

    print("After Save:", booking.status)

    if status == "Approved":
        send_mail(
            subject="🎉 Your Booking Has Been Approved",
            message=f"""
Hello {booking.full_name},

Your booking has been approved.
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.email],
            fail_silently=False,
        )

    return redirect("admin_bookings")

@staff_member_required
def booking_details(request, booking_id):

    booking = Booking.objects.get(id=booking_id)

    return render(
        request,
        "adminpanel/booking_details.html",
        {
            "booking": booking
        }
    )
    
    
@staff_member_required
def upload_gallery(request, booking_id):

    booking = Booking.objects.get(id=booking_id)

    if request.method == "POST":

        form = GalleryForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            gallery = form.save(commit=False)

            gallery.user = booking.user
            gallery.booking = booking

            gallery.save()

            return redirect("booking_details", booking_id=booking.id)

    else:

        form = GalleryForm()

    return render(
        request,
        "adminpanel/upload_gallery.html",
        {
            "booking": booking,
            "form": form
        }
    )
    
    
from django.db.models import Count

@staff_member_required
def gallery_manager(request):

    users = User.objects.filter(is_staff=False)

    photos = Gallery.objects.select_related("user").order_by("-uploaded_at")

    albums = (
        Gallery.objects
        .values("user__username", "album_name")
        .annotate(total=Count("id"))
        .order_by("user__username", "album_name")
    )

    if request.method == "POST":

        user = User.objects.get(id=request.POST["user"])

        album_name = request.POST.get("album_name")

        title = request.POST.get("title")

        images = request.FILES.getlist("images")

        for image in images:

            Gallery.objects.create(
                user=user,
                album_name=album_name,
                title=title,
                image=image
            )

        messages.success(
            request,
            f"{len(images)} photos uploaded successfully."
        )

        return redirect("gallery_manager")

    return render(
        request,
        "adminpanel/gallery_manager.html",
        {
            "users": users,
            "photos": photos,
            "albums": albums,
        }
    
    )
@staff_member_required
def album_photos(request, album_name):

    photos = Gallery.objects.filter(
        album_name=album_name
    ).order_by("-uploaded_at")

    return render(
        request,
        "adminpanel/album_photos.html",
        {
            "photos": photos,
            "album_name": album_name,
        }
    )
@staff_member_required
def delete_photo(request, photo_id):

    photo = get_object_or_404(Gallery, id=photo_id)

    photo.delete()

    messages.success(request, "Photo deleted successfully.")

    return redirect("gallery_manager")

from django.contrib.auth.decorators import login_required
@staff_member_required
def edit_photo(request, photo_id):

    photo = get_object_or_404(Gallery, id=photo_id)

    if request.method == "POST":

        photo.title = request.POST.get("title")

        photo.album_name = request.POST.get("album_name")

        if request.FILES.get("image"):
            photo.image = request.FILES["image"]

        photo.save()

        messages.success(
            request,
            "Photo updated successfully."
        )

        return redirect("gallery_manager")

    return render(
        request,
        "adminpanel/edit_photo.html",
        {
            "photo": photo,
        }
    )

@login_required
def customer_gallery(request):

    photos = Gallery.objects.filter(
        user=request.user
    ).order_by("-uploaded_at")

    return render(
        request,
        "customer/gallery.html",
        {
            "photos": photos,
        }
    )
    
@login_required
def customer_albums(request):

    albums = (
        Gallery.objects
        .filter(user=request.user)
        .values("album_name")
        .distinct()
    )

    return render(
        request,
        "customer/albums.html",
        {
            "albums": albums,
        }
    )
@login_required
def album_gallery(request, album_name):

    photos = Gallery.objects.filter(
        user=request.user,
        album_name=album_name
    )

    return render(
        request,
        "customer/album_gallery.html",
        {
            "photos": photos,
            "album_name": album_name,
        }
    )
@staff_member_required
def video_manager(request):

    users = User.objects.filter(is_staff=False)

    videos = Video.objects.select_related("user").order_by("-uploaded_at")

    if request.method == "POST":

        user = User.objects.get(id=request.POST["user"])

        title = request.POST.get("title")

        video = request.FILES["video"]

        Video.objects.create(
            user=user,
            title=title,
            video=video
        )

        messages.success(
            request,
            "Video uploaded successfully."
        )

        return redirect("video_manager")

    return render(
        request,
        "adminpanel/video_manager.html",
        {
            "users": users,
            "videos": videos,
        }
    )
@staff_member_required
def delete_video(request, video_id):

    video = get_object_or_404(
        Video,
        id=video_id
    )

    video.delete()

    messages.success(
        request,
        "Video deleted successfully."
    )

    return redirect("video_manager")
@staff_member_required
def edit_video(request, video_id):

    video = get_object_or_404(Video, id=video_id)

    if request.method == "POST":

        video.title = request.POST.get("title")

        if request.FILES.get("video"):
            video.video = request.FILES["video"]

        video.save()

        messages.success(
            request,
            "Video updated successfully."
        )

        return redirect("video_manager")

    return render(
        request,
        "adminpanel/edit_video.html",
        {
            "video": video,
        }
    )
    
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings

def test_mail(request):
    try:
        result = send_mail(
            "Prem Studio Test",
            "Hello from Prem Studio",
            settings.DEFAULT_FROM_EMAIL,
            ["akashyaswaroop@gmail.com"],   # Nee Gmail
            fail_silently=False,
        )
        return HttpResponse(f"Mail Sent. Result = {result}")

    except Exception as e:
        return HttpResponse(f"Error: {e}")
    
def gallery(request):
    photos = Gallery.objects.all().order_by("-uploaded_at")

    return render(
        request,
        "gallery.html",
        {
            "photos": photos
        }
    )
    
from django.contrib.auth.decorators import login_required
from .models import Booking

@login_required
def my_bookings(request):

    bookings = Booking.objects.filter(
        user=request.user
    ).order_by("-event_date")

    return render(
    request,
    "customer/bookings.html",
    {
        "bookings": bookings
    }
)    
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User

@staff_member_required
def customers(request):

    users = User.objects.filter(
        is_staff=False
    ).order_by("-date_joined")

    return render(
        request,
        "adminpanel/customers.html",
        {
            "users": users
        }
    )