# -*- coding: utf-8 -*-

"""
***************************************************************************
    TextToFloat.py
    ---------------------
    Date                 : May 2010
    Copyright            : (C) 2010 by Michael Minn
    Email                : pyqgis at michaelminn dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Michael Minn'
__date__ = 'May 2010'
__copyright__ = '(C) 2010, Michael Minn'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from qgis.PyQt.QtCore import QVariant
from qgis.core import (QgsApplication,
                       QgsField,
                       QgsProcessingUtils)
from processing.algs.qgis.QgisAlgorithm import QgisAlgorithm
from processing.core.parameters import ParameterVector
from processing.core.parameters import ParameterTableField
from processing.core.outputs import OutputVector


class TextToFloat(QgisAlgorithm):
    INPUT = 'INPUT'
    FIELD = 'FIELD'
    OUTPUT = 'OUTPUT'

    def icon(self):
        return QgsApplication.getThemeIcon("/providerQgis.svg")

    def svgIconPath(self):
        return QgsApplication.iconPath("providerQgis.svg")

    def group(self):
        return self.tr('Vector table tools')

    def __init__(self):
        super().__init__()
        self.addParameter(ParameterVector(self.INPUT,
                                          self.tr('Input Layer')))
        self.addParameter(ParameterTableField(self.FIELD,
                                              self.tr('Text attribute to convert to float'),
                                              self.INPUT, ParameterTableField.DATA_TYPE_STRING))
        self.addOutput(OutputVector(self.OUTPUT, self.tr('Float from text')))

    def name(self):
        return 'texttofloat'

    def displayName(self):
        return self.tr('Text to float')

    def processAlgorithm(self, parameters, context, feedback):
        layer = QgsProcessingUtils.mapLayerFromString(self.getParameterValue(self.INPUT), context)
        fieldName = self.getParameterValue(self.FIELD)
        idx = layer.fields().lookupField(fieldName)

        fields = layer.fields()
        fields[idx] = QgsField(fieldName, QVariant.Double, '', 24, 15)

        writer = self.getOutputFromName(self.OUTPUT).getVectorWriter(fields, layer.wkbType(), layer.crs(), context)

        features = QgsProcessingUtils.getFeatures(layer, context)

        total = 100.0 / QgsProcessingUtils.featureCount(layer, context)
        for current, f in enumerate(features):
            value = f[idx]
            try:
                if '%' in value:
                    f[idx] = float(value.replace('%', '')) / 100.0
                else:
                    f[idx] = float(value)
            except:
                f[idx] = None

            writer.addFeature(f)
            feedback.setProgress(int(current * total))

        del writer
