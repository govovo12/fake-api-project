from pathlib import Path
import importlib.util

print("🔍 掃描中...")

for path in Path("workspace").rglob("*.py"):
    try:
        spec = importlib.util.spec_from_file_location(path.stem, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, "__task_info__"):
            print(f"✅ 找到任務模組: {path}")
            print("   └─ __task_info__ =", module.__task_info__)
    except Exception as e:
        print(f"⚠️ 無法載入 {path}: {e}")
