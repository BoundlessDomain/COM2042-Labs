import data_wizard
from .models import Project, Board, List, Task, Label

# Register all of our models with the wizard
data_wizard.register(Project)
data_wizard.register(Board)
data_wizard.register(List)
data_wizard.register(Task)
data_wizard.register(Label)