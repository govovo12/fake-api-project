def generate_username(prefix: str, length: int, random_fn) -> str:
    return prefix + '_' + ''.join(random_fn(length))

def generate_password(length: int, random_fn) -> str:
    return ''.join(random_fn(length))

def generate_account(username_cfg: dict, password_cfg: dict, random_fn) -> dict:
    return {
        "username": generate_username(**username_cfg, random_fn=random_fn),
        "password": generate_password(**password_cfg, random_fn=random_fn)
    }

def generate_accounts(username_cfg: dict, password_cfg: dict, random_fn, count: int) -> list:
    return [
        generate_account(username_cfg, password_cfg, random_fn)
        for _ in range(count)
    ]

def save_account_to_json(data, path, writer_fn):
    # ✅ 若資料夾不存在就建立（這行最重要）
    path.parent.mkdir(parents=True, exist_ok=True)

    # 若只是一組 dict，包成 list 寫入
    if isinstance(data, dict):
        data = [data]
    writer_fn(data, path)
    return str(path)

