# Generated by Django 4.0.4 on 2022-06-25 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bonus',
            fields=[
                ('id', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=30)),
                ('value', models.CharField(db_column='Value', max_length=9)),
            ],
            options={
                'db_table': 'Bonus',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Bonusspin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, max_digits=4)),
                ('combi', models.CharField(db_column='Combi', max_length=1)),
            ],
            options={
                'db_table': 'BonusSpin',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'Category',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'Club',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=50)),
                ('place', models.CharField(max_length=25)),
                ('date', models.CharField(max_length=25)),
            ],
            options={
                'db_table': 'Competition',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=25)),
            ],
            options={
                'db_table': 'Component',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'Element',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judges', models.DecimalField(decimal_places=0, max_digits=1)),
            ],
            options={
                'db_table': 'Event',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Eventskater',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.DecimalField(blank=True, decimal_places=0, max_digits=2, null=True)),
                ('et', models.DecimalField(decimal_places=2, max_digits=5)),
                ('ia', models.DecimalField(decimal_places=2, max_digits=5)),
                ('deduction', models.DecimalField(decimal_places=2, max_digits=5)),
                ('total', models.DecimalField(decimal_places=2, max_digits=5)),
                ('place', models.DecimalField(decimal_places=0, max_digits=2)),
            ],
            options={
                'db_table': 'EventSkater',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=50)),
                ('factor', models.DecimalField(decimal_places=1, max_digits=3)),
                ('judges', models.DecimalField(decimal_places=0, max_digits=1)),
            ],
            options={
                'db_table': 'Level',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Levelcomponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'LevelComponent',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'Program',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=50)),
                ('base', models.DecimalField(decimal_places=2, max_digits=5)),
                ('bonus', models.DecimalField(decimal_places=2, max_digits=5)),
                ('tech', models.DecimalField(decimal_places=2, max_digits=4)),
                ('qoe', models.DecimalField(decimal_places=2, max_digits=4)),
                ('j1', models.CharField(max_length=2)),
                ('j2', models.CharField(max_length=2)),
                ('j3', models.CharField(max_length=2)),
                ('total', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
            options={
                'db_table': 'Score',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Scoreia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('j1', models.DecimalField(decimal_places=2, max_digits=4)),
                ('j2', models.DecimalField(decimal_places=2, max_digits=4)),
                ('j3', models.DecimalField(decimal_places=2, max_digits=4)),
                ('total', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
            options={
                'db_table': 'ScoreIA',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Skater',
            fields=[
                ('id', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('music', models.FileField(upload_to='music/')),
            ],
            options={
                'db_table': 'Skater',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Territorial',
            fields=[
                ('id', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'Territorial',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'Type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p3', models.DecimalField(decimal_places=2, max_digits=4)),
                ('p2', models.DecimalField(decimal_places=2, max_digits=4)),
                ('p1', models.DecimalField(decimal_places=2, max_digits=4)),
                ('base', models.DecimalField(decimal_places=2, max_digits=4)),
                ('n1', models.DecimalField(decimal_places=2, max_digits=4)),
                ('n2', models.DecimalField(decimal_places=2, max_digits=4)),
                ('n3', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
            options={
                'db_table': 'Value',
                'managed': False,
            },
        ),
    ]
