# Generated by Django 5.0.6 on 2024-05-31 15:07

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('AG', 'An Giang'), ('BR', 'Bà Rịa - Vũng Tàu'), ('BG', 'Bắc Giang'), ('BK', 'Bắc Kạn'), ('BL', 'Bạc Liêu'), ('BN', 'Bắc Ninh'), ('BT', 'Bến Tre'), ('BD', 'Bình Định'), ('BĐ', 'Bình Dương'), ('BP', 'Bình Phước'), ('BT', 'Bình Thuận'), ('CM', 'Cà Mau'), ('CT', 'Cần Thơ'), ('CB', 'Cao Bằng'), ('DN', 'Đà Nẵng'), ('DL', 'Đắk Lắk'), ('DK', 'Đắk Nông'), ('DB', 'Điện Biên'), ('ĐN', 'Đồng Nai'), ('ĐT', 'Đồng Tháp'), ('GL', 'Gia Lai'), ('HG', 'Hà Giang'), ('HN', 'Hà Nội'), ('HT', 'Hà Tĩnh'), ('HD', 'Hải Dương'), ('HP', 'Hải Phòng'), ('HM', 'Hậu Giang'), ('HB', 'Hòa Bình'), ('HY', 'Hưng Yên'), ('KH', 'Khánh Hòa'), ('KG', 'Kiên Giang'), ('KT', 'Kon Tum'), ('LC', 'Lai Châu'), ('LD', 'Lâm Đồng'), ('LS', 'Lạng Sơn'), ('LC', 'Lào Cai'), ('LA', 'Long An'), ('ND', 'Nam Định'), ('NA', 'Nghệ An'), ('NB', 'Ninh Bình'), ('NT', 'Ninh Thuận'), ('PT', 'Phú Thọ'), ('PY', 'Phú Yên'), ('QB', 'Quảng Bình'), ('QNam', 'Quảng Nam'), ('QN', 'Quảng Ngãi'), ('QNI', 'Quảng Ninh'), ('QT', 'Quảng Trị'), ('ST', 'Sóc Trăng'), ('SL', 'Sơn La'), ('TNI', 'Tây Ninh'), ('TB', 'Thái Bình'), ('TN', 'Thái Nguyên'), ('TH', 'Thanh Hóa'), ('TTH', 'Thừa Thiên Huế'), ('TG', 'Tiền Giang'), ('TV', 'Trà Vinh'), ('TQ', 'Tuyên Quang'), ('VL', 'Vĩnh Long'), ('VP', 'Vĩnh Phúc'), ('YB', 'Yên Bái'), ('HCM', 'Hồ Chí Minh')], default='HCM', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_employer', models.BooleanField(default=False)),
                ('is_candidate', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatar_candidate/')),
                ('phone', models.CharField(max_length=20)),
                ('cv', models.FileField(blank=True, null=True, upload_to='cv/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('full_name', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatar_employer/')),
                ('phone', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('position', models.CharField(blank=True, choices=[('NV', 'Nhân viên'), ('TN', 'Trưởng nhóm'), ('PP', 'Phó phòng'), ('TP', 'Trưởng phòng'), ('PGD', 'Phó giám đốc'), ('GD', 'Giám đốc'), ('TGD', 'Tổng giám đốc')], default='NV', max_length=3, null=True)),
                ('full_name', models.CharField(blank=True, max_length=255, null=True)),
                ('gender', models.BooleanField(default=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.company')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('work_location', models.ManyToManyField(blank=True, default='HCM', null=True, related_name='work_location', to='users.location')),
            ],
        ),
    ]
