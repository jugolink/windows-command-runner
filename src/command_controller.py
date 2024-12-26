import json
import os
import subprocess
from typing import Dict, List, Tuple

class CommandController:
    def __init__(self):
        self.config_file = "commands.json"
        self._commands: Dict[str, Tuple[str, str]] = {}
        self.load_commands()
    
    def load_commands(self) -> None:
        """从配置文件加载命令，如果文件不存在或无效则创建"""
        try:
            if os.path.exists(self.config_file):
                # 检查文件是否为空
                if os.path.getsize(self.config_file) > 0:
                    with open(self.config_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # 验证数据格式
                        if self._validate_commands_data(data):
                            self._commands = {
                                name: (cmd[0], cmd[1]) 
                                for name, cmd in data.items()
                            }
                            print("已从配置文件加载命令")
                            return
                        else:
                            print("配置文件格式无效")
                else:
                    print("配置文件为空")
            
            # 如果文件不存在、为空或格式无效，使用默认命令
            self._load_default_commands()
            self.save_commands()
            print(f"已创建配置文件: {self.config_file}")
            
        except Exception as e:
            print(f"加载命令失败: {e}")
            self._load_default_commands()
    
    def _load_default_commands(self) -> None:
        """加载默认命令列表"""
        self._commands = {
            "网络连接": ("ncpa.cpl", "打开网络连接设置"),
            "系统属性": ("sysdm.cpl", "打开系统属性"),
            "设备管理器": ("devmgmt.msc", "打开设备管理器"),
            "磁盘管理": ("diskmgmt.msc", "打开磁盘管理"),
            "服务": ("services.msc", "打开服务管理"),
            "任务管理器": ("taskmgr", "打开任务管理器"),
            "控制面板": ("control", "打开控制面板"),
            "注册表编辑器": ("regedit", "打开注册表编辑器"),
            "DirectX诊断工具": ("dxdiag", "打开DirectX诊断工具"),
            "命令提示符": ("cmd", "打开命令提示符"),
            "PowerShell": ("powershell", "打开PowerShell"),
            "计算器": ("calc", "打开计算器"),
            "记事本": ("notepad", "打开记事本"),
            "画图": ("mspaint", "打开画图"),
            "远程桌面": ("mstsc", "打开远程桌面连接"),
            "声音设置": ("mmsys.cpl", "打开声音设置"),
            "Windows防火墙": ("firewall.cpl", "打开Windows防火墙设置"),
            "电源选项": ("powercfg.cpl", "打开电源选项设置"),
            "区域设置": ("intl.cpl", "打开区域设置"),
            "程序和功能": ("appwiz.cpl", "打开程序和功能")
        }
    
    def save_commands(self) -> bool:
        """保存命令到配置文件"""
        try:
            data = {
                name: [cmd, desc] 
                for name, (cmd, desc) in self._commands.items()
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
            
        except Exception as e:
            print(f"保存命令失败: {e}")
            return False
    
    def add_command(self, name: str, command: str, description: str) -> bool:
        """添加新命令"""
        try:
            if not name or not command:
                return False
            
            self._commands[name] = (command, description)
            return self.save_commands()
            
        except Exception as e:
            print(f"添加命令失败: {e}")
            return False
    
    def remove_command(self, name: str) -> bool:
        """删除命令"""
        try:
            if name in self._commands:
                del self._commands[name]
                return self.save_commands()
            return False
            
        except Exception as e:
            print(f"删除命令失败: {e}")
            return False
    
    def get_commands(self) -> List[Tuple[str, str]]:
        """获取所有可用命令及其描述"""
        return [(name, desc) for name, (_, desc) in self._commands.items()]
    
    def execute_command(self, command_name: str) -> bool:
        """执行指定的命令"""
        try:
            if command_name not in self._commands:
                return False
                
            command = self._commands[command_name][0]
            subprocess.Popen(command, shell=True)
            return True
            
        except Exception as e:
            print(f"执行命令失败: {e}")
            return False
    
    def _validate_commands_data(self, data: dict) -> bool:
        """验证命令数据格式是否有效"""
        try:
            if not isinstance(data, dict):
                return False
            
            for name, cmd in data.items():
                if not isinstance(name, str) or not isinstance(cmd, list):
                    return False
                if len(cmd) != 2 or not isinstance(cmd[0], str) or not isinstance(cmd[1], str):
                    return False
            return True
            
        except Exception:
            return False