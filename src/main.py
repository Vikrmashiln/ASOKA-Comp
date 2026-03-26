import sys
from PySide6 import QtWidgets
from NodeGraphQt import NodeGraph, BaseNode

# --- 1. The Input Node (Read) ---
class ReadNode(BaseNode):
    __identifier__ = 'asoka.nodes'
    NODE_NAME = 'Read'

    def __init__(self):
        super(ReadNode, self).__init__()
        self.add_output('out')
        self.set_color(40, 150, 40) # Green

# --- 2. The Process Node (Reformat) ---
class ReformatNode(BaseNode):
    __identifier__ = 'asoka.nodes'
    NODE_NAME = 'Reformat'

    def __init__(self):
        super(ReformatNode, self).__init__()
        # Input and Output pipes
        self.add_input('in')
        self.add_output('out')
        
        # Add basic attributes for resolution
        self.add_text_input('width', 'Width', text='1920')
        self.add_text_input('height', 'Height', text='1080')
        self.set_color(150, 40, 40) # Red

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    graph = NodeGraph()

    # Register both nodes
    graph.register_node(ReadNode)
    graph.register_node(ReformatNode)

    graph_widget = graph.widget
    graph_widget.resize(1200, 800)
    graph_widget.setWindowTitle("ASOKA - Alpha 0.1")
    graph_widget.show()

    # Create one of each to start
    n_read = graph.create_node('asoka.nodes.ReadNode', name='Read_01', pos=[0, 0])
    n_reformat = graph.create_node('asoka.nodes.ReformatNode', name='Reformat_01', pos=[250, 0])

    sys.exit(app.exec())