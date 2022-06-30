from django.db import models

# Create your models here.


class Car(models.Model):
    car_number = models.CharField(primary_key=True, max_length=8)

    class Meta:
        managed = False
        db_table = 'car'


class Commodity(models.Model):
    commodity_id = models.CharField(primary_key=True, max_length=20)
    limit_temperature = models.FloatField()
    limit_humidity = models.FloatField()
    commodity_name = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'commodity'


class OrderMain(models.Model):
    id = models.IntegerField(primary_key=True)
    commodity = models.ForeignKey(Commodity, models.DO_NOTHING)
    start_place = models.ForeignKey('Storage', models.DO_NOTHING, db_column='start_place')
    location = models.CharField(max_length=20)
    end_time = models.CharField(max_length=20)
    transportation_time = models.FloatField()
    check_temperature = models.SmallIntegerField()
    check_humidity = models.SmallIntegerField()
    car_number = models.ForeignKey(Car, models.DO_NOTHING, db_column='car_number')
    phone_number = models.BigIntegerField()
    check_complete = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'order_main'


class OrderTime(models.Model):
    id = models.ForeignKey(OrderMain, models.DO_NOTHING, db_column='id')
    realtime = models.DateTimeField(primary_key=True)
    temperature = models.FloatField()
    humidity = models.FloatField()
    probability_temperature = models.FloatField(blank=True, null=True)
    probability_humidity = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_time'


class Storage(models.Model):
    start_place = models.CharField(primary_key=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'storage'


class Users(models.Model):
    phone_number = models.CharField(primary_key=True, max_length=20)
    user_key = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    identify = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'users'
