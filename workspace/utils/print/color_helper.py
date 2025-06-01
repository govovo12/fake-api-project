# workspace/utils/printer/color_helper.py

def tool(func):
    func.is_tool = True
    return func

OKGREEN = "\033[92m"
WARNING = "\033[93m"
FAIL = "\033[91m"
ENDC = "\033[0m"

@tool
def apply_color(text: str, color_code: str) -> str:
    """將字串以指定 ANSI 色碼包裝後回傳 [TOOL]"""
    return f"{color_code}{text}{ENDC}"
