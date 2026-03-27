import sys
from NodeGraphQt import NodeGraph, BaseNode
from PySide6 import QtWidgets, QtCore

app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)


class ViewerNode(BaseNode):
    __identifier__ = 'asoka.core'
    NODE_NAME = 'ViewerNode'

    def __init__(self):
        super().__init__()
        self.add_input('Input')
        self.set_color(30, 100, 150)


class ViewerPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #1a1a1a;")
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        title = QtWidgets.QLabel("VIEWER")
        title.setStyleSheet("color: #888888; font-size: 13px; font-family: monospace; padding: 6px;")
        layout.addWidget(title)

        self.screen = QtWidgets.QLabel("[ No Input ]")
        self.screen.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.screen.setStyleSheet("color: #444444; font-size: 12px;")
        layout.addWidget(self.screen)


class PropertiesPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(240)
        self.setStyleSheet("background-color: #1e1e1e;")
        layout = QtWidgets.QVBoxLayout(self)

        title = QtWidgets.QLabel("PROPERTIES")
        title.setStyleSheet("color: #888888; font-size: 13px; font-family: monospace; padding: 6px;")
        layout.addWidget(title)

        self.info = QtWidgets.QLabel("Select a node\nto view properties.")
        self.info.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.info.setStyleSheet("color: #555555; font-size: 11px; padding: 8px;")
        layout.addWidget(self.info)
        layout.addStretch()


class CurveEditor(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #1a1a1a;")
        layout = QtWidgets.QVBoxLayout(self)
        label = QtWidgets.QLabel("Curve Editor — Coming Soon")
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: #444444; font-size: 12px; font-family: monospace;")
        layout.addWidget(label)


class DataSheet(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #1a1a1a;")
        layout = QtWidgets.QVBoxLayout(self)

        self.table = QtWidgets.QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Node", "Type", "Status"])
        self.table.setStyleSheet("""
            QTableWidget { background-color: #1a1a1a; color: #aaaaaa; gridline-color: #333333; font-size: 11px; }
            QHeaderView::section { background-color: #252525; color: #888888; padding: 4px; border: none; }
        """)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)


class NodeGraphPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #1a1a1a;")
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: none; background: #1a1a1a; }
            QTabBar::tab { background: #252525; color: #888888; padding: 6px 16px; font-size: 11px; font-family: monospace; border: none; }
            QTabBar::tab:selected { background: #1a1a1a; color: #cccccc; border-top: 2px solid #4a90d9; }
            QTabBar::tab:hover { background: #2a2a2a; color: #aaaaaa; }
        """)

        self.graph = NodeGraph()
        self.graph.register_node(ViewerNode)
        viewer_node = self.graph.create_node('asoka.core.ViewerNode', name='Viewer', pos=[0, 0])
        self.tabs.addTab(self.graph.widget, "  Node Graph  ")

        self.curve_editor = CurveEditor()
        self.tabs.addTab(self.curve_editor, "  Curve Editor  ")

        self.data_sheet = DataSheet()
        self.tabs.addTab(self.data_sheet, "  Data Sheet  ")

        layout.addWidget(self.tabs)


class ASOKAWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ASOKA-Comp  v0.1")
        self.setMinimumSize(1280, 720)
        self.setStyleSheet("background-color: #1a1a1a;")

        self._build_menu()

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        main_layout = QtWidgets.QHBoxLayout(central)
        main_layout.setContentsMargins(4, 4, 4, 4)
        main_layout.setSpacing(4)

        left_split = QtWidgets.QSplitter(QtCore.Qt.Orientation.Vertical)

        self.viewer = ViewerPanel()
        left_split.addWidget(self.viewer)

        self.node_panel = NodeGraphPanel()
        left_split.addWidget(self.node_panel)
        left_split.setSizes([380, 340])

        main_layout.addWidget(left_split, stretch=3)

        self.properties = PropertiesPanel()
        main_layout.addWidget(self.properties, stretch=1)

    def _build_menu(self):
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar { background-color: #252525; color: #aaaaaa; font-size: 12px; padding: 2px; }
            QMenuBar::item:selected { background-color: #333333; color: #ffffff; }
            QMenu { background-color: #252525; color: #aaaaaa; border: 1px solid #333333; }
            QMenu::item:selected { background-color: #3a3a3a; color: #ffffff; }
            QMenu::separator { height: 1px; background: #333333; margin: 4px 0; }
        """)

        file_menu = menubar.addMenu("File")
        file_menu.addAction("New Project")
        file_menu.addAction("Open Project...")
        file_menu.addSeparator()
        file_menu.addAction("Save")
        file_menu.addAction("Save As...")
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)

        edit_menu = menubar.addMenu("Edit")
        edit_menu.addAction("Undo")
        edit_menu.addAction("Redo")
        edit_menu.addSeparator()
        edit_menu.addAction("Cut")
        edit_menu.addAction("Copy")
        edit_menu.addAction("Paste")
        edit_menu.addSeparator()
        edit_menu.addAction("Preferences...")

        workspace_menu = menubar.addMenu("Workspace")
        workspace_menu.addAction("Reset Layout")
        workspace_menu.addAction("Save Layout")
        workspace_menu.addSeparator()
        workspace_menu.addAction("Compositing")
        workspace_menu.addAction("Grading")
        workspace_menu.addAction("Roto")

        viewer_menu = menubar.addMenu("Viewer")
        viewer_menu.addAction("Fit Image")
        viewer_menu.addAction("Zoom In")
        viewer_menu.addAction("Zoom Out")
        viewer_menu.addSeparator()
        viewer_menu.addAction("Show RGBA")
        viewer_menu.addAction("Show Alpha")
        viewer_menu.addAction("Show Luminance")
        viewer_menu.addSeparator()
        viewer_menu.addAction("Toggle Exposure Controls")

        render_menu = menubar.addMenu("Render")
        render_menu.addAction("Render Current Frame")
        render_menu.addAction("Render Sequence...")
        render_menu.addSeparator()
        render_menu.addAction("Render Settings...")
        render_menu.addAction("AWS Cloud Render...")

        cache_menu = menubar.addMenu("Cache")
        cache_menu.addAction("Clear Viewer Cache")
        cache_menu.addAction("Clear All Cache")
        cache_menu.addSeparator()
        cache_menu.addAction("Cache Settings...")

        help_menu = menubar.addMenu("Help")
        help_menu.addAction("Documentation")
        help_menu.addAction("GitHub Repository")
        help_menu.addSeparator()
        help_menu.addAction("About ASOKA")


window = ASOKAWindow()
window.show()
window.raise_()

app.exec()