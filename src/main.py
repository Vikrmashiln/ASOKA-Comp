import sys
from PySide6 import QtWidgets, QtCore
from NodeGraphQt import NodeGraph, BaseNode, NodeBaseWidget

# --- 1. CUSTOM BROWSE WIDGET ---
# --- FIXED: The Custom Button Widget ---
class BrowseFileWidget(NodeBaseWidget):
    def __init__(self, parent=None):
        super(BrowseFileWidget, self).__init__(parent, name='Browse', label='File')
        self.set_custom_widget(QtWidgets.QPushButton('Browse...'))
        self.get_custom_widget().clicked.connect(self.on_browse)

    def on_browse(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            None, "ASOKA: Select Plate", "", "Images (*.exr *.jpg *.png *.tiff)"
        )
        if file_path:
            self.node.set_property('file_path', file_path)
            print(f"ASOKA: Linked -> {file_path}")

    # --- ADD THESE TWO LINES TO FIX THE ERROR ---
    def get_value(self):
        return None  # The button itself doesn't have a value

    def set_value(self, value):
        pass  # We don't need to set a value on a button

# --- 2. READ NODE ---
class ReadNode(BaseNode):
    __identifier__ = 'asoka.nodes'
    NODE_NAME = 'Read'
    def __init__(self):
        super(ReadNode, self).__init__()
        self.add_output('out')
        self.add_text_input('file_path', 'File Path', text='')
        self.add_custom_widget(BrowseFileWidget())
        self.set_color(40, 150, 40)

# --- 3. BLUR NODE ---
class BlurNode(BaseNode):
    __identifier__ = 'asoka.nodes'
    NODE_NAME = 'Blur'
    def __init__(self):
        super(BlurNode, self).__init__()
        self.add_input('in')
        self.add_output('out')
        self.add_text_input('blur_val', 'Size', text='5')
        self.set_color(40, 70, 150)

# --- 4. WRITE NODE ---
class WriteNode(BaseNode):
    __identifier__ = 'asoka.nodes'
    NODE_NAME = 'Write'
    def __init__(self):
        super(WriteNode, self).__init__()
        self.add_input('in')
        self.add_text_input('export_path', 'Export To', text='C:/ASOKA_Renders/output.png')
        self.set_color(150, 150, 40)

# --- MAIN APP ---
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    
    # Create the graph
    graph = NodeGraph()

    # Register nodes
    graph.register_node(ReadNode)
    graph.register_node(BlurNode)
    graph.register_node(WriteNode)

    # Show UI
    graph_widget = graph.widget
    graph_widget.resize(1100, 800)
    graph_widget.setWindowTitle("ASOKA - Studio Build")
    graph_widget.show()

    # Create & Connect
    n_read = graph.create_node('asoka.nodes.ReadNode', pos=[-300, 0])
    n_blur = graph.create_node('asoka.nodes.BlurNode', pos=[0, 0])
    n_write = graph.create_node('asoka.nodes.WriteNode', pos=[300, 0])
    
    n_read.set_output(0, n_blur.input(0))
    n_blur.set_output(0, n_write.input(0))

    sys.exit(app.exec())