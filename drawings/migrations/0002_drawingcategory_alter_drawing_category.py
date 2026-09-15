from django.db import migrations, models
import django.db.models.deletion


def migrate_categories(apps, schema_editor):
    Drawing = apps.get_model('drawings', 'Drawing')
    DrawingCategory = apps.get_model('drawings', 'DrawingCategory')

    drawings = Drawing.objects.all()

    for drawing in drawings:
        category_name = drawing.category

        if category_name:
            category, created = DrawingCategory.objects.get_or_create(
                name=category_name
            )

            drawing.category_new_id = category.id
            drawing.save(update_fields=['category_new'])


class Migration(migrations.Migration):

    dependencies = [
        ('drawings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DrawingCategory',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'name',
                    models.CharField(
                        max_length=100,
                        unique=True
                    )
                ),
                (
                    'description',
                    models.TextField(
                        blank=True
                    )
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True
                    )
                ),
            ],
        ),

        migrations.AddField(
            model_name='drawing',
            name='category_new',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='drawings_new',
                to='drawings.drawingcategory',
            ),
        ),

        migrations.RunPython(
            migrate_categories,
            migrations.RunPython.noop
        ),

        migrations.RemoveField(
            model_name='drawing',
            name='category',
        ),

        migrations.RenameField(
            model_name='drawing',
            old_name='category_new',
            new_name='category',
        ),

        migrations.AlterField(
            model_name='drawing',
            name='category',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='drawings',
                to='drawings.drawingcategory',
            ),
        ),
    ]