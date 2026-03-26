import sys
import os
import cv2
import torch
import kornia
import numpy as np
from PySide6 import QtWidgets, QtCore
from NodeGraphQt import NodeGraph, BaseNode

# --- 1. THE READ NODE ---
class ReadNode(BaseNode):
    __identifier__ = 'asoka.nodes'
    NODE_NAME = 'Read'
    def __init__(self):
        super(ReadNode, self).__init__()
        self.add_output('out')
        self.add_text_input('file_path', 'Path', text='')
        self.set_color(40, 150, 40)

# --- 2. THE BLUR NODE (NOW POWERED BY KORNIA) ---
class BlurNode(BaseNode):
    __identifier__ = 'asoka.nodes'
    NODE_NAME = 'Blur'
    def __init__(self):
        super(BlurNode, self).__init__()
        self.add_input('in')
        self.add_output('out')
        self.add_text_input('blur_val', 'Size', text='15')
        self.set_color(40, 70, 150)

    def process_image(self, image_path):
        # 1. Load image via OpenCV
        img = cv2.imread(image_path)
        if img is None: return None
        
        # 2. Convert to Tensor (The Kornia Way)
        # We move it to RGB and then to a Tensor
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        tensor = kornia.utils.image_to_tensor(img_rgb).float() / 255.0
        tensor = tensor.unsqueeze(0) # Add batch dimension [1, C, H, W]

        # 3. Apply Kornia Gaussian Blur
        size = int(self.get_property('blur_val'))
        # Kernel size must be odd
        k_size = size if size % 2 != 0 else size + 1
        blurred_tensor = kornia.filters.gaussian_blur2d(tensor, (k_size, k_size), (1.5, 1.5))

        # 4. Convert back to OpenCV format for viewing
        blurred_img = kornia.utils.tensor_to_image(blurred_tensor.squeeze(0))
        blurred_img = (blurred_img * 255).astype(np.uint8)
        return cv2.cvtColor(blurred_img, cv2.COLOR_RGB2BGR)

# --- 3. THE VIEWER NODE ---
class ViewerNode(BaseNode):
    __identifier__ = 'asoka.nodes'
    NODE_NAME = 'Viewer'
    def __init__(self):
        super(ViewerNode, self).__init__()
        self.add_input('in')
        self.set_color(150, 40, 150)

    def show_result(self):
        # Find the path from the Read node through the pipe
        try:
            blur_node = self.input(0).connected_ports()[0].node()
            read_node = blur_node.input(0).connected_ports()[0].node()
            path = read_node.get_property('file_path')
            
            if path and os.path.exists(path):
                # Run the Blur processing!
                final_img = blur_node.process_image(path)
                cv2.imshow("ASOKA GPU VIEW", final_img)
                cv2.waitKey(1)
            else:
                print("ASOKA: No file path found!")
        except Exception as e:
            print(f"ASOKA PIPE ERROR: {e}")

# --- GLOBAL FUNCTIONS & UI START ---
def open_browser(graph, node):
    file_path, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select Image", "", "Images (*.jpg *.png *.exr)")
    if file_path: node.set_property('file_path', file_path)

def trigger_viewer(graph, node):
    node.show_result()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    graph = NodeGraph()
    graph.register_node(ReadNode)
    graph.register_node(BlurNode)
    graph.register_node(ViewerNode)

    nodes_menu = graph.get_context_menu('nodes')
    nodes_menu.add_command('Load Image File...', open_browser, node_type='asoka.nodes.ReadNode')
    nodes_menu.add_command('Show Result', trigger_viewer, node_type='asoka.nodes.ViewerNode')

    graph_widget = graph.widget
    graph_widget.resize(1100, 800)
    graph_widget.show()

    # Create & Connect
    n_read = graph.create_node('asoka.nodes.ReadNode', pos=[-300, 0])
    n_blur = graph.create_node('asoka.nodes.BlurNode', pos=[0, 0])
    n_view = graph.create_node('asoka.nodes.ViewerNode', pos=[300, 0])
    n_read.set_output(0, n_blur.input(0))
    n_blur.set_output(0, n_view.input(0))

    sys.exit(app.exec())