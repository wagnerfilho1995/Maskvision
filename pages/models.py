from django.db import models
from django.contrib.postgres.fields import ArrayField
import os
import csv
import pandas as pd
import math
import numpy as np

class Amplifier(models.Model):
    responsible = models.CharField(max_length=200, verbose_name="Responsible")
    email = models.EmailField() 
    reference = models.CharField(max_length=200,verbose_name="Reference")  
    mask = models.FileField(upload_to='csv files/', null = True, blank=True, verbose_name="Mask")
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
    file_signal = models.FileField(upload_to='tmp/', null = True, blank=True)
    file_h5 = models.FileField(upload_to='tmp/', null = True, blank=True)
    file_info = models.FileField(upload_to='tmp/', null = True, blank=True)
    
    def __str__(self):
        return self.file_info

class Modelo(models.Model):
    model_type = models.CharField(max_length=255, blank=True, verbose_name="Model Type") # RNA ou SVM
    amplifier = models.ForeignKey(Amplifier, on_delete=models.CASCADE, verbose_name="Amplifiers") # 
    file_h5 = models.FileField(upload_to='h5files/', null = True, blank=True, verbose_name="Model NN (.h5)")
    file_txt = models.FileField(upload_to='txtfiles/', null = True, blank=True, verbose_name="Network information(.txt)")
    def __str__(self):
        return self.amplifier.reference

class RequestPrediction(models.Model):
    net_model = models.ForeignKey(Modelo, on_delete=models.CASCADE, verbose_name="Model") #
    pin_signal = models.FileField(upload_to='requests/', null = True, blank=True, verbose_name="Input signal (Pin)")
    ganho = models.IntegerField(null=True)
    def __str__(self):
        return self.name

