from django.db import models


class LogicDeleteManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_delete=False)


class NoDeleteModel(models.Model):
    is_delete = models.BooleanField(default=False)
    objects = LogicDeleteManager()

    class Meta:
        abstract = True


class Education(NoDeleteModel):
    name = models.CharField(max_length=32, null=False)


class Departments(NoDeleteModel):
    name = models.CharField(max_length=32, null=False)


class Employees(NoDeleteModel):
    name = models.CharField(max_length=32, null=False)
    card_id = models.CharField(max_length=32, unique=True, null=False)
    male = models.BooleanField(null=False)
    birth = models.DateField(null=False, default='2020-01-01')
    education = models.ForeignKey(Education)
    telephone = models.CharField(max_length=16, null=False)
    address = models.CharField(max_length=256)


# many to many relation ? how ?
class Managers(NoDeleteModel):
    emp = models.ForeignKey(Employees)
    department = models.ForeignKey(Departments)


class Salesmen(NoDeleteModel):
    emp = models.ForeignKey(Employees)


class Subjects(NoDeleteModel):
    name = models.CharField(max_length=32, null=False)


class Teachers(NoDeleteModel):
    emp = models.ForeignKey(Employees)
    subject = models.ForeignKey(Subjects)


class Guests(models.Model):
    username = models.CharField(max_length=32, null=False)
    password = models.CharField(max_length=128, null=False)
    datetime = models.DateTimeField()
    star_teacher = models.ManyToManyField(Teachers)

