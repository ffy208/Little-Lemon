from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_groups(sender, **kwargs):
    if sender.name == "restaurant":  # 确保只运行在 restaurant app
        Group.objects.get_or_create(name='Manager')
        Group.objects.get_or_create(name='Delivery Crew')
