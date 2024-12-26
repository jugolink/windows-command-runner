import os
import json
import pytest
from src.command_controller import CommandController

@pytest.fixture
def command_controller():
    # 使用临时配置文件进行测试
    controller = CommandController()
    controller.config_file = "test_commands.json"
    yield controller
    # 清理测试文件
    if os.path.exists(controller.config_file):
        os.remove(controller.config_file)

def test_load_default_commands(command_controller):
    """测试加载默认命令"""
    command_controller._load_default_commands()
    commands = command_controller.get_commands()
    assert len(commands) > 0
    assert any(cmd[0] == "网络连接" for cmd in commands)

def test_save_and_load_commands(command_controller):
    """测试保存和加载命令"""
    # 保存默认命令
    command_controller._load_default_commands()
    assert command_controller.save_commands()
    
    # 清空当前命令
    command_controller._commands.clear()
    
    # 重新加载
    command_controller.load_commands()
    commands = command_controller.get_commands()
    assert len(commands) > 0

def test_add_command(command_controller):
    """测试添加命令"""
    name = "测试命令"
    cmd = "test.exe"
    desc = "测试描述"
    
    assert command_controller.add_command(name, cmd, desc)
    commands = command_controller.get_commands()
    assert any(cmd[0] == name for cmd in commands)

def test_remove_command(command_controller):
    """测试删除命令"""
    name = "测试命令"
    cmd = "test.exe"
    desc = "测试描述"
    
    command_controller.add_command(name, cmd, desc)
    assert command_controller.remove_command(name)
    commands = command_controller.get_commands()
    assert not any(cmd[0] == name for cmd in commands)

def test_validate_commands_data(command_controller):
    """测试命令数据验证"""
    # 有效数据
    valid_data = {
        "测试": ["test.exe", "测试描述"]
    }
    assert command_controller._validate_commands_data(valid_data)
    
    # 无效数据
    invalid_data = {
        "测试": "test.exe"  # 不是列表
    }
    assert not command_controller._validate_commands_data(invalid_data) 