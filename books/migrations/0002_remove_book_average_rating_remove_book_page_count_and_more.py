# Generated by Django 5.1.6 on 2025-03-09 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='average_rating',
        ),
        migrations.RemoveField(
            model_name='book',
            name='page_count',
        ),
        migrations.RemoveField(
            model_name='book',
            name='preview_link',
        ),
        migrations.RemoveField(
            model_name='book',
            name='ratings_count',
        ),
        migrations.AddField(
            model_name='book',
            name='currency',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='authors',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='categories',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='published_date',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=500),
        ),
    ]
