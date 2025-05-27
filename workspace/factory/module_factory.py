from modules import account_generator
from utils.random_factory import simple_random_string
from utils.json_helper import write_json

def get_account_generator_module():
    return {
        "account_module": account_generator,
        "random_fn": simple_random_string,
        "writer_fn": write_json
    }
