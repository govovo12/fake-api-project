import os
import subprocess

def get_current_branch():
    result = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True)
    return result.stdout.strip()

def prompt_input(prompt_msg, default):
    user_input = input(f"{prompt_msg} (預設: {default}) ➤ ").strip()
    return user_input if user_input else default

def finalize_and_force_push():
    current_branch = get_current_branch()
    print(f"\n🧠 當前分支為：{current_branch}")

    commit_msg = prompt_input("請輸入 Commit 訊息", "自動收尾")
    remote_branch = prompt_input("請輸入要覆蓋的遠端分支", "main")

    print("\n🔧 開始執行收尾操作...\n")

    os.system("git add .")
    os.system(f"git commit -m \"{commit_msg}\"")
    os.system(f"git pull origin {remote_branch} --rebase")
    os.system(f"git push origin HEAD:{remote_branch} --force")

    print(f"\n✅ 已強制推送至遠端分支：{remote_branch}")

if __name__ == "__main__":
    finalize_and_force_push()
