from django.db import models

class TimeStampedBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Blog(TimeStampedBaseModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey('author.Author', on_delete=models.CASCADE)
    cover_image = models.OneToOneField('CoverImage', related_name='blog_cover_image', null=True, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', related_name='blog_tags')

    class Meta:
        permissions = [     # Add custom permissions
            ("update_title", "Can update the title of the blog"),
            ("update_content", "Can update the content of the blog"),
        ]
    
    def __str__(self):
        return self.title


class CoverImage(models.Model):
    image_link = models.URLField(default='1')


class Tag(TimeStampedBaseModel):
    name = models.CharField(max_length=100, unique=True)
    