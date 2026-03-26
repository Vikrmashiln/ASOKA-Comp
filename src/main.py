import sys
import os
import cv2 # This is our "Eyes"
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

# --- 2. THE VIEWER NODE (NEW!) ---
class ViewerNode(BaseNode):
    __identifier__ = 'asoka.nodes'
    NODE_NAME = 'Viewer'
    def __init__(self):
        super(ViewerNode, self).__init__()
        self.add_input('in')
        self.set_color(150, 40, 150) # Purple

    def show_result(self, graph, node):
        # 1. Trace back to the Read node to get the path
        input_port = self.input(0)
        connected_ports = input_port.connected_ports()
        
        if not connected_ports:
            print("ASOKA: Nothing connected to Viewer!")
            return

        source_node = connected_ports[0].node()
        path = source_node.get_property('file_path')

        if path and os.path.exists(path):
            # 2. Use OpenCV to show the image
            img = cv2.imread(path)
            cv2.imshow("ASOKA VIEW - " + os.path.basename(path), img)
            cv2.waitKey(1) # Keeps the window alive
        else:
            print("ASOKA: No image found at path!")

# --- 3. THE BLUR NODE ---
class BlurNode(BaseNode):
    __identifier__ = 'asoka.nodes'
    NODE_NAME = 'Blur'
    def __init__(self):
        super(BlurNode, self).__init__()
        self.add_input('in')
        self.add_output('out')
        self.add_text_input('blur_val', 'Size', text='5')
        self.set_color(40, 70, 150)

# --- 4. THE GLOBAL MENU FUNCTION ---
def open_browser(graph, node):
    file_path, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select Image", "", "Images (*.jpg *.png *.exr)")
    if file_path:
        node.set_property('file_path', file_path)

def trigger_viewer(graph, node):
    node.show_result(graph, node)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    graph = NodeGraph()
    
    graph.register_node(ReadNode)
    graph.register_node(BlurNode)
    graph.register_node(ViewerNode)

    # ADD MENU COMMANDS
    nodes_menu = graph.get_context_menu('nodes')
    nodes_menu.add_command('Load Image File...', open_browser, node_type='asoka.nodes.ReadNode')
    nodes_menu.add_command('Show Image', trigger_viewer, node_type='asoka.nodes.ViewerNode')

    graph_widget = graph.widget
    graph_widget.resize(1100, 800)
    graph_widget.show()

    # CREATE PIPELINE
    n_read = graph.create_node('asoka.nodes.ReadNode', pos=[-300, 0])
    n_blur = graph.create_node('asoka.nodes.BlurNode', pos=[0, 0])
    n_view = graph.create_node('asoka.nodes.ViewerNode', pos=[300, 0])
    
    n_read.set_output(0, n_blur.input(0))
    n_blur.set_output(0, n_view.input(0))

    sys.exit(app.exec())