import argparse
import sys
from pathlib import Path

# 引入你的 paths.py 裡的 PROJECT_ROOT
from workspace.config.paths import PROJECT_ROOT

def main():
    parser = argparse.ArgumentParser(description="Fake-API 任務入口")
    parser.add_argument("--folder", type=str, required=True, help="請指定任務資料夾名稱（如 controller、tasks）")
    parser.add_argument("--task", type=str, required=True, help="請指定要執行的任務模組名稱（不含 .py）")
    args = parser.parse_args()
    folder = args.folder
    task_name = args.task

    # 路徑正確指到 workspace/底下對應資料夾
    task_module_path = PROJECT_ROOT / "workspace" / folder / f"{task_name}.py"

    if not task_module_path.exists():
        print(f"找不到任務模組：{task_module_path}")
        sys.exit(1)

    # 動態 import 該任務模組
    import importlib.util

    spec = importlib.util.spec_from_file_location(task_name, task_module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # 檢查是否有 __task_info__ 並且有 entry function
    if hasattr(module, "__task_info__") and "entry" in module.__task_info__:
        entry_func = module.__task_info__["entry"]
        if callable(entry_func):
            entry_func()
        else:
            print(f"模組 {task_name} 的 __task_info__['entry'] 不是 callable。")
            sys.exit(1)
    else:
        print(f"模組 {task_name} 缺少 __task_info__ 或 entry。")
        sys.exit(1)

if __name__ == "__main__":
    main()
