# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 02:36:46 2021

@author: s
"""
import numpy.matlib
import numpy as np
import sympy as sp
import re
import sys
import io
from io import StringIO
import string
from pytexit import py2tex
#import matplotlib.pyplot as plt

import argparse
from pywebio import start_server
from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask, send_from_directory

from flask import Flask

from test1 import *

from test2 import *

from test3 import *



app = Flask(__name__)

def bmi():
    
    defff_type = select('diferentiation scheme Type', ['forwrd', 'backwrd','central'])
    if (defff_type == 'forwrd'):
        defff_type = forwrd()
        
    elif (defff_type == 'backwrd'):
        defff_type = backwrd()
        
    elif (defff_type == 'central'):
        defff_type = central()
    
    bmi=deff_type
     
app.add_url_rule('/tool', 'webio_view', webio_view(bmi),
            methods=['GET', 'POST', 'OPTIONS'])  # need GET,POST and OPTIONS methods

# app.run(host='localhost', port=500)
if __name__ == '__main__':
    import argparse


    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=800)
    args = parser.parse_args()

    start_server(bmi, port=args.port)
