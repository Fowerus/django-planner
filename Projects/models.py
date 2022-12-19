from django.db import models
from django.contrib.auth import get_user_model



class Task(models.Model):
    STATUS_VARIABLES = [
        (0, 'To do'),
        (1, 'In progress'),
        (2, 'Code review'),
        (3, 'Done')
    ]
    name = models.CharField(max_length=100, verbose_name='Name')
    description = models.TextField(max_length=300, verbose_name='Description')

    status = models.CharField(max_length=100, choices=STATUS_VARIABLES,
                              default='To do', verbose_name='Status')
    priority = models.IntegerField(verbose_name='Priority')

    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                related_name='user_task_creator', verbose_name='Creator')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created_at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Update_at')

    def __str__(self):
        return f'id: {self.id} | name: {self.name} | ' \
               f'creator: {self.creator.name} {self.creator.surname[0]}'

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['-created_at']


class Project(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    description = models.TextField(max_length=300, verbose_name='Description')

    lead = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             related_name='user_project_lead')
    team = models.ForeignKey('Users.Team', on_delete=models.SET_NULL, null = True, verbose_name='Team')

    done = models.BooleanField(default=False, verbose_name='Done')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created_at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Update_at')

    def __str__(self):
        return f'id: {self.id} | name: {self.name} | ' \
               f'lead: {self.lead.name} {self.lead.surname[0]}'

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['-created_at']