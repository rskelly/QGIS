# -*- coding: utf-8 -*-

"""
***************************************************************************
    SymmetricalDifference.py
    ---------------------
    Date                 : September 2014
    Copyright            : (C) 2014 by Alexander Bruy
    Email                : alexander dot bruy at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Alexander Bruy'
__date__ = 'September 2014'
__copyright__ = '(C) 2014, Alexander Bruy'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os

from qgis.PyQt.QtGui import QIcon

from qgis.core import (QgsFeature,
                       QgsGeometry,
                       QgsFeatureRequest,
                       NULL,
                       QgsWkbTypes,
                       QgsMessageLog,
                       QgsProcessingUtils)
from processing.algs.qgis.QgisAlgorithm import QgisAlgorithm
from processing.core.parameters import ParameterVector
from processing.core.outputs import OutputVector
from processing.tools import vector

pluginPath = os.path.split(os.path.split(os.path.dirname(__file__))[0])[0]


class SymmetricalDifference(QgisAlgorithm):

    INPUT = 'INPUT'
    OVERLAY = 'OVERLAY'
    OUTPUT = 'OUTPUT'

    def icon(self):
        return QIcon(os.path.join(pluginPath, 'images', 'ftools', 'sym_difference.png'))

    def group(self):
        return self.tr('Vector overlay tools')

    def __init__(self):
        super().__init__()
        self.addParameter(ParameterVector(self.INPUT,
                                          self.tr('Input layer')))
        self.addParameter(ParameterVector(self.OVERLAY,
                                          self.tr('Difference layer')))
        self.addOutput(OutputVector(self.OUTPUT,
                                    self.tr('Symmetrical difference')))

    def name(self):
        return 'symmetricaldifference'

    def displayName(self):
        return self.tr('Symmetrical difference')

    def processAlgorithm(self, parameters, context, feedback):
        layerA = QgsProcessingUtils.mapLayerFromString(self.getParameterValue(self.INPUT), context)
        layerB = QgsProcessingUtils.mapLayerFromString(self.getParameterValue(self.OVERLAY), context)

        geomType = QgsWkbTypes.multiType(layerA.wkbType())
        fields = vector.combineVectorFields(layerA, layerB)
        writer = self.getOutputFromName(self.OUTPUT).getVectorWriter(fields, geomType, layerA.crs(), context)

        featB = QgsFeature()
        outFeat = QgsFeature()

        indexA = QgsProcessingUtils.createSpatialIndex(layerB, context)
        indexB = QgsProcessingUtils.createSpatialIndex(layerA, context)

        featuresA = QgsProcessingUtils.getFeatures(layerA, context)
        featuresB = QgsProcessingUtils.getFeatures(layerB, context)

        total = 100.0 / (QgsProcessingUtils.featureCount(layerA, context) * QgsProcessingUtils.featureCount(layerB, context))
        count = 0

        for featA in featuresA:
            geom = featA.geometry()
            diffGeom = QgsGeometry(geom)
            attrs = featA.attributes()
            intersects = indexA.intersects(geom.boundingBox())
            request = QgsFeatureRequest().setFilterFids(intersects).setSubsetOfAttributes([])
            for featB in layerB.getFeatures(request):
                tmpGeom = featB.geometry()
                if diffGeom.intersects(tmpGeom):
                    diffGeom = QgsGeometry(diffGeom.difference(tmpGeom))

            try:
                outFeat.setGeometry(diffGeom)
                outFeat.setAttributes(attrs)
                writer.addFeature(outFeat)
            except:
                QgsMessageLog.logMessage(self.tr('Feature geometry error: One or more output features ignored due to invalid geometry.'),
                                         self.tr('Processing'), QgsMessageLog.WARNING)
                continue

            count += 1
            feedback.setProgress(int(count * total))

        length = len(layerA.fields())

        for featA in featuresB:
            geom = featA.geometry()
            diffGeom = QgsGeometry(geom)
            attrs = featA.attributes()
            attrs = [NULL] * length + attrs
            intersects = indexB.intersects(geom.boundingBox())
            request = QgsFeatureRequest().setFilterFids(intersects).setSubsetOfAttributes([])
            for featB in layerA.getFeatures(request):
                tmpGeom = featB.geometry()
                if diffGeom.intersects(tmpGeom):
                    diffGeom = QgsGeometry(diffGeom.difference(tmpGeom))

            try:
                outFeat.setGeometry(diffGeom)
                outFeat.setAttributes(attrs)
                writer.addFeature(outFeat)
            except:
                QgsMessageLog.logMessage(self.tr('Feature geometry error: One or more output features ignored due to invalid geometry.'),
                                         self.tr('Processing'), QgsMessageLog.WARNING)
                continue

            count += 1
            feedback.setProgress(int(count * total))

        del writer
