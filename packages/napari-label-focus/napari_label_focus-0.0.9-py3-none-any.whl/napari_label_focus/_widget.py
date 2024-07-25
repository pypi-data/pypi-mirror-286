import napari.layers
from qtpy.QtWidgets import QComboBox, QGridLayout, QWidget

import napari.layers

from ._table import Table

class TableWidget(QWidget):
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        self.labels_layer = None

        self.setLayout(QGridLayout())
        self.cb = QComboBox()
        self.cb.currentTextChanged.connect(self._on_cb_change)
        self.layout().addWidget(self.cb, 0, 0)

        self.table = Table(viewer=self.viewer)
        self.layout().addWidget(self.table, 1, 0)

        self.viewer.layers.events.inserted.connect(
            lambda e: e.value.events.name.connect(self._on_layer_change)
        )
        self.viewer.layers.events.inserted.connect(self._on_layer_change)
        self.viewer.layers.events.removed.connect(self._on_layer_change)
        self._on_layer_change(None)

    def _on_layer_change(self, e):
        self.cb.clear()
        for x in self.viewer.layers:
            if isinstance(x, napari.layers.Labels):
                if len(x.data.shape) in [2, 3, 4]:  # Only 2D-4D data are supported.
                    self.cb.addItem(x.name, x.data)

    def _on_cb_change(self, selection: str):
        if selection == '':
            self.table.update_content(None)
            return
        
        selected_layer = self.viewer.layers[selection]
        if not isinstance(selected_layer, napari.layers.Labels):
            return
        
        if self.labels_layer is not None:
            # self.labels_layer.events.labels_update.disconnect(lambda _: self.table.update_content(self.labels_layer))
            self.labels_layer.events.paint.disconnect(lambda _: self.table.update_content(self.labels_layer))
            self.labels_layer.events.data.disconnect(lambda _: self.table.update_content(self.labels_layer))
        
        # Updating live as pixels are drawn is too expensive (labels_update)
        # selected_layer.events.labels_update.connect(lambda _: self.table.update_content(selected_layer))
        
        # Not sure what this does - it's probably useful
        selected_layer.events.data.connect(lambda _: self.table.update_content(selected_layer))
        
        # Instead we update the table only when the mouse is up after drawing.
        selected_layer.events.paint.connect(lambda _: self.table.update_content(selected_layer))

        # Temporary
        if selected_layer.data.ndim == 4:
            self.viewer.dims.events.current_step.connect(lambda e: self.table.handle_time_axis_changed(e, selected_layer))

        self.labels_layer = selected_layer

        self.table.update_content(selected_layer)
