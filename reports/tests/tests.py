from django.test import TestCase
from reports.models import Reports
from django.utils.timezone import now
# Create your tests here.
from users.models import Department



class ResportsTestCase(TestCase):
    def setUp(self):
        self.dep1 = Department.objects.create(department_name='Руководитель Отдела')
        self.dep2 = Department.objects.create(department_name='Руководитель Отдела 2')

        self.report = Reports.objects.create(
            reports_name = 'Ежемесячный отчет',
            start_date = now(),
            end_date=now()
         )
        self.report.department.add(self.dep1,self.dep2)

    def test_reports_creation(self):
        self.assertEqual(self.report.reports_name,'Ежемесячный отчет')
        self.assertTrue(self.report.start_date)
        self.assertTrue(self.report.end_date)
    def test_reports_department_relation(self):
        departmens = self.report.department.all()
        self.assertEqual(departmens.count(),2)
        self.assertIn(self.dep1,departmens)
        self.assertIn(self.dep2,departmens)


#class Reports(models.Model):
    # reports_name = models.CharField(max_length=100)
    # start_date = models.DateTimeField()
    # end_date = models.DateTimeField()
    # department = models.ManyToManyField('users.Department',blank=True)
    # def __str__(self):
    #     return self.reports_name
#
# from users.models import Department
# from .models import Reports
#
# class ReportsTestCase(TestCase):
#     def setUp(self):
#         # Создаём тестовые департаменты
#         self.dep1 = Department.objects.create(name="Отдел разработки")
#         self.dep2 = Department.objects.create(name="Отдел аналитики")
#
#         # Создаём тестовый отчёт
#         self.report = Reports.objects.create(
#             reports_name="Ежемесячный отчёт",
#             start_date=now(),
#             end_date=now()
#         )
#         # Добавляем департаменты в отчёт (ManyToMany)
#         self.report.department.add(self.dep1, self.dep2)
#
#     def test_reports_creation(self):
#         """Проверяет, что отчёт создаётся правильно"""
#         self.assertEqual(self.report.reports_name, "Ежемесячный отчёт")
#         self.assertTrue(self.report.start_date)
#         self.assertTrue(self.report.end_date)
#
#     def test_reports_department_relation(self):
#         """Проверяет, что отчёт связан с департаментами"""
#         departments = self.report.department.all()
#         self.assertEqual(departments.count(), 2)
#         self.assertIn(self.dep1, departments)
#         self.assertIn(self.dep2, departments)