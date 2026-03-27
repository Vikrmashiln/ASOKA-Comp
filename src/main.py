import sys
import os
import cv2
import torch
import kornia
import numpy as np
from PySide6 import QtWidgets, QtCore, QtGui
from NodeGraphQt import NodeGraph, BaseNode, PropertiesBinWidget

# --- 1. THE NODES ---

class ReadNode(BaseNode):
    __identifier__ = 'asoka.nodes'
    NODE_NAME = 'Read'
    def __init__(self):
        super(ReadNode, self).__init__()
        self.add_output('out')
        self.add_text_input('file_path', 'Path', text='')
        self.set_color(40, 150, 40)
        self.set_property('width', 250)

class BlurNode(BaseNode):
    __identifier__ = 'asoka.nodes'
    NODE_NAME = 'Blur'
    def __init__(self):
        super(BlurNode, self).__init__()
        self.add_input('in')
        self.add_output('out')
        self.add_text_input('blur_val', 'Size', text='25')
        self.set_color(40, 70, 150)

    def process_image(self, path):
        img = cv2.imread(path)
        if img is None: return None
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        tensor = kornia.utils.image_to_tensor(img_rgb).float() / 255.0
        tensor = tensor.unsqueeze(0)
        val = int(self.get_property('blur_val'))
        k_size = val if val % 2 != 0 else val + 1
        blurred = kornia.filters.gaussian_blur2d(tensor, (k_size, k_size), (1.5, 1.5))
        out = kornia.utils.tensor_to_image(blurred.squeeze(0))
        out = (out * 255).astype(np.uint8)
        return cv2.cvtColor(out, cv2.COLOR_RGB2BGR)

class WriteNode(BaseNode):
    __identifier__ = 'asoka.nodes'
    NODE_NAME = 'Write'
    def __init__(self):
        super(WriteNode, self).__init__()
        self.add_input('in')
        self.add_text_input('export_path', 'Export Path', text='C:/ASOKA_Renders/output.png')
        self.set_color(150, 150, 40)
        self.set_property('width', 250)

class ViewerNode(BaseNode):
    __identifier__ = 'asoka.nodes'
    NODE_NAME = 'Viewer'
    def __init__(self):
        super(ViewerNode, self).__init__()
        self.add_input('in')
        self.set_color(150, 40, 150)

# --- 2. UI CLASSES (VIEWER & STUDIO) ---

class InteractiveView(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScene(QtWidgets.QGraphicsScene(self))
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(25, 25, 25)))
        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self._pixmap_item = None

    def set_image(self, pixmap):
        self.scene().clear()
        self._pixmap_item = self.scene().addPixmap(pixmap)
        self.setSceneRect(QtCore.QRectF(pixmap.rect()))
        self.fitInView(self.sceneRect(), QtCore.Qt.KeepAspectRatio)

    def wheelEvent(self, event):
        zoom_in = 1.25
        zoom_out = 1 / zoom_in
        if event.angleDelta().y() > 0:
            self.scale(zoom_in, zoom_in)
        else:
            self.scale(zoom_out, zoom_out)

class AsokaStudio(QtWidgets.QMainWindow):
    def __init__(self, graph):
        super().__init__()
        self.setWindowTitle("ASOKA STUDIO - NukeX Interactive Build")
        self.resize(1600, 900)
        self.h_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.setCentralWidget(self.h_splitter)
        self.v_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.h_splitter.addWidget(self.v_splitter)
        self.viewer_display = InteractiveView()
        self.v_splitter.addWidget(self.viewer_display)
        self.v_splitter.addWidget(graph.widget)
        self.prop_bin = PropertiesBinWidget(node_graph=graph)
        self.h_splitter.addWidget(self.prop_bin)
        self.v_splitter.setSizes([500, 400])
        self.h_splitter.setSizes([1100, 500])

    def update_viewer(self, cv_img):
        height, width, channel = cv_img.shape
        bytes_per_line = 3 * width
        q_img = QtGui.QImage(cv_img.data, width, height, bytes_per_line, QtGui.QImage.Format_BGR888)
        pixmap = QtGui.QPixmap.fromImage(q_img)
        self.viewer_display.set_image(pixmap)

# --- 3. GLOBAL FUNCTIONS ---

def open_file(graph, node):
    path, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select Image", "", "Images (*.jpg *.png *.exr)")
    if path:
        node.set_property('file_path', path)

def run_view(graph, node):
    try:
        ports = node.input(0).connected_ports()
        if not ports: return
        blur = ports[0].node()
        read_ports = blur.input(0).connected_ports()
        if not read_ports: return
        path = read_ports[0].node().get_property('file_path')
        if path and os.path.exists(path):
            res = blur.process_image(path)
            main_window.update_viewer(res)
    except Exception as e: print(f"VIEW ERROR: {e}")

# --- 4. STARTUP LOGIC ---

# --- 3. GLOBAL FUNCTIONS ---

def open_file(graph, node):
    path, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select Image", "", "Images (*.jpg *.png *.exr)")
    if path:
        node.set_property('file_path', path)

def run_view(graph, node):
    try:
        ports = node.input(0).connected_ports()
        if not ports: return
        blur = ports[0].node()
        read_ports = blur.input(0).connected_ports()
        if not read_ports: return
        path = read_ports[0].node().get_property('file_path')
        if path and os.path.exists(path):
            res = blur.process_image(path)
            main_window.update_viewer(res)
    except Exception as e: print(f"VIEW ERROR: {e}")

# NEW: Function to handle the double-click
def on_node_double_clicked(node):
    main_window.prop_bin.set_node(node)

# --- 4. STARTUP LOGIC ---

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    graph = NodeGraph()
    
    graph.register_node(ReadNode)
    graph.register_node(BlurNode)
    graph.register_node(WriteNode)
    graph.register_node(ViewerNode)

    main_window = AsokaStudio(graph)

    # --- THE MAGIC LINK ---
    # This connects the double-click event to our function
    graph.node_double_clicked.connect(on_node_double_clicked)

    m = graph.get_context_menu('nodes')
    m.add_command('Load Image...', open_file, node_type='asoka.nodes.ReadNode')
    m.add_command('Show Image', run_view, node_type='asoka.nodes.ViewerNode')

    main_window.show()

    n1 = graph.create_node('asoka.nodes.ReadNode', pos=[-600, 0])
    n2 = graph.create_node('asoka.nodes.BlurNode', pos=[-200, 0])
    n3 = graph.create_node('asoka.nodes.ViewerNode', pos=[200, 0])
    n1.set_output(0, n2.input(0))
    n2.set_output(0, n3.input(0))

    sys.exit(app.exec())