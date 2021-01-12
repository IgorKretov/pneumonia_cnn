from django.db import models


class Task(models.Model):
    name = models.CharField(max_length=50)
    info = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE
    )
    original_name = models.CharField(max_length=255)
    info = models.CharField(max_length=255)
    saved_name = models.CharField(max_length=255)
    saved_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.saved_name