# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 11:59:27 2021

@author: Leonardo Eiji Tamayose & Guilherme Ferrari Fortino 
"""

# =============================================================================
# import numpy as np
# import matplotlib.pyplot as plt
# from lmfit.models import ExpressionModel
# from lmfit import Parameters
# =============================================================================

import sys
from src.MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, QtGui, QtCore
import qdarkstyle


def main():
    # Initializing App
    app = QApplication(sys.argv)
    
    # Setting Style
    app.setStyle('Fusion')
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    
    # Opening Main Window
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()      

# =============================================================================
# f = lambda x: x**3 + x**2 + x + 10
# x = np.linspace(0, 10, 20)
# z = f(x) + np.random.randn(20)*5
# =============================================================================

# =============================================================================
# x = [19, 63, 110, 150, 199, 243]
# y = [17.6, 18.7, 19.8, 20.5, 21.7, 22.8]
# sig = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
# 
# x = np.array(x)
# #x = np.deg2rad(x)
# y = np.array(y)
# sig = np.array(sig)
# #sig = np.deg2rad(sig)
# 
# gmod = ExpressionModel('a*x + b', absolute_sigma = True, sigma = sig)
# 
# p = Parameters()
# for i in gmod.param_names:
#     p.add(i, value=1)
# 
# result = gmod.fit(data=y, x=x, params=p, scale_covar = False, weights = 1/sig) #, fit_kws = {absolute_sigma : True})
# #result.plot_fit()
# 
# print(result.fit_report())
# =============================================================================
