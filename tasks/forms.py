from django import forms
from tasks.models import Task,Status,Projects

class ProjectStatusForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ('project_name','description','department','assigned_id','end_date')

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['status_name','user']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['__all__'
            # 'task_name','description','status','start_date','end_date',
            # 'projects','assigned','priority','agreed_with_managers','department'
        ]

