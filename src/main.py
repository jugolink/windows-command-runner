import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QListWidget, QListWidgetItem, QPushButton, QHBoxLayout,
                            QLabel, QMessageBox, QDialog, QLineEdit, QFormLayout)
from PyQt6.QtCore import Qt
from command_controller import CommandController
from PyQt6.QtGui import QIcon

import resource_rc

class AddCommandDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("添加命令")
        self.setModal(True)
        
        layout = QFormLayout(self)
        
        # 创建输入框
        self.name_input = QLineEdit()
        self.command_input = QLineEdit()
        self.description_input = QLineEdit()
        
        layout.addRow("命令名称:", self.name_input)
        layout.addRow("执行命令:", self.command_input)
        layout.addRow("命令描述:", self.description_input)
        
        # 创建按钮
        button_layout = QHBoxLayout()
        
        ok_button = QPushButton("确定")
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)
        
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addRow(button_layout)
    
    def get_command_info(self):
        return (
            self.name_input.text().strip(),
            self.command_input.text().strip(),
            self.description_input.text().strip()
        )

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Windows 命令执行器")
        self.setFixedSize(400, 500)
        
        # 创建主窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 添加说明标签
        description = QLabel("双击命令即可执行，或选中后点击执行按钮")
        description.setWordWrap(True)
        layout.addWidget(description)
        
        # 创建命令列表
        self.command_list = QListWidget()
        self.command_list.itemDoubleClicked.connect(self.execute_selected_command)
        layout.addWidget(self.command_list)
        
        # 创建按钮
        button_layout = QHBoxLayout()
        
        self.execute_btn = QPushButton("执行")
        self.execute_btn.clicked.connect(self.execute_selected_command)
        button_layout.addWidget(self.execute_btn)
        
        self.add_btn = QPushButton("添加")
        self.add_btn.clicked.connect(self.show_add_dialog)
        button_layout.addWidget(self.add_btn)
        
        self.remove_btn = QPushButton("删除")
        self.remove_btn.clicked.connect(self.remove_selected_command)
        button_layout.addWidget(self.remove_btn)
        
        layout.addLayout(button_layout)
        
        # 初始化命令控制器
        self.command_controller = CommandController()
        
        # 加载命令列表
        self.load_commands()
    
    def load_commands(self):
        """加载命令列表"""
        self.command_list.clear()
        
        for name, description in self.command_controller.get_commands():
            item = QListWidgetItem(f"{name} - {description}")
            item.setData(Qt.ItemDataRole.UserRole, name)
            self.command_list.addItem(item)
    
    def show_add_dialog(self):
        """显示添加命令对话框"""
        dialog = AddCommandDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name, command, description = dialog.get_command_info()
            if name and command:
                if self.command_controller.add_command(name, command, description):
                    self.load_commands()
                    self.statusBar().showMessage("命令添加成功", 2000)
                else:
                    QMessageBox.critical(self, "错误", "添加命令失败")
    
    def remove_selected_command(self):
        """删除选中的命令"""
        item = self.command_list.currentItem()
        if item is None:
            QMessageBox.warning(self, "警告", "请先选择一个命令")
            return
            
        command_name = item.data(Qt.ItemDataRole.UserRole)
        reply = QMessageBox.question(
            self,
            "确认删除",
            f"确定要删除命令 '{command_name}' 吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.command_controller.remove_command(command_name):
                self.load_commands()
                self.statusBar().showMessage("命令删除成功", 2000)
            else:
                QMessageBox.critical(self, "错误", "删除命令失败")
    
    def execute_selected_command(self, item=None):
        """执行选中的命令"""
        if item is None:
            item = self.command_list.currentItem()
            
        if item is None:
            QMessageBox.warning(self, "警告", "请先选择一个命令")
            return
            
        command_name = item.data(Qt.ItemDataRole.UserRole)
        if self.command_controller.execute_command(command_name):
            self.statusBar().showMessage(f"正在执行: {command_name}", 2000)
        else:
            QMessageBox.critical(self, "错误", f"执行命令失败: {command_name}")

def main():
    app = QApplication(sys.argv)

    # 设置应用图标
    app_icon = QIcon(":/logo")
    app.setWindowIcon(app_icon)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 