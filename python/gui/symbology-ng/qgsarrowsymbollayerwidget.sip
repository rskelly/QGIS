/************************************************************************
 * This file has been generated automatically from                      *
 *                                                                      *
 * src/gui/symbology-ng/qgsarrowsymbollayerwidget.h                     *
 *                                                                      *
 * Do not edit manually ! Edit header and run scripts/sipify.pl again   *
 ************************************************************************/



class QgsArrowSymbolLayerWidget: QgsSymbolLayerWidget
{

%TypeHeaderCode
#include "qgsarrowsymbollayerwidget.h"
%End
  public:

    QgsArrowSymbolLayerWidget( const QgsVectorLayer *layer, QWidget *parent /TransferThis/ = 0 );
%Docstring
 Constructor
 \param layer the layer where this symbol layer is applied
 \param parent the parent widget
%End

    static QgsSymbolLayerWidget *create( const QgsVectorLayer *layer ) /Factory/;
%Docstring
 Static creation method
 \param layer the layer where this symbol layer is applied
 :rtype: QgsSymbolLayerWidget
%End

    virtual void setSymbolLayer( QgsSymbolLayer *layer );
    virtual QgsSymbolLayer *symbolLayer();

};

/************************************************************************
 * This file has been generated automatically from                      *
 *                                                                      *
 * src/gui/symbology-ng/qgsarrowsymbollayerwidget.h                     *
 *                                                                      *
 * Do not edit manually ! Edit header and run scripts/sipify.pl again   *
 ************************************************************************/
