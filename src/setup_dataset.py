import requests
import json
import os
from pathlib import Path

CLASSEVAL_URL = "https://raw.githubusercontent.com/FudanSELab/ClassEval/master/data/ClassEval_data.json"
DATASET_DIR = Path("dataset")

def clean_and_merge_imports(import_list, skeleton_code):
    # Chuyển import_list (có thể là list hoặc str) thành một set các dòng
    if isinstance(import_list, str):
        import_list = [line.strip() for line in import_list.split('\n') if line.strip()]
    
    unique_imports = set(import_list)
    
    # Tách các dòng trong skeleton
    skeleton_lines = skeleton_code.split('\n')
    new_skeleton_lines = []
    
    for line in skeleton_lines:
        trimmed = line.strip()
        # Nếu dòng đó là import/from, thêm vào set và bỏ qua trong phần thân skeleton
        if trimmed.startswith('import ') or trimmed.startswith('from '):
            unique_imports.add(trimmed)
        else:
            new_skeleton_lines.append(line)
            
    # Gộp lại: Imports ở trên đầu, code ở dưới
    final_imports = "\n".join(sorted(list(unique_imports)))
    final_skeleton = "\n".join(new_skeleton_lines)
    return final_imports + "\n\n" + final_skeleton.strip()

def setup(num_tasks=10):
    print(f"--- Downloading and Cleaning {num_tasks} tasks from ClassEval ---")
    try:
        response = requests.get(CLASSEVAL_URL)
        response.encoding = 'utf-8-sig'
        tasks = json.loads(response.text)
        
        for i in range(min(num_tasks, len(tasks))):
            task = tasks[i]
            task_id = f"task_{i+1:03d}"
            task_path = DATASET_DIR / task_id
            task_path.mkdir(parents=True, exist_ok=True)
            
            # 1. Lưu skeleton.py (Đã làm sạch import)
            imports = task.get("import_statement", [])
            cleaned_skeleton = clean_and_merge_imports(imports, task["skeleton"])
            with open(task_path / "skeleton.py", "w", encoding="utf-8") as f:
                f.write(cleaned_skeleton)
            
            # 2. Lưu test.py (Giữ nguyên logic import chuẩn)
            class_name = task["class_name"]
            common_test_imports = ["import unittest", "import datetime", "import math", "import os", "import json", "import logging", "import re"]
            if isinstance(imports, list): common_test_imports.extend(imports)
            full_test_imports = "\n".join(sorted(list(set(common_test_imports))))
            
            test_code = task["test"].replace(f"from {class_name} import", f"from {task_id} import")
            if f"from {task_id}" not in test_code:
                test_code = f"from {task_id} import {class_name}\n" + test_code
            
            with open(task_path / "test.py", "w", encoding="utf-8") as f:
                f.write(full_test_imports + "\n\n" + test_code)
            
            # 3. Lưu prompt.txt & solution.py
            with open(task_path / "prompt.txt", "w", encoding="utf-8") as f:
                f.write(task.get("class_description", "No description provided."))
            with open(task_path / "solution.py", "w", encoding="utf-8") as f:
                f.write(task.get("solution_code", ""))
                
            print(f"Done: {task_id} ({class_name})")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    setup(10)
