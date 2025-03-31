def move_task_to_next_step(task, user):
    current_step = task.current_step
    next_step = task.process.steps.filter(order__gt=current_step.order).order_by('order').first()

    if not next_step:
        raise ValueError("Это последний этап, дальше двигать нельзя!")

    if current_step.requires_approval and not user.has_perm('bpm.approve_step'):
        raise PermissionError("Вы не можете двигать задачу дальше!")

    task.current_step = next_step
    task.save()
    return task
