from django.db import models
# Imports the slug function. A slug is a string which typically contains only letters, numbers, underscores, or hyphens, making it safe to use in a URL path.
from django.utils.text import slugify
from django.core.validators import RegexValidator

# Create your models here.
class Project(models.Model): # We inherit from the "models.Model" base class to create a Django model.
    """
    Represents a project, which is the top-level container for boards, lists, tasks, and labels.
    """
    title = models.CharField(max_length=64, unique=True, blank=False, null=False)
    description = models.CharField(max_length=256, blank=True)
    image = models.ImageField(upload_to='media', blank=True) # Stores the image file.
    slug = models.SlugField(unique=True, blank=True) # Label, usually used for generating URLs.

    # Overrides the default Django save method to check if a slug already exists. If not, it generates one from the "title".
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns a string representation of the project, which is its title.
        This is useful for the Django admin site.
        """
        return self.title



class Board(models.Model):
    """
    A board within a project, used to organise teams or sprints.
    """
    # The "ForeignKey" creates a many-to-one relationship. Links each "Board" and "Label" to a single "Project".
    # "on_delete=models.CASCADE" makes sure that if a "Project" is deleted, all associated "Board"s and "Label"s are also deleted.
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='boards')
    title = models.CharField(max_length=64)

    class Meta:
        # Makes sure that a board's title is unique within the that project.
        # Just having "unique=True" on the "Title" wouldn't work since that would stop two different projects having the same board name.
        constraints = [
            models.UniqueConstraint(fields=['project', 'title'], name='unique_board_title_per_project')
        ]

    def __str__(self):
        return f"{self.project.title} - {self.title}"



class Label(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='labels')
    title = models.CharField(max_length=32)
    color = models.CharField(
        max_length=7,
        validators=[
            # Makes sure that the colour input is a valid hex code.
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6})$',
                message='Color must be a valid hex code (e.g., #AABBCC).'
            )
        ]
    )

    class Meta:
        # Makes sure that a label's title is unique within the scope of its project.
        constraints = [
            models.UniqueConstraint(fields=['project', 'title'], name='unique_label_title_per_project')
        ]

    def __str__(self):
        return self.title