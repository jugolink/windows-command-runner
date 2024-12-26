import os
import shutil
import subprocess
from pathlib import Path

def clean_build():
    """清理构建文件"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    
    # 清理 .spec 文件
    for spec_file in Path('.').glob('*.spec'):
        os.remove(spec_file)

def build_exe():
    """构建可执行文件"""
    try:
        # 确保在项目根目录
        project_root = Path(__file__).parent.parent
        os.chdir(project_root)
        
        # 清理旧的构建文件
        clean_build()
        
        # 构建命令
        cmd = [
            'pyinstaller',
            '--noconfirm',
            '--onefile',
            '--windowed',
            '--icon', 'resource/logo.ico',
            '--name', 'windows-command-runner',
            '--add-data', 'resource;resource/',
            '--add-data', 'commands.json;.',
            'src/main.py'
        ]
        
        # 执行构建
        subprocess.run(cmd, check=True)
        
        print("构建成功！可执行文件位于 dist/windows-command-runner.exe")
        
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    build_exe() 