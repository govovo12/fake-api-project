from utils.printer.printer import print_info, print_warn, print_error print_info

def save_account_to_json(account, path, writer_fn):
    print(f"[module] 進入 save_account_to_json()，目標路徑：{path}")

    path.parent.mkdir(parents=True, exist_ok=True)
    writer_fn(account, path)

    print_info(f"[module] 測資儲存完成：{path}")
    return str(path)
