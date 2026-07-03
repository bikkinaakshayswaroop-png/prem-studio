from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('booking/', views.booking, name='booking'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('videos/', views.customer_videos, name='customer_videos'),
    path('download-album/', views.download_album, name='download_album'),
    path('profile/', views.profile, name='profile'),

    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('booking-events/', views.booking_events, name='booking_events'),

    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),

    # ===== Custom Admin =====

    path(
        'studio-admin/customers/',
        views.customers,
        name='customers'
    ),

    path(
        'studio-admin/bookings/',
        views.admin_bookings,
        name='admin_bookings'
    ),

    path(
        'studio-admin/booking/<int:booking_id>/',
        views.booking_details,
        name='booking_details'
    ),

    # ✅ Upload Gallery route FIRST
    path(
        'studio-admin/booking/<int:booking_id>/upload-gallery/',
        views.upload_gallery,
        name='upload_gallery'
    ),

    # ✅ Status route AFTER Upload Gallery
    path(
        'studio-admin/booking/<int:booking_id>/<str:status>/',
        views.update_booking_status,
        name='update_booking_status'
    ),
    path(
    "studio-admin/gallery/",
    views.gallery_manager,
    name="gallery_manager"
    ),
    path(
    "studio-admin/album/<str:album_name>/",
    views.album_photos,
    name="album_photos"
    ),
    path(
    "studio-admin/gallery/delete/<int:photo_id>/",
    views.delete_photo,
    name="delete_photo"
    ),
    path(
    "customer/gallery/",
    views.customer_gallery,
    name="customer_gallery"
   ),
    path(
    "studio-admin/videos/",
    views.video_manager,
    name="video_manager"
    ),
    path(
    "studio-admin/video/delete/<int:video_id>/",
    views.delete_video,
    name="delete_video"
),
   path(
    "customer/albums/",
    views.customer_albums,
    name="customer_albums"
),

path(
    "customer/album/<str:album_name>/",
    views.album_gallery,
    name="album_gallery"
),
path(
    "studio-admin/gallery/edit/<int:photo_id>/",
    views.edit_photo,
    name="edit_photo"
),
path(
    "studio-admin/video/edit/<int:video_id>/",
    views.edit_video,
    name="edit_video"
),
path(
    "test-mail/",
    views.test_mail,
    name="test_mail"
),
path(
    "gallery/",
    views.gallery,
    name="gallery"
),
path(
    "my-bookings/",
    views.my_bookings,
    name="my_bookings"
),
    
]