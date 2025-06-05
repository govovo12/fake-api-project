import argparse
import sys
import json
from pathlib import Path
from workspace.config.paths import PROJECT_ROOT

def main():
    parser = argparse.ArgumentParser(description="Fake-API 任務入口")
    parser.add_argument("--folder", type=str, required=True, help="請指定任務資料夾名稱（如 controller、tasks）")
    parser.add_argument("--task", type=str, required=True, help="請指定要執行的任務模組名稱（不含 .py）")
    parser.add_argument("--params", type=str, default="", help="JSON 格式參數，例如: '{\"user_uuid\": \"abc123\"}'")
    args = parser.parse_args()

    folder = args.folder
    task_name = args.task
    param_str = args.params

    task_module_path = PROJECT_ROOT / "workspace" / folder / f"{task_name}.py"
    if not task_module_path.exists():
        print(f"❌ 找不到任務模組：{task_module_path}")
        sys.exit(1)

    import importlib.util
    spec = importlib.util.spec_from_file_location(task_name, task_module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # 解析參數（優先使用 CLI，否則 fallback 為模組內定義的 default_params）
    try:
        task_params = json.loads(param_str) if param_str else module.__task_info__.get("default_params", {})
    except Exception as e:
        print(f"❌ 無法解析 --params：{e}")
        sys.exit(1)

    if not hasattr(module, "__task_info__"):
        print(f"❌ 模組 {task_name} 缺少 __task_info__。")
        sys.exit(1)

    entry_func = module.__task_info__.get("entry", None)
    if not entry_func:
        entry_func = getattr(module, "run", None)

    if not callable(entry_func):
        print(f"❌ 模組 {task_name} 缺少 entry 或 run 函式。")
        sys.exit(1)

    # 執行任務
    entry_func(**task_params)

if __name__ == "__main__":
    main()
