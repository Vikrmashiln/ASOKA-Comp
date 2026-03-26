import sys
from PySide6 import QtWidgets
from NodeGraphQt import NodeGraph, BaseNode

class ReadNode(BaseNode):
    __identifier__ = 'asoka.nodes'
    NODE_NAME = 'Read'
    def __init__(self):
        super(ReadNode, self).__init__()
        self.add_output('out')
        self.set_color(40, 150, 40)

class ReformatNode(BaseNode):
    __identifier__ = 'asoka.nodes'
    NODE_NAME = 'Reformat'

    def __init__(self):
        super(ReformatNode, self).__init__()
        self.add_input('in')
        self.add_output('out')
        
        # We changed 'width' to 'res_w' to avoid the conflict
        self.add_text_input('res_w', 'Width', text='1920')
        self.add_text_input('res_h', 'Height', text='1080')
        
        self.set_color(150, 40, 40)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    graph = NodeGraph()

    graph.register_node(ReadNode)
    graph.register_node(ReformatNode)

    graph_widget = graph.widget
    graph_widget.resize(1100, 800)
    graph_widget.setWindowTitle("ASOKA - Stable Build")
    graph_widget.show()

    graph.create_node('asoka.nodes.ReadNode', name='Read_01', pos=[0, 0])
    graph.create_node('asoka.nodes.ReformatNode', name='Reformat_01', pos=[250, 0])

    sys.exit(app.exec())