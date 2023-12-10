
import cv2
import matplotlib.pyplot as plt
import os.path
import os
import urllib
import datetime
import pandas as pd
import moviepy
from moviepy.editor import *
import xlwt
from azureml.core.experiment import Experiment
from azureml.core.workspace import Workspace
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
import time
import random
import seaborn as sns
from msrest.authentication import ApiKeyCredentials
print('success')