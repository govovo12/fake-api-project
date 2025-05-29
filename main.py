# main.py
from dotenv import load_dotenv
load_dotenv()  # 這行就會自動載入根目錄的 .env
import argparse
import importlib
from pathlib import Path
# === 加入 workspace 根目錄到 PYTHONPATH，支援 controller/modules/config 匯入 ===
import sys
from pathlib import Path




ROOT_PATH = Path(__file__).resolve().parent / "workspace"
if str(ROOT_PATH) not in sys.path:
    sys.path.insert(0, str(ROOT_PATH))
def find_module_by_filename(base_dir: Path, target_filename: str):
    for py_file in base_dir.rglob("*.py"):
        if py_file.stem == target_filename:
            relative_path = py_file.relative_to(base_dir.parent).with_suffix("")
            module_path = ".".join(relative_path.parts)
            return module_path
    return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", required=True, help="模組檔名（例如 task_login）")
    args = parser.parse_args()
    print("[main] 開始執行任務：", args.task)

    base_dir = Path(__file__).resolve().parent / "workspace"
    module_path = find_module_by_filename(base_dir, args.task)

    if not module_path:
        print(f"❌ 找不到符合名稱的模組：{args.task}.py")
        return

    try:
        print(f"[main] 嘗試載入模組路徑：{module_path}")
        task_module = importlib.import_module(module_path)
        print("[main] task 模組已載入成功")

        if hasattr(task_module, "__task_info__"):
            task_meta = getattr(task_module, "__task_info__")
            entry = task_meta.get("entry")
            desc = task_meta.get("description", "")
            print("DEBUG: 抓到 entry =", entry)
            print("DEBUG: entry 的類型 =", type(entry))

            if callable(entry):
                print(f"✅ 執行 {module_path} 任務：{desc}")
                entry()
                return
            else:
                print(f"⚠ 模組 {module_path} 的 __task_info__ 缺少有效 entry")
                return

        print(f"⚠ 模組 {module_path} 沒有定義 __task_info__，請補上以支援新架構")

    except Exception as e:
        print(f"❌ 模組執行錯誤：{e}")



if __name__ == "__main__":
    main()
