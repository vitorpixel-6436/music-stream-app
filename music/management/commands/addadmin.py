from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.db import IntegrityError


class Command(BaseCommand):
    help = 'Быстрое создание или назначение администратора'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email пользователя')
        parser.add_argument('--username', type=str, help='Username (опционально)')
        parser.add_argument('--password', type=str, help='Пароль (опционально, будет запрошен)')
        parser.add_argument('--superuser', action='store_true', help='Создать суперпользователя')

    def handle(self, *args, **options):
        email = options['email']
        username = options.get('username') or email.split('@')[0]
        password = options.get('password')
        is_superuser = options.get('superuser', False)

        # Проверка существующего пользователя
        try:
            user = User.objects.get(email=email)
            self.stdout.write(self.style.WARNING(f'Пользователь с email {email} уже существует'))
            
            # Обновление прав
            if is_superuser:
                user.is_staff = True
                user.is_superuser = True
                user.save()
                self.stdout.write(self.style.SUCCESS(f'✅ Пользователь {username} назначен суперадминистратором'))
            else:
                user.is_staff = True
                user.save()
                self.stdout.write(self.style.SUCCESS(f'✅ Пользователю {username} выданы права администратора'))
                
        except User.DoesNotExist:
            # Создание нового пользователя
            if not password:
                from getpass import getpass
                password = getpass('Введите пароль: ')
                password_confirm = getpass('Подтвердите пароль: ')
                
                if password != password_confirm:
                    raise CommandError('Пароли не совпадают')
            
            try:
                if is_superuser:
                    user = User.objects.create_superuser(
                        username=username,
                        email=email,
                        password=password
                    )
                    self.stdout.write(self.style.SUCCESS(
                        f'✅ Суперпользователь {username} создан успешно'
                    ))
                else:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password
                    )
                    user.is_staff = True
                    user.save()
                    self.stdout.write(self.style.SUCCESS(
                        f'✅ Администратор {username} создан успешно'
                    ))
                    
                self.stdout.write(self.style.SUCCESS(
                    f'\nДанные для входа:\nUsername: {username}\nEmail: {email}\nAdmin URL: /admin/'
                ))
                
            except IntegrityError as e:
                raise CommandError(f'Ошибка создания пользователя: {e}')
