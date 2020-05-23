from django.db import models
from django.contrib.postgres.fields import ArrayField
import os
import csv
import pandas as pd
import math
import numpy as np

class Amplifier(models.Model):
    responsible = models.CharField(max_length=200, verbose_name="Responsável")
    email = models.EmailField() 
    reference = models.CharField(max_length=200,verbose_name="Referência")  
    mask = models.FileField(upload_to='csv files/', null = True, blank=True, verbose_name="Máscara (.csv)")
    def __str__(self):
        return self.reference
	
class State(models.Model):
    amplifier = models.ForeignKey(Amplifier, on_delete=models.CASCADE)
    pin_total = models.FloatField()
    pout_total = models.FloatField()
    frequency_ch = ArrayField(models.FloatField(), null=True)
    ganho = ArrayField(models.FloatField(), null=True)
    nf = ArrayField(models.FloatField(), null=True)
    # ArrayField é referente ao postgree
    def __str__(self):
        return self.amplifier.reference

class Document(models.Model):
    #description = models.CharField(max_length=255, blank=True)
    #document = models.FileField(upload_to='tmp/', null = True, blank=True)
    file_signal = models.FileField(upload_to='tmp/', null = True, blank=True)
    file_h5 = models.FileField(upload_to='tmp/', null = True, blank=True)
    file_info = models.FileField(upload_to='tmp/', null = True, blank=True)
    
    def __str__(self):
        return self.file_info

class Modelo(models.Model):
    model_type = models.CharField(max_length=255, blank=True, verbose_name="Tipo do Modelo") # RNA ou SVM
    amplifier = models.ForeignKey(Amplifier, on_delete=models.CASCADE, verbose_name="Amplificador") # 
    file_h5 = models.FileField(upload_to='h5files/', null = True, blank=True, verbose_name="Modelo NN (.h5)")
    file_txt = models.FileField(upload_to='txtfiles/', null = True, blank=True, verbose_name="Informação da rede (.txt)")
    def __str__(self):
        return self.amplifier.reference

class RequestPrediction(models.Model):
    name = models.CharField(max_length=255, blank=True, verbose_name="Título") # RNA ou SVM
    net_model = models.ForeignKey(Modelo, on_delete=models.CASCADE, verbose_name="Modelo") #
    pin_signal = models.FileField(upload_to='requests/', null = True, blank=True, verbose_name="Sinais de entrada (Pin)")
    ganho = models.IntegerField(null=True)
    def __str__(self):
        return self.name

