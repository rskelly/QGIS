/************************************************************************
 * This file has been generated automatically from                      *
 *                                                                      *
 * src/core/qgsmaplayerstore.h                                          *
 *                                                                      *
 * Do not edit manually ! Edit header and run scripts/sipify.pl again   *
 ************************************************************************/






class QgsMapLayerStore : QObject
{
%Docstring
 A storage object for map layers, in which the layers are owned by the
 store and have their lifetime bound to the store.
.. versionadded:: 3.0
%End

%TypeHeaderCode
#include "qgsmaplayerstore.h"
%End
  public:

    explicit QgsMapLayerStore( QObject *parent /TransferThis/ = 0 );
%Docstring
 Constructor for QgsMapLayerStore.
%End

    ~QgsMapLayerStore();

    int count() const;
%Docstring
 Returns the number of layers contained in the store.
 :rtype: int
%End


    int __len__() const;
%Docstring
 Returns the number of layers contained in the store.
 :rtype: int
%End
%MethodCode
    sipRes = sipCpp->count();
%End

    QgsMapLayer *mapLayer( const QString &id ) const;
%Docstring
 Retrieve a pointer to a layer by layer ``id``.
 \param id ID of layer to retrieve
 :return: matching layer, or None if no matching layer found
.. seealso:: mapLayersByName()
.. seealso:: mapLayers()
 :rtype: QgsMapLayer
%End

    QList<QgsMapLayer *> mapLayersByName( const QString &name ) const;
%Docstring
 Retrieve a list of matching layers by layer ``name``.
 \param name name of layers to match
 :return: list of matching layers
.. seealso:: mapLayer()
.. seealso:: mapLayers()
 :rtype: list of QgsMapLayer
%End

    QMap<QString, QgsMapLayer *> mapLayers() const;
%Docstring
 Returns a map of all layers by layer ID.
.. seealso:: mapLayer()
.. seealso:: mapLayersByName()
.. seealso:: layers()
 :rtype: QMap<str, QgsMapLayer *>
%End


    QList<QgsMapLayer *> addMapLayers( const QList<QgsMapLayer *> &layers /Transfer/);

%Docstring
 \brief
 Add a list of ``layers`` to the store. Ownership of the layers is transferred
 to the store.

 The layersAdded() and layerWasAdded() signals will always be emitted.

 \param layers A list of layer which should be added to the store.
 \param takeOwnership Ownership will be transferred to the layer store.
                      If you specify false here you have take care of deleting
                      the layers yourself. Not available in Python.

 :return: a list of the map layers that were added
         successfully. If a layer is invalid, or already exists in the store,
         it will not be part of the returned list.

.. seealso:: addMapLayer()
 :rtype: list of QgsMapLayer
%End

    QgsMapLayer *addMapLayer( QgsMapLayer *layer /Transfer/);

%Docstring
 \brief
 Add a ``layer`` to the store. Ownership of the layer is transferred to the
 store.

 The layersAdded() and layerWasAdded() signals will always be emitted.
 If you are adding multiple layers at once, you should use
 addMapLayers() instead.

 \param layer A layer to add to the store
 \param takeOwnership Ownership will be transferred to the layer store.
                      If you specify false here you have take care of deleting
                      the layers yourself. Not available in Python.

 :return: None if unable to add layer, otherwise pointer to newly added layer

.. seealso:: addMapLayers

.. note::

   Use addMapLayers() if adding more than one layer at a time.
.. seealso:: addMapLayers()
 :rtype: QgsMapLayer
%End

    void removeMapLayers( const QStringList &layerIds ) /PyName=removeMapLayersById/;
%Docstring
 \brief
 Remove a set of layers from the store by layer ID.

 The specified layers will be removed from the store.
 These layers will also be deleted.

 \param layerIds list of IDs of the layers to remove

.. seealso:: takeMapLayer()
.. seealso:: removeMapLayer()
.. seealso:: removeAllMapLayers()
.. note::

   available in Python bindings as removeMapLayersById.
%End

    void removeMapLayers( const QList<QgsMapLayer *> &layers );
%Docstring
 \brief
 Remove a set of ``layers`` from the store.

 The specified layers will be removed from the store.
 These layers will also be deleted.

