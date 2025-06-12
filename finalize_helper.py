import subprocess

def run(cmd):
    return subprocess.check_output(cmd, shell=True, encoding='utf-8').strip()

def main():
    print("📌 當前 Git 分支：")
    current_branch = run("git branch --show-current")
    print(f"➡️ 目前在：{current_branch}")

    # 分支切換
    target_branch = input("🔀 請輸入要切換的分支（預設=main）：").strip() or "main"
    run(f"git checkout {target_branch}")

    # Commit 訊息
    commit_msg = input("📝 請輸入 commit 訊息：").strip()
    if not commit_msg:
        print("❌ commit 訊息不可為空")
        return

    # 執行 Git 操作
    run("git add .")
    run(f'git commit -m "{commit_msg}"')
    run(f"git push origin {target_branch} --force")

    print(f"✅ 成功推送到 {target_branch}（已覆蓋遠端）")

if __name__ == "__main__":
    main()
