from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField

# Auditoría
from simple_history.models import HistoricalRecords


# MODELOS
class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    history = HistoricalRecords()  # Auditoría

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name='blogs', blank=True)
    history = HistoricalRecords()  # Auditoría

    def __str__(self):
        return self.title


class Review(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()  # Auditoría

    def __str__(self):
        return f"{self.reviewer.username} - {self.blog.title}"

    def clean(self):
        if len(self.comment.strip()) < 10:
            raise ValidationError("El comentario debe tener al menos 10 caracteres.")
        if Review.objects.filter(blog=self.blog, reviewer=self.reviewer).exclude(pk=self.pk).exists():
            raise ValidationError("Ya has dejado una reseña para este blog.")
        if "ofensivo" in self.comment.lower():
            raise ValidationError("Tu comentario contiene lenguaje inapropiado.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()  # Auditoría

    def __str__(self):
        return f"Comment by {self.commenter.username}"
