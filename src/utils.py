import os
from src.config import DATASET_DIR

def load_task_data(task_id):
    """
    Đọc toàn bộ dữ liệu của một task cụ thể.
    Trả về dictionary chứa nội dung các file.
    """
    task_path = DATASET_DIR / task_id
    
    data = {
        "skeleton": "",
        "test": "",
        "solution": ""
    }
    
    # Đọc skeleton.py (Đầu vào cho LLM)
    skeleton_file = task_path / "skeleton.py"
    if skeleton_file.exists():
        with open(skeleton_file, "r", encoding="utf-8") as f:
            data["skeleton"] = f.read()
            
    # Đọc test.py (Để đánh giá sau này)
    test_file = task_path / "test.py"
    if test_file.exists():
        with open(test_file, "r", encoding="utf-8") as f:
            data["test"] = f.read()
            
     # Đọc solution.py (Đáp án mẫu)
    solution_file = task_path / "solution.py"
    if solution_file.exists():
        with open(solution_file, "r", encoding="utf-8") as f:
            data["solution"] = f.read()

    # Đọc prompt.txt (Mô tả tự nhiên)
    prompt_file = task_path / "prompt.txt"
    if prompt_file.exists():
        with open(prompt_file, "r", encoding="utf-8") as f:
            data["prompt_text"] = f.read()
            
    return data

def save_generated_code(task_id, code, prompt_type="baseline"):
    """
    Lưu code do AI tạo ra vào thư mục outputs.
    """
    from src.config import OUTPUTS_DIR
    
    output_folder = OUTPUTS_DIR / prompt_type
    output_folder.mkdir(parents=True, exist_ok=True)
    
    file_path = output_folder / f"{task_id}.py"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)
    
    return file_path