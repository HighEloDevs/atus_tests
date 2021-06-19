# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2021 Leonardo Eiji Tamayose, Guilherme Ferrari Fortino

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from PyQt5.QtCore import QObject, QJsonValue, QUrl, pyqtSignal, pyqtSlot
import pandas as pd
import numpy as np
import platform
import json

class Histogram(QObject):
    """Backend for histogram page"""

    # Signals
    fillPage = pyqtSignal(QJsonValue)

    def __init__(self, canvas, messageHandler) -> None:
        super().__init__()
        self.messageHandler = messageHandler
        self.canvas         = canvas
        self.path           = ""
        self.histAlign      = {"Centro" : "center", "Direita" : "right", "Esquerda" : "left"}
        self.histOrient     = {"Vertical" : "vertical", "Horizontal" : "horizontal"}


########################### EDITE AQUI \/ #############################
    @pyqtSlot(QJsonValue)
    def plot(self, data):
        data = QJsonValue.toVariant(data)
        # print(QJsonValue.toVariant(data))
        self.clearAxis()
        axes =  self.canvas.figure.add_subplot(111)
        if data["props"]["grid"]:
            axes.grid(True, which='major')
        if data["props"]["logy"]:
            axes.set_yscale('log')
        if data["props"]["logx"]:
            axes.set_xscale('log')

        xdiv = self.makeFloat(data["props"]["xdiv"], 0.)
        xmin = self.makeFloat(data["props"]["xmin"], 0.)
        xmax = self.makeFloat(data["props"]["xmax"], 0.)
        ydiv = self.makeFloat(data["props"]["ydiv"], 0.)
        ymin = self.makeFloat(data["props"]["ymin"], 0.)
        ymax = self.makeFloat(data["props"]["ymax"], 0.)

        if xdiv != 0. and (xmax != 0. or xmin != 0.):
            axes.set_xticks(np.linspace(xmin, xmax, xdiv + 1))
            axes.set_xlim(left = xmin, right = xmax)

        else:
            if xmin == 0. and xmax != 0.:
                axes.set_xlim(left = None, right = xmax)
            elif xmin != 0. and xmax == 0.:
                axes.set_xlim(left = xmin, right = None)
            elif xmin != 0. and xmax != 0.:
                axes.set_xlim(left = xmin, right = xmax)
        
        if ydiv != 0. and (ymax != 0. or ymin != 0.):
            axes.set_yticks(np.linspace(ymin, ymax, ydiv + 1))
            axes.set_ylim(bottom = ymin, top = ymax)
        else:
            if ymin == 0. and ymax != 0.:
                axes.set_ylim(bottom = None, top = ymax)
            elif ymin != 0. and ymax == 0.:
                axes.set_ylim(bottom = ymin, top = None)
            elif ymin != 0. and ymax != 0.:
                axes.set_ylim(bottom = ymin, top = ymax)
        df = pd.DataFrame.from_records(data["data"][0]["data"])
        print(data)
        print(data.keys())
        label = data["kargs"].pop("label")
        if len(df["weight"]) > 0:
            counts, bins, _ = axes.hist(x = data["data"]["data"], bins = self.makeInt(data["props"]["bins"], 10),
            range = (self.makeFloat(data["props"]["rangexmin"], -np.inf),
            self.makeFloat(data["props"]["rangexmax"], np.inf)),
            weights     = df["weight"],
            density     = False, cumulative = False, bottom = 0,
            histtype    = data["props"]["histType"],
            align       = self.histAlign[data["props"]["histAlign"]],
            orientation = self.histOrient[data["props"]["histOrientation"]],
            log = False, rwidth = 0, capstyle = "round", ls = "--", aa = True,
            kwargs = data["kargs"])
