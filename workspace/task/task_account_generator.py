# workspace/task/task_account_generator.py

from controller.account_generator_controller import run_account_generator_task

__task_info__ = {
    "name": "task_account_generator",
    "entry": run_account_generator_task,
    "description": "產生隨機帳號測資，並寫入 login 用測資 json"
}