 \param layers A list of layers to remove. Null pointers are ignored.

.. seealso:: takeMapLayer()
.. seealso:: removeMapLayer()
.. seealso:: removeAllMapLayers()
%End

    void removeMapLayer( const QString &id );
%Docstring
 \brief
 Remove a layer from the store by layer ``id``.

 The specified layer will be removed from the store. The layer will also be deleted.

 \param id ID of the layer to remove

.. seealso:: takeMapLayer()
.. seealso:: removeMapLayers()
.. seealso:: removeAllMapLayers()
%End

    void removeMapLayer( QgsMapLayer *layer );
%Docstring
 \brief
 Remove a ``layer`` from the store.

 The specified layer will be removed from the store. The layer will also be deleted.

 \param layer The layer to remove. Null pointers are ignored.

.. seealso:: takeMapLayer()
.. seealso:: removeMapLayers()
.. seealso:: removeAllMapLayers()
%End

    QgsMapLayer *takeMapLayer( QgsMapLayer *layer ) /TransferBack/;
%Docstring
 Takes a ``layer`` from the store. If the layer was owned by the store, the
 layer will be returned without deleting it. The caller takes ownership of
 the layer and is responsible for deleting it.
.. seealso:: removeMapLayer()
 :rtype: QgsMapLayer
%End

    void removeAllMapLayers();
%Docstring
 Removes all registered layers. These layers will also be deleted.

.. note::

   Calling this method will cause the removeAll() signal to
 be emitted.
.. seealso:: removeMapLayer()
.. seealso:: removeMapLayers()
%End

  signals:

    void layersWillBeRemoved( const QStringList &layerIds );
%Docstring
 Emitted when one or more layers are about to be removed from the store.

 \param layerIds A list of IDs for the layers which are to be removed.
.. seealso:: layerWillBeRemoved()
.. seealso:: layersRemoved()
%End

    void layersWillBeRemoved( const QList<QgsMapLayer *> &layers );
%Docstring
 Emitted when one or more layers are about to be removed from the store.

 \param layers A list of layers which are to be removed.
.. seealso:: layerWillBeRemoved()
.. seealso:: layersRemoved()
%End

    void layerWillBeRemoved( const QString &layerId );
%Docstring
 Emitted when a layer is about to be removed from the store.

 \param layerId The ID of the layer to be removed.

.. note::

   Consider using layersWillBeRemoved() instead.
.. seealso:: layersWillBeRemoved()
.. seealso:: layerRemoved()
%End

    void layerWillBeRemoved( QgsMapLayer *layer );
%Docstring
 Emitted when a layer is about to be removed from the store.

 \param layer The layer to be removed.

.. note::

   Consider using layersWillBeRemoved() instead.
.. seealso:: layersWillBeRemoved()
.. seealso:: layerRemoved()
%End

    void layersRemoved( const QStringList &layerIds );
%Docstring
 Emitted after one or more layers were removed from the store.

 \param layerIds  A list of IDs of the layers which were removed.
.. seealso:: layersWillBeRemoved()
%End

    void layerRemoved( const QString &layerId );
%Docstring
 Emitted after a layer was removed from the store.

 \param layerId The ID of the layer removed.

.. note::

   Consider using layersRemoved() instead
.. seealso:: layerWillBeRemoved()
%End

    void allLayersRemoved();
%Docstring
 Emitted when all layers are removed, before layersWillBeRemoved() and
 layerWillBeRemoved() signals are emitted. The layersWillBeRemoved() and
 layerWillBeRemoved() signals will still be emitted following this signal.
 You can use this signal to do easy (and fast) cleanup.
%End

    void layersAdded( const QList<QgsMapLayer *> &layers );
%Docstring
 Emitted when one or more layers were added to the store.

 \param layers List of layers which have been added.

.. seealso:: legendLayersAdded()
.. seealso:: layerWasAdded()
%End

    void layerWasAdded( QgsMapLayer *layer );
%Docstring
 Emitted when a ``layer`` was added to the store.

.. note::

   Consider using layersAdded() instead
.. seealso:: layersAdded()
%End

};

/************************************************************************
 * This file has been generated automatically from                      *
 *                                                                      *
 * src/core/qgsmaplayerstore.h                                          *
 *                                                                      *
 * Do not edit manually ! Edit header and run scripts/sipify.pl again   *
 ************************************************************************/
