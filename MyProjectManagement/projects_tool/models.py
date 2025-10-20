from django.db import models
# Imports the slug function. A slug is a string which typically contains only letters, numbers, underscores, or hyphens, making it safe to use in a URL path.
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

def validate_divisible_by_5(value):
    # Checks if the value is divisible by 5.
    if value % 5 != 0:
        raise ValidationError(f'{value} is not divisible by 5.')



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



class List(models.Model):
    """
    Represents a list or column on a board (e.g., 'To Do', 'Doing', 'Done').
    """
    # Every list must belong to a board, so if a board is deleted, all of its lists are also deleted.
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='lists')
    title = models.CharField(max_length=64)
    position = models.PositiveIntegerField() # Makes sure that it only allows values of 0 or greater.

    # Within any single board, each list must have a unique title. (One "To Do" list in each board)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['board', 'title'], name='unique_list_title_per_board')
        ]

    def __str__(self):
        return self.title



class Task(models.Model):
    # A single task or card that exists within a list.
    class Priority(models.TextChoices):
        # First '' like 'HI' is what is stored in the database. Second '' like 'High' is the human-readable name in the forms and admin panel.
        HIGH = 'HI', 'High'
        MEDIUM = 'ME', 'Medium'
        LOW = 'LO', 'Low'

    # "task_no" is the primary key. "primary_key=True" tells Django to use this field as the unique identifier instead of the default "id" field.
    task_no = models.AutoField(primary_key=True)
    # This links each task to a "List". If a list is deleted, all of its tasks are deleted ("CASCADE").
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=512, blank=True, null=True)
    # Priority for new tasks are set as medium as default.
    priority = models.CharField(max_length=2, choices=Priority.choices, default=Priority.MEDIUM)
    story_points = models.IntegerField(
        validators=[
            # Makes sure the number is between 0 and 100.
            MinValueValidator(0),
            MaxValueValidator(100),
            # Custom function for divisible by 5.
            validate_divisible_by_5
        ]
    )
    # This makes a many-to-many relationship. Blank allows a task to be created without any labels.
    labels = models.ManyToManyField(Label, related_name='tasks', blank=True)

    def __str__(self):
        return f"#{self.task_no}: {self.title}"