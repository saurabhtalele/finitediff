# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 03:26:59 2021

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
# import matplotlib.pyplot as plt
from flask import Flask

from pywebio.input import input, NUMBER, select
from pywebio.output import put_text, put_html, put_markdown, put_table, put_image, put_widget
from pywebio.platform.flask import webio_view


def forwrd():

    # differantiation order
    dd = input("order of differentiation：", type=NUMBER)
    put_text('order of differentiation', (dd))
    put_html('<hr>')
# hex of smal step h is
    hs = dd

# order of error
    err = input("order of error：", type=NUMBER)
    put_text('order of error even number or one', (err))
    put_html('<hr>')
# total number of points in cosideration
    put_text('please provide only integer number ')
    put_text('for error order result if its greter than this please realod web and try max limit integer number is equal or less than ', (dd+err-1))
    put_text(
        'take limits from 0 to 3 for example ,so points in cosiderations are 0,1,2,3 total n is 4')

    n = input("number of points in cosideration：", type=NUMBER)
    put_text('n is ', (n))
# take limits from -3 to 3 for example ,so points in cosiderations are -3,-2,-1,0,1,2,3 total n is 7

    put_text('please provide only integer number ')
    put_text(
        'stencil of 0 to 3 for example ,so points in cosiderations are 0,1,2,3 so min_limit as 0')
    min_limit = 0
    put_html('<hr>')
    put_text(
        'stencil of 0 to 3 for example ,so points in cosiderations are 0,1,2,3 so max_limit as 3')

# max limit
    max_limit = input("Input your max_limit：", type=NUMBER)
    put_text('yor stencils max limit is ', (max_limit))
    put_html('<hr>')


# makiuing array
    a0 = np.linspace(min_limit, max_limit, n)
    a0 = np. array(a0)

# making n*n matrix
    a = np.tile(a0, (n, 1))
# print(a)
    a = np.array(a)

# making indices
    b = np.linspace(0, n-1)
    b = np.arange(0, n).reshape(n, 1)

    it = np.nditer([a, b, None], flags=['external_loop'])

    with it:
        for x, y, z in it:
            z[...] = x**y
        result = it.operands[2]

# result
    bb = result

# Inserting whre one is going to come
    az = np.zeros(n-1)
    yy = np.insert(az, dd, 1)

# output capture from print
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    for i in np.nditer(a0):
        print(sp.symbols('f(x+({}*h))'.format(i)))

    output = new_stdout.getvalue()

    sys.stdout = old_stdout

    j = output

# solving matrix
    hh = np.linalg.solve(bb, yy)

    a = hh*np.math.factorial(dd)
# print(a)


# symbols manupalation and list to symbols conversion
# print(type(j))
    d = [x.replace('\n', '  ') for x in j]
# Original Array
    # array = np.array(j, dtype=np.str)       This is numpy pywebio pytexit==0.3.4 numpy==1.19.2 sympy==1.6.2 flask old deploy heroku
    array = np.array(j, dtype=str)
# print(array)

# Split the element of the said array
# with spaces
    sparr = np.char.split(array)      # imp step str to array numpy

# print(sparr)

    d = np.asarray(sparr, dtype=object)

    d = d.tolist()                    # convert to list
# print(d)

    d = sp.symbols(d)
    d = np.array(d)
# print(d)


# multiplyer
    B = np.array(a)
# B=B.astype(str)
# c = B.tolist()
    c = B.astype(object)
# print(c)

    re.sub(r' *\n *', '\t',
           np.array_str(np.c_[c, d]).replace('[', '(').replace(']', ')').strip())

    res = "\t".join("({}*{})+".format(x, y) for x, y in zip(c, d))

    name = res.rstrip(res[-1])


# print('(',name,')','*','*1/h**',hs)

# captiring print
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    print('(', name, ')', '*', '1/h**', hs)

    kj = new_stdout.getvalue()

    sys.stdout = old_stdout

    def remove(string):
        pattern = re.compile(r'\s+')
        return re.sub(pattern, '', string)

# Driver Program
    string = kj
# remove will remove all spaces
    yy = remove(string)

    # put_text('%s' % (remove(string)))

# making variable to latex plote
    y = py2tex(yy, print_latex=False, print_formula=False)
    o = y.replace('+-', '-')
    # put_text('%s' % o)

    def org(o):
        w = o
        p = w
        pp = p.replace('$$', ' ')
        tt = " ' "
        # string="r"
        # pg=string+pp
        # tg=" ' "
        pg = tt+pp+tt
        return pg

    t = org(o)


# matplotlib

    lat = t

# #add text
#     ax = plt.axes([1,0,0.1,0.1]) #left,bottom,width,height
#     ax.set_xticks([])
#     ax.set_yticks([])
#     ax.axis('off')
#     plt.text(0.2,0.2,r'$%s$' % lat ,size=500,color="red",fontsize=100)
# #hide axes
#     fig = plt.gca()
#     fig.axes.get_xaxis().set_visible(False)
#     fig.axes.get_yaxis().set_visible(False)
#     plt.savefig('images/out.jpeg', bbox_inches='tight', pad_inches=0)
#     plt.close()

# save image

    # img = open('images/out.jpeg', 'rb').read()
    # put_image(img, width='500000000px')

    put_html('<hr>')
    put_text('this is python output  %s' % yy)

    put_html('<hr>')

    # visualize equation
    # tpl = '''<!DOCTYPE html><html><head>  <meta charset="utf-8">  <meta name="viewport" content="width=device-width">  <title>MathJax example</title>  <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>  <script id="MathJax-script" async          src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">  </script></head><body><p>{{#contents}}{{& pywebio_output_parse}}{{/contents}}</p></body></html>'''
    tpl = '''<!DOCTYPE html>
    <html><head>  <meta charset="utf-8">  
    <meta name="viewport" content="width=device-width"> 
    <title> </title>  
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script> 
    <script id="MathJax-script" async          src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">  </script>
    </head>
    <body>
    <p>{{#contents}}{{& pywebio_output_parse}}{{/contents}}
          </p>
          </body>
          </html>'''
    put_widget(tpl, {"contents": [put_text((lat))]})

    # for latex output
    put_html('<hr>')
    put_text('upper is latex out put %s' % o)

# if __name__ == '__main__':
#     bmi()
