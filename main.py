import argparse
import importlib.util
import os
import sys
from pathlib import Path
from types import ModuleType

# === 基本參數設定 ===
WORKSPACE_DIR = Path(__file__).parent / "workspace"
DEFAULT_SCAN_DIRS = [
    WORKSPACE_DIR / "scripts",
    WORKSPACE_DIR / "controller",
]

# === 掃描任務模組 ===
def scan_task_modules(scan_dirs):
    task_map = {}
    for directory in scan_dirs:
        for file in directory.rglob("*.py"):
            if file.name.startswith("_"):
                continue
            module_path = file.relative_to(WORKSPACE_DIR).with_suffix("").as_posix().replace("/", ".")
            spec = importlib.util.spec_from_file_location(module_path, file)
            try:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)  # type: ignore
                if hasattr(module, "__task_info__"):
                    task_name = module.__task_info__["task"]
                    task_map[task_name] = {
                        "module_path": module_path,
                        "entry": module.__task_info__.get("entry", "run"),
                        "module": module,
                    }
            except Exception as e:
                print(f"⚠️ 載入失敗：{file}，錯誤：{e}")
    return task_map

# === 執行指定任務 ===
def run_task(task_name, task_map):
    task = task_map.get(task_name)
    if not task:
        print(f"❌ 找不到任務：{task_name}\n")
        print("✅ 可用任務如下：")
        for name, info in task_map.items():
            print(f" - {name}（from {info['module_path']}）")
        return

    module = task["module"]
    entry = getattr(module, task["entry"], None)
    if not entry:
        print(f"❌ 無法在模組中找到對應入口函式：{task['entry']}")
        return

    print(f"📦 載入任務模組：{task['module_path']}")
    print(f"✅ 執行任務：{task_name}（{task['entry']}）")
    print("[DEBUG] 開始執行 run()...\n")
    try:
        entry()
    except Exception as e:
        print(f"❌ 任務執行時發生錯誤：{e}")

# === 主程式 ===
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", help="指定要執行的任務")
    args = parser.parse_args()

    sys.path.insert(0, str(WORKSPACE_DIR))  # ✅ 確保 workspace 成為根模組
    task_map = scan_task_modules(DEFAULT_SCAN_DIRS)

    if args.task:
        run_task(args.task, task_map)
    else:
        print("⚠️ 請使用 --task 參數指定要執行的任務。")

if __name__ == "__main__":
    main()
