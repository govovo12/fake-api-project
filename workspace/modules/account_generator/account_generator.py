from utils.printer.printer import print_info, print_warn, print_error print_info

def generate_account(username_config, password_config, random_fn):
    print("[module] 進入 generate_account()")
    return {
        "username": random_fn(username_config["prefix"], username_config["length"]),
        "password": random_fn("", password_config["length"])
    }

def generate_accounts(username_config, password_config, random_fn, count):
    print(f"[module] 進入 generate_accounts()，數量：{count}")
    return [
        generate_account(username_config, password_config, random_fn)
        for _ in range(count)
    ]
