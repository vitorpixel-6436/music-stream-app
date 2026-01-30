"""Management command for quickly creating or promoting admin users

Usage:
    python manage.py addadmin <email> [--username USERNAME] [--superuser]
    
Examples:
    python manage.py addadmin admin@example.com --superuser
    python manage.py addadmin user@example.com --username johndoe
"""

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.db import IntegrityError
from getpass import getpass


class Command(BaseCommand):
    help = 'Быстрое создание или назначение администратора'

    def add_arguments(self, parser):
        parser.add_argument(
            'email',
            type=str,
            help='Email пользователя'
        )
        parser.add_argument(
            '--username',
            type=str,
            help='Username (опционально, по умолчанию из email)'
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Пароль (опционально, будет запрошен интерактивно)'
        )
        parser.add_argument(
            '--superuser',
            action='store_true',
            help='Создать суперпользователя с полными правами'
        )

    def handle(self, *args, **options):
        email = options['email']
        username = options.get('username') or email.split('@')[0]
        password = options.get('password')
        is_superuser = options.get('superuser', False)

        self.stdout.write(
            self.style.HTTP_INFO('\n' + '='*60)
        )
        self.stdout.write(
            self.style.HTTP_INFO('🎵 Music Stream App - Admin Management')
        )
        self.stdout.write(
            self.style.HTTP_INFO('='*60 + '\n')
        )

        # Check if user exists
        try:
            user = User.objects.get(email=email)
            self.stdout.write(
                self.style.WARNING(
                    f'⚠️  Пользователь с email {email} уже существует'
                )
            )
            
            # Update permissions
            if is_superuser:
                user.is_staff = True
                user.is_superuser = True
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Пользователь {username} назначен суперадминистратором'
                    )
                )
            else:
                user.is_staff = True
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Пользователю {username} выданы права администратора'
                    )
                )
            
            self._print_user_info(user)
                
        except User.DoesNotExist:
            # Create new user
            self.stdout.write(
                self.style.HTTP_INFO(
                    f'📝 Создание нового пользователя: {username}'
                )
            )
            
            if not password:
                password = getpass('🔐 Введите пароль: ')
                password_confirm = getpass('🔐 Подтвердите пароль: ')
                
                if password != password_confirm:
                    raise CommandError(
                        self.style.ERROR('❌ Пароли не совпадают')
                    )
                
                if len(password) < 8:
                    raise CommandError(
                        self.style.ERROR(
                            '❌ Пароль должен содержать минимум 8 символов'
                        )
                    )
            
            try:
                if is_superuser:
                    user = User.objects.create_superuser(
                        username=username,
                        email=email,
                        password=password
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✅ Суперпользователь {username} создан успешно'
                        )
                    )
                else:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password
                    )
                    user.is_staff = True
                    user.save()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✅ Администратор {username} создан успешно'
                        )
                    )
                
                self._print_user_info(user)
                    
            except IntegrityError as e:
                raise CommandError(
                    self.style.ERROR(f'❌ Ошибка создания пользователя: {e}')
                )
        
        self.stdout.write(
            self.style.HTTP_INFO('\n' + '='*60 + '\n')
        )
    
    def _print_user_info(self, user):
        """Print user information summary"""
        self.stdout.write('\n' + self.style.HTTP_INFO('📋 Данные для входа:'))
        self.stdout.write(f'   Username: {self.style.SUCCESS(user.username)}')
        self.stdout.write(f'   Email: {self.style.SUCCESS(user.email)}')
        self.stdout.write(
            f'   Is Staff: {self.style.SUCCESS("Yes" if user.is_staff else "No")}'
        )
        self.stdout.write(
            f'   Is Superuser: {self.style.SUCCESS("Yes" if user.is_superuser else "No")}'
        )
        self.stdout.write(f'\n   Admin URL: {self.style.HTTP_INFO("http://localhost:8000/admin/")}')
