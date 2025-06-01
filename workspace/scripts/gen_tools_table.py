import os
import ast
from pathlib import Path
from collections import defaultdict

# 根目錄與輸出路徑請依實際調整
UTILS_ROOT = Path(__file__).resolve().parent.parent / "utils"
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "docs" / "tools_table.md"

def is_tool_function(node):
    """判斷 AST function/class node 是否有 @tool 裝飾器 或 docstring 含 [TOOL]"""
    for deco in getattr(node, "decorator_list", []):
        if isinstance(deco, ast.Name) and deco.id == "tool":
            return True
    doc = ast.get_docstring(node) or ""
    if "[TOOL]" in doc:
        return True
    return False

def scan_utils(path: Path):
    categorized = defaultdict(list)  # { category: [ {module, name, doc, is_tool}, ... ] }
    for root, dirs, files in os.walk(path):
        for fname in files:
            if fname.endswith(".py") and not fname.startswith("__"):
                fpath = Path(root) / fname
                try:
                    with open(fpath, encoding="utf-8") as f:
                        tree = ast.parse(f.read(), filename=str(fpath))
                except Exception as e:
                    print(f"[Warn] 解析失敗 {fpath}: {e}")
                    continue

                rel_path = fpath.relative_to(UTILS_ROOT)
                module_path_str = str(rel_path.parent).replace("\\", "/") or "(root)"
                category = module_path_str.split("/")[0] if module_path_str != "(root)" else "(root)"

                for node in tree.body:
                    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                        name = node.name
                        if name.startswith("_") or name.startswith("test_"):
                            continue
                        if not is_tool_function(node):
                            continue
                        doc = (ast.get_docstring(node) or "").splitlines()
                        doc = doc[0].strip() if doc else ""
                        categorized[category].append({
                            "module": module_path_str,
                            "name": name,
                            "doc": doc,
                            "is_tool": "✅",
                        })
    # 各分類內排序
    for cat in categorized:
        categorized[cat].sort(key=lambda r: (r['module'], r['name']))

    return dict(sorted(categorized.items()))  # 按分類排序返回

def write_tools_table(categorized_table):
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("# 🛠️ Fake API 專案自製工具對照表（含分類分段）\n\n")
        for category, rows in categorized_table.items():
            f.write(f"## {category}\n\n")
            f.write("| 模組 | 名稱 | 說明 | @tool |\n")
            f.write("|---|---|---|---|\n")
            for row in rows:
                f.write(f"| {row['module']} | {row['name']} | {row['doc']} | {row['is_tool']} |\n")
            f.write("\n---\n\n")

    print(f"已產生分分類工具表：{OUTPUT_PATH}")

def main():
    print(f"開始掃描工具模組：{UTILS_ROOT}")
    categorized_table = scan_utils(UTILS_ROOT)
    if not categorized_table:
        print("沒有掃描到任何帶 @tool 標記的函式或類別！")
    write_tools_table(categorized_table)

if __name__ == "__main__":
    main()
