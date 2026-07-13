from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import migrations


def create_demo_accounts(apps, schema_editor):
    User = apps.get_model(*settings.AUTH_USER_MODEL.split('.'))
    Account = apps.get_model('projekti', 'Account')

    demo_users = [
        ('demo1', 'demo1pass', '1000.00'),
        ('demo2', 'demo2pass', '500.00'),
        ('demo3', 'demo3pass', '400.00'),
    ]

    for username, password, balance in demo_users:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'password': make_password(password),
                'is_staff': False,
                'is_superuser': False,
                'email': '',
            },
        )

        if created:
            Account.objects.create(user=user, balance=balance)
        else:
            Account.objects.get_or_create(user=user, defaults={'balance': balance})


def reverse_create_demo_accounts(apps, schema_editor):
    User = apps.get_model(*settings.AUTH_USER_MODEL.split('.'))
    User.objects.filter(username__in=['demo1', 'demo2']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('projekti', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_demo_accounts, reverse_create_demo_accounts),
    ]
