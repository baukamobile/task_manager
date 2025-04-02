# test_workflow.py
from users.models import Department, User, Positions
from bpm.models import (Process, ProcessStage, ProcessTemplate, Task,
                             WorkflowStep, WorkflowRule, TaskStageHistory)
from django.utils import timezone
import random


# Создаем тестовые данные
def create_test_data():
    # 1. Создаем отдел
    dept, created = Department.objects.get_or_create(name="Тестовый отдел")

    # 2. Создаем должности
    manager, _ = Positions.objects.get_or_create(name="Менеджер", department=dept)
    specialist, _ = Positions.objects.get_or_create(name="Специалист", department=dept)
    accountant, _ = Positions.objects.get_or_create(name="Бухгалтер", department=dept)

    # 3. Создаем пользователей
    users = []
    for i, position in enumerate([manager, specialist, accountant]):
        user, _ = User.objects.get_or_create(
            username=f"test_user_{i}",
            defaults={
                'first_name': f"Имя_{i}",
                'last_name': f"Фамилия_{i}",
                'email': f"user{i}@example.com",
                'position': position
            }
        )
        users.append(user)

    manager_user, specialist_user, accountant_user = users

    # 4. Создаем процесс
    process = Process.objects.create(
        name="Тестовый процесс закупки",
        description="Процесс согласования закупки оборудования",
        owner=manager_user,
        department=dept
    )

    # 5. Создаем этапы процесса
    stages = []
    for i, name in enumerate(["Заявка", "Согласование", "Бухгалтерия", "Выполнение"]):
        stage = ProcessStage.objects.create(
            process=process,
            name=name,
            order=i + 1,
            is_required=True,
            sla_hours=24
        )
        stages.append(stage)

    # 6. Создаем рабочие шаги
    steps = []
    for i, (name, position, user) in enumerate([
        ("Создание заявки", specialist, specialist_user),
        ("Согласование заявки", manager, manager_user),
        ("Финансовое согласование", accountant, accountant_user),
        ("Исполнение заявки", specialist, specialist_user)
    ]):
        step = WorkflowStep.objects.create(
            process=process,
            name=name,
            order=i + 1,
            requires_approval=(i in [1, 2]),  # Требуют одобрения шаги 1 и 2
            responsible_position=position,
            assigned_to=user
        )
        steps.append(step)

    # 7. Создаем правила перехода
    for i in range(len(steps) - 1):
        WorkflowRule.objects.create(
            process=process,
            from_step=steps[i],
            to_step=steps[i + 1],
            allowed_position=steps[i].responsible_position
        )

    # 8. Создаем тестовую задачу
    task = Task.objects.create(
        process=process,
        current_stage=stages[0],
        title="Закупка компьютера",
        description="Необходимо закупить новый ноутбук для отдела разработки",
        assigned_to=specialist_user,
        created_by=manager_user,
        status="not_started",
        priority="medium",
        due_date=timezone.now() + timezone.timedelta(days=5)
    )

    return process, task, stages, steps, users


# Выполнить тест движения задачи по этапам
def test_workflow(process, task, stages, users):
    print(f"\nНачало тестирования процесса: {process.name}")
    print(f"Задача: {task.title}, текущий этап: {task.current_stage.name}")

    # Перемещаем задачу по всем этапам
    for i in range(1, len(stages)):
        prev_stage = task.current_stage
        task.current_stage = stages[i]
        task.assigned_to = users[min(i, len(users) - 1)]
        task.save()

        # Записываем историю перемещения
        history = TaskStageHistory.objects.create(
            task=task,
            from_stage=prev_stage,
            to_stage=stages[i],
            changed_by=users[0],  # Менеджер всегда меняет
            comments=f"Перемещено на этап {stages[i].name}"
        )

        print(
            f"Этап {i}: Задача перемещена из '{prev_stage.name}' в '{stages[i].name}', назначена: {task.assigned_to.first_name}")

    # Проверяем историю перемещений
    history = TaskStageHistory.objects.filter(task=task).order_by('changed_at')
    print(f"\nИстория перемещений задачи '{task.title}':")
    for entry in history:
        print(
            f"• {entry.changed_at.strftime('%Y-%m-%d %H:%M')} - из '{entry.from_stage}' в '{entry.to_stage}' ({entry.changed_by.first_name})")

    print("\nТестирование завершено успешно!")


# Удалить все тестовые данные
def cleanup_test_data(process):
    # Вызывайте эту функцию, если нужно очистить тестовые данные
    if process:
        process.delete()
    print("Тестовые данные очищены")


# Запускаем тест
if __name__ == "__main__":
    print("=== ТЕСТ СИСТЕМЫ БИЗНЕС-ПРОЦЕССОВ ===")
    process, task, stages, steps, users = create_test_data()
    test_workflow(process, task, stages, users)

    # Раскомментируйте, если нужно удалить тестовые данные
    # cleanup_test_data(process)