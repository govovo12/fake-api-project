from pathlib import Path
import re

tests_root = Path(__file__).resolve().parents[0] / "workspace" / "tests"
pytest_ini = Path(__file__).resolve().parents[0] / "pytest.ini"

test_files = list(tests_root.rglob("test_*.py"))

used_markers = set()
file_marks = {}

for file in test_files:
    content = file.read_text(encoding="utf-8")
    found = re.findall(r"pytest\.mark\.([a-zA-Z_][a-zA-Z0-9_]*)", content)
    marks_in_file = list(set(found))
    file_marks[str(file.relative_to(tests_root))] = marks_in_file
    used_markers.update(marks_in_file)

# 讀取 pytest.ini 中已註冊的 markers
registered_markers = set()
if pytest_ini.exists():
    content = pytest_ini.read_text(encoding="utf-8")
    matches = re.findall(r"^\s*([a-zA-Z_][a-zA-Z0-9_]*):", content, re.MULTILINE)
    registered_markers.update(matches)

# 分析差異
unused_registered = registered_markers - used_markers
unregistered_used = used_markers - registered_markers

print("✅ 使用中的 pytest.mark 名稱：")
for m in sorted(used_markers):
    print(f"  - {m}")

print("\n✅ pytest.ini 中註冊的 markers：")
for m in sorted(registered_markers):
    print(f"  - {m}")

if unused_registered:
    print("\n⚠️ 註冊但未在測試中使用的 markers：")
    for m in sorted(unused_registered):
        print(f"  - {m}")

if unregistered_used:
    print("\n❌ 使用但未註冊於 pytest.ini 的 markers（可能無法被 -m 抓到）：")
    for m in sorted(unregistered_used):
        print(f"  - {m}")

print("\n📂 每個測試檔案的 pytestmark 使用狀況：")
for file, marks in sorted(file_marks.items()):
    mark_display = ", ".join(marks) if marks else "❌ 無 pytestmark"
    print(f"  - {file}: {mark_display}")

no_mark_files = [f for f, marks in file_marks.items() if not marks]
if no_mark_files:
    print("\n❌ 以下測試檔案沒有 pytestmark（可能會被 -m 略過）：")
    for f in no_mark_files:
        print(f"  - {f}")
