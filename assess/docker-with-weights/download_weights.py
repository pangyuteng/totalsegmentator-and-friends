import os
import ast
from time import sleep
from totalsegmentator.libs import download_pretrained_weights

if __name__ == "__main__":
    task_id_list = ast.literal_eval(os.environ.get("TASK_ID_LIST"))
    for task_id in task_id_list:
        download_pretrained_weights(task_id)
        sleep(5)
