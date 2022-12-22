from django.db import models
from django.contrib.auth import get_user_model


class Task(models.Model):
    STATUS_VARIABLES = [
        ('To do', 'To do'),
        ('In progress', 'In progress'),
        ('Code review', 'Code review'),
        ('Done', 'Done')
    ]
    name = models.CharField(max_length=100, verbose_name='Name')
    description = models.TextField(max_length=300, verbose_name='Description')

    status = models.CharField(max_length=100, choices=STATUS_VARIABLES,
                              default='To do', verbose_name='Status')
    priority = models.IntegerField(verbose_name='Priority')

    executor = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True,
        blank=True, related_name='user_task_executor', verbose_name='Executor')

    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True,
                                related_name='user_task_creator', verbose_name='Creator')
    project = models.ForeignKey('Project', on_delete=models.CASCADE,
        related_name='project_task', verbose_name='Project')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created_at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Update_at')

    def __str__(self):
        return f'id: {self.id} | name: {self.name} | ' \
               f'creator: {self.creator.first_name} {self.creator.surname[0]}'

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['-updated_at']


class Project(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    prefix = models.SlugField(max_length=50, unique=True, blank=True, verbose_name='Prefix')
    description = models.TextField(max_length=300, verbose_name='Description')

    lead = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             related_name='user_project_lead')
    team = models.ForeignKey('Users.Team', on_delete=models.SET_NULL, null = True,
        blank=True, verbose_name='Team')

    done = models.BooleanField(default=False, verbose_name='Done')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created_at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Update_at')

    def __str__(self):
        return f'id: {self.id} | name: {self.name} | ' \
               f'lead: {self.lead.first_name} {self.lead.surname[0]}'

    def save(self, *args, **kwargs):
        if len(self.name.split()) > 1:
            self.prefix = self.name.title().replace(' ', '')
        else:
            self.prefix = self.name

        return super(Project, self).save(args, kwargs)

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['-created_at']