from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError  
from django.utils.html import format_html
from cloudinary.models import CloudinaryField
import random
import string
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

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
    
    COURSE_CHOICES = [
        ('', 'N/A'),
        ('Science', 'Science'),
        ('Commerce', 'Commerce'),
        ('Arts', 'Arts'),
    ]

    class_name = models.CharField(max_length=50, choices=CLASS_CHOICES)
    # only for class XI and XII, for other classes it will be blank
    course = models.CharField(max_length=20, choices=COURSE_CHOICES, blank=True, default ='')
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
        if self.course:
              return f"{self.class_name} ({self.course}) - {self.session_year}"
        return f"{self.class_name} - {self.session_year}"

    class Meta:
        ordering = ['class_name']
        verbose_name = 'Fee Structure'
        verbose_name_plural = 'Fee Structures'
        unique_together = ['class_name', 'course', 'session_year']
        

# Otp generation
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

# generate random passwords
def generate_random_password(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

class OTPVerification(models.Model):
    PURPOSE_CHOICES = [
        ('email', 'Email Verification'),
        ('phone', 'Phone Verification'),
    ]

    # Not tied to a User yet, verification happens before account creation
    identifier = models.CharField(max_length=255)  # email address or phone number
    purpose = models.CharField(max_length=10, choices=PURPOSE_CHOICES)
    otp_code = models.CharField(max_length=6, default=generate_otp)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    attempts = models.IntegerField(default=0)  # guards against brute-force guessing

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.identifier} - {self.purpose} - {'verified' if self.is_verified else 'pending'}"

    class Meta:
        verbose_name = 'OTP Verification'
        verbose_name_plural = 'OTP Verifications'

class StudentApplication(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending_verification', 'Pending Verification'),
        ('pending_payment', 'Pending Payment'),
        ('payment_failed', 'Payment Failed'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
    ]
    PASSWORD_CHOICE = [
        ('auto', 'Auto-Generate Password'),
        ('custom', 'Custom Password'),
    ]
    password_choice = models.CharField(max_length=10, choices=PASSWORD_CHOICE, default='auto')

    last_reminder_sent = models.DateTimeField(null=True, blank=True)
    reminder_count = models.IntegerField(default=0)

    # Linked once the account is created (after successful payment)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='student_profile')

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=150)
    mother_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    applying_class = models.CharField(max_length=50)   # mirrors FeeStructure.CLASS_CHOICES
    course = models.CharField(max_length=20, blank=True, default='')  # only for XI/XII

    fee_structure = models.ForeignKey('FeeStructure', on_delete=models.SET_NULL, null=True, blank=True)

    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)

    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='pending_verification')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name()} - {self.applying_class} ({self.status})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Student Application'
        verbose_name_plural = 'Student Applications'

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('created', 'Order Created'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    application = models.ForeignKey(StudentApplication, on_delete=models.CASCADE, related_name='transactions')
    razorpay_order_id = models.CharField(max_length=100)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='INR')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.application.full_name()} - ₹{self.amount} - {self.status}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'