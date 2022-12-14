# Generated by Django 4.0.5 on 2022-10-09 02:12

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0024_alter_complainttype_creation_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complainttype',
            name='creation_date',
            field=models.DateField(default=datetime.datetime(2022, 10, 9, 2, 12, 34, 149908, tzinfo=utc), verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='complainttype',
            name='updation_date',
            field=models.DateField(default=datetime.datetime(2022, 10, 9, 2, 12, 34, 149908, tzinfo=utc), verbose_name='Last Updated'),
        ),
        migrations.AlterField(
            model_name='tblecomplaint',
            name='complainant',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tblecomplaint',
            name='complaintStatus',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, related_name='status', to='users.complaintstatus'),
        ),
        migrations.AlterField(
            model_name='tblecomplaint',
            name='complaint_file',
            field=models.FileField(upload_to='media', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'doc', 'png', 'jpg', 'jpeg', 'mp4', 'mkv', 'mp3', 'ppt'])], verbose_name='Complaint Files'),
        ),
        migrations.AlterField(
            model_name='tblecomplaint',
            name='complaint_regDate',
            field=models.DateField(default=datetime.datetime(2022, 10, 9, 2, 12, 34, 149908, tzinfo=utc), verbose_name='Complaint Submitted Date'),
        ),
        migrations.AlterField(
            model_name='tblecomplaint',
            name='complaint_remark',
            field=models.CharField(default=True, max_length=1000, verbose_name='remark'),
        ),
    ]
