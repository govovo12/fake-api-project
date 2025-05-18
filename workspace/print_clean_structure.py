# print_clean_structure.py
import os

EXCLUDED_DIRS = {
    'venv', '__pycache__', '.git', '.pytest_cache', '.mypy_cache', 'node_modules'
}

def print_structure(root_path, indent=""):
    for item in sorted(os.listdir(root_path)):
        full_path = os.path.join(root_path, item)
        if os.path.isdir(full_path):
            if item in EXCLUDED_DIRS:
                continue
            print(f"{indent}{item}/")
            print_structure(full_path, indent + "    ")
        else:
            print(f"{indent}{item}")

if __name__ == "__main__":
    # 🔧 修正：從 workspace 往上層找，抓 fake-api-project 根目錄
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    print("=== 專案資料夾結構清單（已排除常見雜項）===\n")
    print_structure(root_dir)