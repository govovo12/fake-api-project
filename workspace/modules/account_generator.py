def generate_username(prefix: str, length: int, random_fn) -> str:
    return prefix + '_' + ''.join(random_fn(length))

def generate_password(length: int, random_fn) -> str:
    return ''.join(random_fn(length))

def generate_account(username_cfg: dict, password_cfg: dict, random_fn) -> dict:
    return {
        "username": generate_username(**username_cfg, random_fn=random_fn),
        "password": generate_password(**password_cfg, random_fn=random_fn)
    }

def save_account_to_json(account: dict, output_path, json_writer) -> str:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    json_writer(account, output_path)
    return str(output_path)
