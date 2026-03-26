import sys
from PySide6 import QtWidgets, QtCore
from NodeGraphQt import NodeGraph, BaseNode

# --- 1. Define our first ASOKA Node ---
class ReadNode(BaseNode):
    __identifier__ = 'asoka.nodes'
    NODE_NAME = 'Read'

    def __init__(self):
        super(ReadNode, self).__init__()
        self.add_output('out')
        self.set_color(40, 150, 40) # Green for Input/Read

# --- 2. Setup the Application ---
if __name__ == '__main__':
    # Initialize the App
    app = QtWidgets.QApplication(sys.argv)

    # Create the Node Graph
    graph = NodeGraph()

    # Register our Read node
    graph.register_node(ReadNode)

    # UI Settings
    graph_widget = graph.widget
    graph_widget.resize(1100, 800)
    graph_widget.setWindowTitle("ASOKA - Compositing Without Sorrow")
    graph_widget.show()

    # Auto-create one node to show it works
    graph.create_node('asoka.nodes.ReadNode', name='Read_Plate_01')

    sys.exit(app.exec())