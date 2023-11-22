from django.db import models
from django.conf import settings

class Log(models.Model):
    bot = models.CharField(max_length=2000)
    question = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
      settings.AUTH_USER_MODEL, 
      on_delete=models.CASCADE,
      
    )
    
    class Meta:
        ordering = ('-created_at',)
    def __str__(self):
        return self.question

class RequestContext(models.Model):
    request = models.CharField(max_length=1000)
    comment = models.CharField(max_length=1000)

    PENDING = 'pending'
    APPLIED = 'applied'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPLIED, 'Applied'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING,)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
    def __str__(self):
        return self.request

    @classmethod
    def get_applied_count(cls):
        return cls.objects.filter(status=cls.APPLIED).count()

    @classmethod
    def get_pending_count(cls):
        return cls.objects.filter(status=cls.PENDING).count()

    @classmethod
    def get_total_count(cls):
        return cls.objects.count()