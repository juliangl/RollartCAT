# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Actual(models.Model):
    event = models.ForeignKey('Eventskater', models.DO_NOTHING, db_column='event')

    class Meta:
        managed = False
        db_table = 'Actual'

class Bonus(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    description = models.CharField(max_length=30)
    value = models.CharField(db_column='Value', max_length=9)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Bonus'


class Bonusspin(models.Model):
    spin = models.ForeignKey('Element', models.DO_NOTHING, db_column='spin')
    bonus = models.ForeignKey(Bonus, models.DO_NOTHING, db_column='bonus')
    value = models.DecimalField(max_digits=4, decimal_places=2)
    combi = models.CharField(db_column='Combi', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BonusSpin'


class Category(models.Model):
    id = models.CharField(primary_key=True, max_length=2)
    description = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'Category'


class Club(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=50)
    territorial = models.ForeignKey('Territorial', models.DO_NOTHING, db_column='territorial')

    class Meta:
        managed = False
        db_table = 'Club'


class Competition(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    description = models.CharField(max_length=50)
    place = models.CharField(max_length=25)
    date = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'Competition'


class Component(models.Model):
    id = models.CharField(primary_key=True, max_length=2)
    description = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'Component'


class Element(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    description = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'Element'


class Event(models.Model):
    competition = models.ForeignKey(Competition, models.DO_NOTHING, db_column='competition')
    category = models.ForeignKey(Category, models.DO_NOTHING, db_column='category')
    level = models.ForeignKey('Level', models.DO_NOTHING, db_column='level')
    program = models.ForeignKey('Program', models.DO_NOTHING, db_column='program')
    judges = models.DecimalField(max_digits=1, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'Event'


class Eventskater(models.Model):
    competition = models.ForeignKey(Competition, models.DO_NOTHING, db_column='competition')
    category = models.ForeignKey(Category, models.DO_NOTHING, db_column='category')
    level = models.ForeignKey('Level', models.DO_NOTHING, db_column='level')
    program = models.ForeignKey('Program', models.DO_NOTHING, db_column='program')
    skater = models.ForeignKey('Skater', models.DO_NOTHING, db_column='skater')
    order = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    et = models.DecimalField(max_digits=5, decimal_places=2)
    ia = models.DecimalField(max_digits=5, decimal_places=2)
    deduction = models.DecimalField(max_digits=5, decimal_places=2)
    total = models.DecimalField(max_digits=5, decimal_places=2)
    place = models.DecimalField(max_digits=2, decimal_places=0)


    class Meta:
        managed = False
        db_table = 'EventSkater'


class Level(models.Model):
    id = models.CharField(primary_key=True, max_length=2)
    description = models.CharField(max_length=50)
    factor = models.DecimalField(max_digits=3, decimal_places=1)
    judges = models.DecimalField(max_digits=1, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'Level'


class Levelcomponent(models.Model):
    level = models.ForeignKey(Level, models.DO_NOTHING, db_column='level')
    component = models.ForeignKey(Component, models.DO_NOTHING, db_column='component')

    class Meta:
        managed = False
        db_table = 'LevelComponent'


class Program(models.Model):
    id = models.CharField(primary_key=True, max_length=2)
    description = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'Program'


class Score(models.Model):
    event = models.ForeignKey(Eventskater, models.DO_NOTHING, db_column='event')
    element = models.ForeignKey('Value', models.DO_NOTHING, db_column='element')
    comment = models.CharField(max_length=50)
    base = models.DecimalField(max_digits=5, decimal_places=2)
    bonus = models.DecimalField(max_digits=5, decimal_places=2)
    tech = models.DecimalField(max_digits=4, decimal_places=2)
    qoe = models.DecimalField(max_digits=4, decimal_places=2)
    j1 = models.CharField(max_length=2)
    j2 = models.CharField(max_length=2)
    j3 = models.CharField(max_length=2)
    total = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'Score'


class Scoreia(models.Model):
    event = models.ForeignKey(Eventskater, models.DO_NOTHING, db_column='event')
    component = models.ForeignKey(Levelcomponent, models.DO_NOTHING, db_column='component')
    j1 = models.DecimalField(max_digits=4, decimal_places=2)
    j2 = models.DecimalField(max_digits=4, decimal_places=2)
    j3 = models.DecimalField(max_digits=4, decimal_places=2)
    total = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'ScoreIA'


class Skater(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=50)
    club = models.ForeignKey(Club, models.DO_NOTHING, db_column='club')
    music = models.FileField(upload_to='music/')

    class Meta:
        managed = False
        db_table = 'Skater'


class Territorial(models.Model):
    id = models.CharField(primary_key=True, max_length=2)
    description = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'Territorial'


class Type(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    description = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'Type'


class Value(models.Model):
    type = models.ForeignKey(Type, models.DO_NOTHING, db_column='type', blank=True, null=True)
    element = models.ForeignKey(Element, models.DO_NOTHING, db_column='element')
    p3 = models.DecimalField(max_digits=4, decimal_places=2)
    p2 = models.DecimalField(max_digits=4, decimal_places=2)
    p1 = models.DecimalField(max_digits=4, decimal_places=2)
    base = models.DecimalField(max_digits=4, decimal_places=2)
    n1 = models.DecimalField(max_digits=4, decimal_places=2)
    n2 = models.DecimalField(max_digits=4, decimal_places=2)
    n3 = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'Value'


