import sys
from PySide6 import QtWidgets
from NodeGraphQt import NodeGraph, BaseNode

# --- 1. THE INPUT (READ) ---
class ReadNode(BaseNode):
    __identifier__ = 'asoka.nodes'
    NODE_NAME = 'Read'
    def __init__(self):
        super(ReadNode, self).__init__()
        self.add_output('out')
        self.add_text_input('file_path', 'File Path', text='C:/vfx/plate.exr')
        self.set_color(40, 150, 40) # Green

# --- 2. THE EDIT (BLUR) ---
class BlurNode(BaseNode):
    __identifier__ = 'asoka.nodes'
    NODE_NAME = 'Blur'
    def __init__(self):
        super(BlurNode, self).__init__()
        self.add_input('in')
        self.add_output('out')
        # We use 'blur_size' to avoid reserved words
        self.add_text_input('blur_val', 'Size', text='5')
        self.set_color(40, 70, 150) # Blue

# --- 3. THE GENERATE (WRITE) ---
class WriteNode(BaseNode):
    __identifier__ = 'asoka.nodes'
    NODE_NAME = 'Write'
    def __init__(self):
        super(WriteNode, self).__init__()
        self.add_input('in')
        self.add_text_input('export_path', 'Export To', text='C:/vfx/render.png')
        self.set_color(150, 150, 40) # Yellow/Gold

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    graph = NodeGraph()

    # Register our new ASOKA "Lego Blocks"
    graph.register_node(ReadNode)
    graph.register_node(BlurNode)
    graph.register_node(WriteNode)

    graph_widget = graph.widget
    graph_widget.resize(1100, 800)
    graph_widget.setWindowTitle("ASOKA - Input/Edit/Generate Pipeline")
    graph_widget.show()

    # Auto-layout a basic script
    n_read = graph.create_node('asoka.nodes.ReadNode', pos=[-300, 0])
    n_blur = graph.create_node('asoka.nodes.BlurNode', pos=[0, 0])
    n_write = graph.create_node('asoka.nodes.WriteNode', pos=[300, 0])
    
    # Connect them automatically!
    n_read.set_output(0, n_blur.input(0))
    n_blur.set_output(0, n_write.input(0))

    sys.exit(app.exec())