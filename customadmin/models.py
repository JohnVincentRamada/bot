from django.db import models
from customadmin.services.pinecone_service import upsert_data_in_pinecone

class Description(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    answer = models.CharField(max_length=100000)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        upsert_data_in_pinecone(self)
    def __str__(self):
        return self.title