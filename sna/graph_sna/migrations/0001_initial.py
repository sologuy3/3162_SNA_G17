# Generated by Django 2.1 on 2018-09-06 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('subject', models.CharField(max_length=200)),
                ('body', models.TextField()),
                ('time_sent', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email_address', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AddField(
            model_name='email',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='graph_sna.Person'),
        ),
        migrations.AddField(
            model_name='email',
            name='bccs',
            field=models.ManyToManyField(related_name='bccs', to='graph_sna.Person'),
        ),
        migrations.AddField(
            model_name='email',
            name='ccs',
            field=models.ManyToManyField(related_name='ccs', to='graph_sna.Person'),
        ),
        migrations.AddField(
            model_name='email',
            name='recipients',
            field=models.ManyToManyField(related_name='recipients', to='graph_sna.Person'),
        ),
    ]