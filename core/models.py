from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Topic(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='topics',
        blank=True,
        null=True,
        help_text="User"
    )
    name = models.CharField(max_length=200)
    summary = models.TextField(help_text="Short summary from Wikipedia")
    user_notes = models.TextField(blank=True, null=True, help_text="Custom user notes")
    mind_map_data = models.JSONField(blank=True, null=True, help_text="Saved mind map nodes and edges")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
