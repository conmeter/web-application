from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator
from django.utils import timezone
from users.models import User
import random
import uuid

def validate_image(image):
    file_size = image.file.size
    limit_kb = 5120  # 5MB
    if file_size > limit_kb * 1024:
        raise ValidationError("Max size of file is %s MB" % limit_kb)

def get_image_filename(instance, filename):
    return os.path.join('post_images', str(instance.id)+filename)



class Posts(models.Model):
    post_id = models.AutoField(primary_key=True)
    web_url = models.ForeignKey("webs.Webs", on_delete=models.CASCADE, validators=[URLValidator],
                                verbose_name="Enter the URL of the website")
    user_email = models.ForeignKey("users.User", on_delete=models.CASCADE)
    review_text = models.TextField(help_text="Describe how you felt about the website", null=True, blank=True,
                                   verbose_name="Feedback")
    date_posted = models.DateTimeField(default=timezone.now)
    design_rating = models.IntegerField(null=False, blank=False,
                                        validators=[MinValueValidator(0), MaxValueValidator(5)],
                                        help_text="How easy was it to navigate the website",
                                        verbose_name="DESIGN RATING")
    ui_rating = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(0), MaxValueValidator(5)],
                                    help_text="How modern looking was the website",
                                    verbose_name="USER INTERFACE RATING")
    speed_rating = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(0), MaxValueValidator(5)],
                                       help_text="How responsive was the website", verbose_name="RESPONSIVENESS RATING")
    qoc_rating = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(0), MaxValueValidator(5)],
                                     help_text="How was the quality of content on the website",
                                     verbose_name="QOC RATING")
    reliability_rating = models.IntegerField(null=False, blank=False,
                                             validators=[MinValueValidator(0), MaxValueValidator(5)],
                                             help_text="Rate the availability of the website",
                                             verbose_name="RELIABILITY RATING")
    compatibility_rating = models.IntegerField(null=False, blank=False,
                                               validators=[MinValueValidator(0), MaxValueValidator(5)],
                                               help_text="How compatible was the website with all your devices",
                                               verbose_name="COMPATABILITY RATING")
    support_rating = models.IntegerField(null=False, blank=False,
                                         validators=[MinValueValidator(0), MaxValueValidator(5)],
                                         help_text="How good was the customer support", verbose_name="SUPPORT RATING")
    trust_rating = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(0), MaxValueValidator(5)],
                                       help_text="How trustworthy is the website", verbose_name="TRUST RATING")
    total_rating_value = models.FloatField(blank=False)
    rating_count = models.IntegerField(default=0)
    user = models.ManyToManyField(User, blank=True, related_name="user_likes")
    image = models.ImageField(verbose_name='Image', upload_to="post_images", null=True, blank=True,
                              validators=[validate_image])

    def calc_total(self):
        x = self.design_rating * 1 + self.ui_rating * 2 + self.speed_rating * 1 + self.qoc_rating * 3 + self.reliability_rating * 2 + self.compatibility_rating * 1 + self.support_rating * 3 + self.trust_rating * 3
        t_r = (x / 80) * 100
        return t_r

    def save(self, *args, **kwargs):
        x = self.calc_total()
        self.total_rating_value = float(x)
        super(Posts, self).save(*args, **kwargs)


class Notifications(models.Model):
    head = models.CharField(max_length = 50, blank = False, null = False, verbose_name = 'NOTIFICATION HEAD')
    body = models.CharField(max_length = 250, blank = False, null = False, verbose_name = 'NOTIFICATION BODY')
    date = models.DateTimeField(default=timezone.now)
