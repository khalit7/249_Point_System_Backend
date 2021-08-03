from django.apps import AppConfig
from django.db.models.signals import post_migrate


def initialize_objects(sender, **kwargs):
    from booking.models import DailySchedule, Resource
    all_schedules = DailySchedule.objects.all()
    all_resources = Resource.objects.all()
    if not all_schedules.exists() and not all_resources.exists():  # the tables are empty
        # initialize all resources
        Resource(name="Room1", service='meeting',
                 capacity=7, price_per_hour=500.0).save()
        Resource(name="Room2", service='meeting',
                 capacity=7, price_per_hour=500.0).save()
        Resource(name="Room3", service='meeting',
                 capacity=3, price_per_hour=250.0).save()
        Resource(name="Workplace1", service='workplace',
                 capacity=15, price_per_hour=630.0).save()

        # initialize resources schedules
        all_resources = Resource.objects.all()
        for resource in all_resources:
            for i in range(1, 32):  # 1-31 (days of a month)
                day_i = DailySchedule(
                    resource=resource, date=i, time_table="111111110000000000000111")
                day_i.save()


class BookingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'booking'

    def ready(self):
        post_migrate.connect(initialize_objects, sender=self)
