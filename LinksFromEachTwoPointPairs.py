# -*- coding: utf-8 -*-
__author__ = 'szchixy'
__create_date__ = '2022-04-18'

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsExpression,
                       QgsExpressionContext,
                       QgsFeature,
                       QgsLineString,
                       QgsPoint,
                       QgsGeometry,
                       QgsFields)

class LinksFromEachTwoPointPairs(QgsProcessingAlgorithm):
    OUTPUT = 'OUTPUT'
    INPUT = 'INPUT'

    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr('Input layer (Point)'),
                [QgsProcessing.TypeVectorPoint]
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Output layer (LineString)')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)
        (sink, dest_id) = self.parameterAsSink(parameters, self.OUTPUT,
                context, QgsFields(), 2, source.sourceCrs())

        total = 0
        for i in range(1, source.featureCount()):
            total += i
        features = list(source.getFeatures())

        ex = QgsExpression('$x')
        ey = QgsExpression('$y')
        context_source_layer = QgsExpressionContext()
        context_source_layer.appendScope(source.createExpressionContextScope())
        
        count = 0
        for i in range(1, source.featureCount()):
            context_source_layer.setFeature(features[i])
            x1 = ex.evaluate(context_source_layer)
            y1 = ey.evaluate(context_source_layer)
            for j in range(i):
                if feedback.isCanceled():
                    break
                context_source_layer.setFeature(features[j])
                x2 = ex.evaluate(context_source_layer)
                y2 = ey.evaluate(context_source_layer)
                f = QgsFeature()
                line = QgsLineString(QgsPoint(x1, y1), QgsPoint(x2, y2))
                f.setGeometry(QgsGeometry.fromPolyline(line))
                sink.addFeature(f, QgsFeatureSink.FastInsert)
                count += 1
                feedback.setProgress(int((count) / total * 100))

        return {self.OUTPUT: dest_id}

    def shortHelpString(self):
        return self.tr(
            '''
            Input layer (Point): 输入一个 Point/MultiPoint 图层
            
            算法: 对点图层中的任意两点连接一条线段
            
            Output layer (LineString): 输出一个 LineString 图层
            ''')

    def name(self):
        return 'LinksFromEachTwoPointPairs'

    def displayName(self):
        return self.tr(self.name())

    # def group(self):
    #     return self.tr(self.groupId())

    # def groupId(self):
    #     return 'default'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return LinksFromEachTwoPointPairs()
