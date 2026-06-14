from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError  
from django.utils.html import format_html
from cloudinary.models import CloudinaryField


class About(models.Model):
    title = models.CharField(null=True, max_length=100)
    principal_heading = models.CharField(max_length=100)
    principal_content = models.TextField()
    principal_image = models.ImageField(upload_to='about_images/', blank=True, null=True)
    our_story_heading = models.CharField(max_length=100)
    our_story_content = models.TextField()
    about_school_heading = models.CharField(max_length=100)
    about_school_content = models.TextField()

    def __str__(self):
        return self.title


class Banner(models.Model):
    title = models.CharField(max_length=100)
    alt_text = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to='banner_images/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
    )
    add_date = models.DateTimeField(auto_now_add=True, null=True)

    def image_tag(self):
        if self.image:
            return format_html('<img src="{}" style="width:100px;border-radius:4px;" />', self.image.url)
        return "-"
    image_tag.short_description = "Preview"

    def __str__(self):
        return self.title




# ← fixed: removed dots from extensions, fixed ValidationError import
def validate_file_extension(value):
    valid_extensions = ['jpg', 'jpeg', 'png', 'mp4']
    extension = str(value.name).lower().split('.')[-1]
    if extension not in valid_extensions:
        raise ValidationError("Unsupported file extension. Only JPG, PNG, and MP4 files are allowed.")


class GalleryItem(models.Model):
    category = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(
        upload_to='gallery/photos/',
        null=True,
        blank=True,
        validators=[validate_file_extension],
    )
    # ← replace FileField with CloudinaryField for video
    video = CloudinaryField(
        'video',
        resource_type='video',
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.category} - {self.subtitle}"
    

# Newsletter section
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Newsletter Subscriber'
        verbose_name_plural = 'Newsletter Subscribers'

# New&Update section :)
class NewsUpdate(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date', '-id']


# Fee-Structure section
class FeeStructure(models.Model):
    CLASS_CHOICES = [
        ('Nursery', 'Nursery'),
        ('LKG', 'LKG'),
        ('UKG', 'UKG'),
        ('Class I', 'Class I'),
        ('Class II', 'Class II'),
        ('Class III', 'Class III'),
        ('Class IV', 'Class IV'),
        ('Class V', 'Class V'),
        ('Class VI', 'Class VI'),
        ('Class VII', 'Class VII'),
        ('Class VIII', 'Class VIII'),
        ('Class IX', 'Class IX'),
        ('Class X', 'Class X'),
        ('Class XI', 'Class XI'),
        ('Class XII', 'Class XII'),
    ]

    class_name = models.CharField(max_length=50, choices=CLASS_CHOICES)
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    admission_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    exam_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sports_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    miscellaneous_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    session_year = models.CharField(max_length=20, default='2025-26')
    is_active = models.BooleanField(default=True)

    def total_fee(self):
        return self.tuition_fee + self.admission_fee + self.exam_fee + self.sports_fee + self.miscellaneous_fee

    def __str__(self):
        return f"{self.class_name} - {self.session_year}"

    class Meta:
        ordering = ['class_name']
        verbose_name = 'Fee Structure'
        verbose_name_plural = 'Fee Structures'