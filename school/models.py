from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    STUDENT = 'student'
    INSTRUCTOR = 'instructor'
    SECRETARY = 'secretary'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (STUDENT,'Student'),
        (INSTRUCTOR,'instructor'),
        (SECRETARY,'Secretary'),
        (ADMIN,'Admin'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def is_student(self):
        return self.role == self.STUDENT
    def is_instructor(self):
        return self.role == self.INSTRUCTOR
    def is_secretary(self):
        return self.role == self.SECRETARY
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def total_hours_remaining(self):
        return sum(p.hours_remaining for p in self.package_set.all())

class Package(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    hours_total = models.IntegerField()
    hours_used = models.IntegerField(default=0)
    @property
    def hours_remaining(self):
        return self.hours_total - self.hours_used

class Lesson(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons_as_student')
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons_as_instructor')
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    duration = models.IntegerField(default=1)

    def _deduct_hours(self, hours):
        packages = Package.objects.filter(student=self.student).order_by('id')
        hours_to_deduct = hours
        for package in packages:
            if hours_to_deduct <= 0:
                break
            if package.hours_remaining >= hours_to_deduct:
                package.hours_used += hours_to_deduct
                package.save()
                hours_to_deduct = 0
            else:
                hours_to_deduct -= package.hours_remaining
                package.hours_used = package.hours_total
                package.save()

    def _refund_hours(self, hours):
        packages = Package.objects.filter(student=self.student).order_by('id')
        hours_to_refund = hours
        for package in packages:
            if hours_to_refund <= 0:
                break
            refund = min(package.hours_used, hours_to_refund)
            package.hours_used -= refund
            package.save()
            hours_to_refund -= refund

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new:
            packages = Package.objects.filter(student=self.student)
            total_remaining = sum(p.hours_remaining for p in packages)
            if total_remaining < self.duration:
                raise ValidationError("L'étudiant n'a pas assez d'heures disponibles.")
            super().save(*args, **kwargs)
            self._deduct_hours(self.duration)
        else:
            old = Lesson.objects.get(pk=self.pk)
            diff = self.duration - old.duration
            if diff > 0:
                packages = Package.objects.filter(student=self.student)
                total_remaining = sum(p.hours_remaining for p in packages)
                if total_remaining < diff:
                    raise ValidationError("L'étudiant n'a pas assez d'heures disponibles.")
            super().save(*args, **kwargs)
            if diff > 0:
                self._deduct_hours(diff)
            elif diff < 0:
                self._refund_hours(-diff)

    def delete(self, *args, **kwargs):
        self._refund_hours(self.duration)
        super().delete(*args, **kwargs)

class SchoolSettings(models.Model):
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2, default=20.00)

    class Meta:
        verbose_name = 'School Settings'

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

class LessonRequest(models.Model):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REFUSED = 'refused'
    STATUS_CHOICE = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REFUSED, 'Refused')
    ]

    STUDENT = 'student'
    INSTRUCTOR = 'instructor'
    PROPOSED_BY_CHOICES = [
        (STUDENT, 'Student'),
        (INSTRUCTOR, 'Instructor')
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_request_as_student')
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_request_as_instructor')
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    duration = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default=PENDING)
    proposed_by = models.CharField(max_length=20, choices=PROPOSED_BY_CHOICES, default=STUDENT)


    def is_pending(self):
        return self.status == self.PENDING
    def is_accepted(self):
        return self.status == self.ACCEPTED
    def is_refused(self):
        return self.status == self.REFUSED