#         'kargs': {'alpha': '1.0', 'ec': '#006e00', 
# 'fc': '#006e00', 'fill': True, 'hatch': '/', 'label': True, 'lw': 3}
########################### EDITE AQUI /\ #############################

    @pyqtSlot()
    def new(self):
        self.path = ""
        self.fillPage.emit(None)

    @pyqtSlot(QJsonValue, result=bool)
    def save(self, data):
        # If there's no path for saving, saveAs()
        if self.path == '':
            return False

        # Getting properties
        data = data.toVariant()

        if platform.system() == "Linux":
            if self.path[-5:] == ".json":
                with open(self.path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
            else: 
                with open(self.path + ".json", 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
        else:
            with open(self.path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

        return True

    @pyqtSlot(str, QJsonValue)
    def saveAs(self, path, data):
        # Getting path
        self.path = QUrl(path).toLocalFile()
        self.save(data)

    @pyqtSlot(str)
    def load(self, path):
        # Reseting frontend
        self.new()

        # Getting path
        self.path = QUrl(path).toLocalFile()

        # Getting props
        with open(self.path, encoding='utf-8') as file:
            props = json.load(file)

        if "key" in props:
            if props["key"].split('-')[-1] != 'hist':
                self.messageHandler.raiseError("Este projeto pertence à outra aba do ATUS.")
                return 0
        else:
            self.messageHandler.raiseError("O arquivo carregado é incompatível com o ATUS.")
            return 0

        self.fillPage.emit(QJsonValue.fromVariant(props))

    @pyqtSlot(str, result=QJsonValue)
    def checkData(self, filePath):
        '''
        Check if data is valid
        Returns: True + Data if valid data, False otherwise
        '''
        package = {
            "isValid": False,
            "data"   : None
        }
        # Loading from .csv or (.txt and .tsv)
        filePath = QUrl(filePath).toLocalFile()
        if filePath[-3:] == "csv":
            try:
                df = pd.read_csv(filePath, sep=',', header=None, dtype = str).replace(np.nan, "0")
            except pd.errors.ParserError:
                self.messageHandler.raiseError("Separação de colunas de arquivos csv são com vírgula (","). Rever dados de entrada.")
                # Separação de colunas de arquivos csv são com vírgula (","). Rever dados de entrada.
                return QJsonValue.fromVariant(package)
        elif filePath[-3:] == "tsv" or filePath[-3:] == "txt":
            try:
                df = pd.read_csv(filePath, sep='\t', header=None, dtype = str).replace(np.nan, "0")
            except pd.errors.ParserError:
                self.messageHandler.raiseError("Separação de colunas de arquivos txt e tsv são com tab. Rever dados de entrada.")
                # Separação de colunas de arquivos txt e tsv são com tab. Rever dados de entrada.
                return QJsonValue.fromVariant(package)
        else:
            self.messageHandler.raiseError("Apenas arquivos .txt, .csv, .tsv são suportados.")
            return QJsonValue.fromVariant(package)

        if len(df.columns) == 1:
            df.columns = ["x"]
        elif len(df.columns) == 2:
            df.columns = ["x", "weight"]
        else:
            self.messageHandler.raiseError("A tabela de histogramas deve conter no máximo 2 colunas: x e pesos.")
            return QJsonValue.fromVariant(package)
        
        for i in df.columns:
            # Replacing comma for dots
            df[i] = [x.replace(',', '.') for x in df[i]]
            # Converting everything to float
            try:
                df[i] = df[i].astype(float)
            except:
                self.messageHandler.raiseError("A entrada de dados só permite entrada de números. Rever arquivo de entrada.")
                # Há células não numéricas. A entrada de dados só permite entrada de números. Rever arquivo de entrada.
                return QJsonValue.fromVariant(package)

        package["data"] = df.to_json()
        package["isValid"] = True
        return package

    def makeFloat(self, var, value):
        try:
            return float(var)
        except:
            return value

    def makeInt(self, var, value):
        try:
            return int(var)
        except:
            return value

    def clearAxis(self):
        """Clear the current plot in the axis."""
        try:
            self.canvas.axes.remove()
        except:
            pass
        try:
            self.canvas.ax1.remove()
            self.canvas.ax2.remove()
        except:
            pass