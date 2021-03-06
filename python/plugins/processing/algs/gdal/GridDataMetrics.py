# -*- coding: utf-8 -*-

"""
***************************************************************************
    GridDataMetrics.py
    ---------------------
    Date                 : October 2013
    Copyright            : (C) 2013 by Alexander Bruy
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
from builtins import str

__author__ = 'Alexander Bruy'
__date__ = 'October 2013'
__copyright__ = '(C) 2013, Alexander Bruy'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os

from qgis.PyQt.QtGui import QIcon

from processing.algs.gdal.GdalAlgorithm import GdalAlgorithm
from processing.core.parameters import ParameterVector
from processing.core.parameters import ParameterTableField
from processing.core.parameters import ParameterSelection
from processing.core.parameters import ParameterNumber
from processing.core.outputs import OutputRaster
from processing.tools import dataobjects
from processing.algs.gdal.GdalUtils import GdalUtils


pluginPath = os.path.split(os.path.split(os.path.dirname(__file__))[0])[0]


class GridDataMetrics(GdalAlgorithm):

    INPUT = 'INPUT'
    Z_FIELD = 'Z_FIELD'
    METRIC = 'METRIC'
    RADIUS_1 = 'RADIUS_1'
    RADIUS_2 = 'RADIUS_2'
    MIN_POINTS = 'MIN_POINTS'
    ANGLE = 'ANGLE'
    NODATA = 'NODATA'
    OUTPUT = 'OUTPUT'
    RTYPE = 'RTYPE'

    TYPE = ['Byte', 'Int16', 'UInt16', 'UInt32', 'Int32', 'Float32', 'Float64']

    DATA_METRICS = ['Minimum', 'Maximum', 'Range', 'Count', 'Average distance',
                    'Average distance between points']

    def __init__(self):
        super().__init__()
        self.addParameter(ParameterVector(self.INPUT,
                                          self.tr('Input layer'), [dataobjects.TYPE_VECTOR_POINT]))
        self.addParameter(ParameterTableField(self.Z_FIELD,
                                              self.tr('Z field'), self.INPUT,
                                              ParameterTableField.DATA_TYPE_NUMBER, True))
        self.addParameter(ParameterSelection(self.METRIC,
                                             self.tr('Metrics'), self.DATA_METRICS, 0))
        self.addParameter(ParameterNumber(self.RADIUS_1,
                                          self.tr('Radius 1'), 0.0, 99999999.999999, 0.0))
        self.addParameter(ParameterNumber(self.RADIUS_2,
                                          self.tr('Radius 2'), 0.0, 99999999.999999, 0.0))
        self.addParameter(ParameterNumber(self.MIN_POINTS,
                                          self.tr('Min points'), 0.0, 99999999.999999, 0.0))
        self.addParameter(ParameterNumber(self.ANGLE,
                                          self.tr('Angle'), 0.0, 359.0, 0.0))
        self.addParameter(ParameterNumber(self.NODATA,
                                          self.tr('Nodata'), 0.0, 99999999.999999, 0.0))
        self.addParameter(ParameterSelection(self.RTYPE,
                                             self.tr('Output raster type'), self.TYPE, 5))

        self.addOutput(OutputRaster(self.OUTPUT, self.tr('Interpolated metrics')))

    def name(self):
        return 'griddatametrics'

    def displayName(self):
        return self.tr('Grid (Data metrics)')

    def icon(self):
        return QIcon(os.path.join(pluginPath, 'images', 'gdaltools', 'grid.png'))

    def group(self):
        return self.tr('Raster analysis')

    def getConsoleCommands(self, parameters):
        arguments = ['-l']
        arguments.append(
            os.path.basename(os.path.splitext(
                str(self.getParameterValue(self.INPUT)))[0]))

        fieldName = self.getParameterValue(self.Z_FIELD)
        if fieldName is not None and fieldName != '':
            arguments.append('-zfield')
            arguments.append(fieldName)

        metric = self.getParameterValue(self.METRIC)
        if metric == 0:
            params = 'minimum'
        elif metric == 1:
            params = 'maximum'
        elif metric == 2:
            params = 'range'
        elif metric == 3:
            params = 'count'
        elif metric == 4:
            params = 'average_distance'
        elif metric == 5:
            params = 'average_distance_pts'

        params += ':radius1=%s' % self.getParameterValue(self.RADIUS_1)
        params += ':radius2=%s' % self.getParameterValue(self.RADIUS_2)
        params += ':angle=%s' % self.getParameterValue(self.ANGLE)
        params += ':min_points=%s' % self.getParameterValue(self.MIN_POINTS)
        params += ':nodata=%s' % self.getParameterValue(self.NODATA)

        arguments.append('-a')
        arguments.append(params)
        arguments.append('-ot')
        arguments.append(self.TYPE[self.getParameterValue(self.RTYPE)])
        arguments.append(str(self.getParameterValue(self.INPUT)))
        arguments.append(str(self.getOutputValue(self.OUTPUT)))

        return ['gdal_grid', GdalUtils.escapeAndJoin(arguments)]
