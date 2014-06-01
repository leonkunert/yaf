from django.contrib.auth.models import User
from django.db import models


class Bus(models.Model):
    id = models.AutoField(primary_key=True)
    nummer = models.CharField(max_length=45)
    typ = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'bus'


class Busfahrer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    vorname = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'busfahrer'


class Einsatzzeit(models.Model):
    id = models.AutoField(primary_key=True)
    von_wochentag = models.IntegerField()
    bis_wochentag = models.IntegerField()
    von_uhrzeit = models.IntegerField()
    bis_uhrzeit = models.IntegerField()
    takt = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'einsatzzeit'


class Linie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    einsetzfahrt = models.CharField(max_length=45)
    aussetzfahrt = models.CharField(max_length=45)
    rueckfahrt = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'linie'


class EinsatzzeitLinie(models.Model):
    id = models.AutoField(primary_key=True)  # NEW!
    einsatzzeit = models.ForeignKey(Einsatzzeit, db_column='einsatzzeit')  # HAD PK! REMOVE! ## rename einsatzzeit_id -> einsatzzeit
    linie = models.ForeignKey(Linie, db_column='linie') ## rename linie_id -> linie

    class Meta:
        managed = False
        db_table = 'einsatzzeit-linie-mapping'


class Haltestelle(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'haltestelle'


class Fahrplan(models.Model):
    id = models.AutoField(primary_key=True)  # NEW!
    wochentag = models.IntegerField()
    stunde = models.IntegerField()
    minute = models.IntegerField()
    haltestelle = models.ForeignKey(Haltestelle, db_column='haltestelle') ## rename haltestelle_id -> haltestelle
    linie = models.ForeignKey(Linie, db_column='linie') ## rename linie_id = linie

    class Meta:
        managed = False
        db_table = 'fahrplan'


class Kurs(models.Model):
    id = models.AutoField(primary_key=True)
    bus = models.ForeignKey(Bus, db_column='bus')
    fahrer = models.ForeignKey(Busfahrer, db_column='fahrer')
    linie = models.ForeignKey(Linie, db_column='linie')
    wochentag = models.IntegerField()
    schicht = models.IntegerField()
    tour = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'kurs'


class HaltestelleLinie(models.Model):
    id = models.AutoField(primary_key=True)  # NEW!
    haltestelle = models.ForeignKey(Haltestelle, db_column='haltestelle') ## rename haltestelle_id -> haltestelle
    linie = models.ForeignKey(Linie, db_column='linie') ## rename linie_id -> linie
    fahrtzeit = models.IntegerField()
    haltestellennummer = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'haltestelle-linie-mapping'


class FahrerUserMap(models.Model):
    id = models.AutoField(primary_key=True)
    fahrer = models.ForeignKey(Busfahrer)
    user = models.ForeignKey(User)

    class Meta:
        db_table = 'fahrer-user-map'