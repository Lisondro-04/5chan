from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField


# MODELOS

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reviewer.username} - {self.blog.title}"

    def clean(self):
        # Validar que el comentario tenga al menos 10 caracteres
        if len(self.comment.strip()) < 10:
            raise ValidationError("El comentario debe tener al menos 10 caracteres.")
        
        # Validar que el usuario no deje más de una review por blog
        if Review.objects.filter(blog=self.blog, reviewer=self.reviewer).exclude(pk=self.pk).exists():
            raise ValidationError("Ya has dejado una reseña para este blog.")

        # Validar lenguaje inapropiado
        if "ofensivo" in self.comment.lower():
            raise ValidationError("Tu comentario contiene lenguaje inapropiado.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Aplica validaciones antes de guardar
        super().save(*args, **kwargs)


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.commenter.username}"
