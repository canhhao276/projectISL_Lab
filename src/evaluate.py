# src/evaluate.py
import subprocess
import os
import shutil
import sys
from src.config import OUTPUTS_DIR, DATASET_DIR, RESULTS_DIR

def run_test(task_id, prompt_type="baseline"):
    """
    Hàm chạy unit test cho một task cụ thể và trả về kết quả.
    """
    print(f"--- Evaluating {task_id} ({prompt_type}) ---")
    
    # 1. Định nghĩa đường dẫn
    generated_code_path = OUTPUTS_DIR / prompt_type / f"{task_id}.py"
    test_script_path = DATASET_DIR / task_id / "test.py"
    
    if not generated_code_path.exists():
        print(f"Error: Generated code not found at {generated_code_path}")
        return "MISSING"

    # 2. Tạo thư mục tạm để chạy test
    # ClassEval yêu cầu folder chạy test phải chứa file __init__.py hoặc cấu trúc đúng để import
    temp_run_dir = RESULTS_DIR / "temp" / f"{task_id}_{prompt_type}"
    temp_run_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy code AI (đổi tên thành task_id.py để test_script.py import được)
    shutil.copy(generated_code_path, temp_run_dir / f"{task_id}.py")
    # Copy file test
    shutil.copy(test_script_path, temp_run_dir / "test_script.py")
    
    # Tạo file trống __init__.py để Python hiểu đây là một package
    with open(temp_run_dir / "__init__.py", "w") as f: pass

    # 3. Chạy pytest bằng subprocess
    # Chúng ta thêm thư mục tạm vào PYTHONPATH để pytest tìm thấy file
    env = os.environ.copy()
    env["PYTHONPATH"] = str(temp_run_dir) + os.pathsep + env.get("PYTHONPATH", "")
    
    result = subprocess.run(
        [sys.executable, "-m", "pytest", str(temp_run_dir / "test_script.py")],
        capture_output=True,
        text=True,
        env=env
    )
    
    # 4. Phân tích kết quả
    if result.returncode == 0:
        print(f"RESULT: PASSED ✅")
        return "PASSED"
    else:
        print(f"RESULT: FAILED ❌")
        # In lỗi ra để chúng ta soi sau này (Phase 7)
        # print(result.stdout)
        return "FAILED"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        task = sys.argv[1]
        ptype = sys.argv[2]
        run_test(task, ptype)
    else:
        # Mặc định nếu không truyền tham số
        res_b = run_test("task_001", "baseline")
        res_s = run_test("task_001", "structured")
        print(f"\nTASK 001 SUMMARY: Baseline: {res_b}, Structured: {res_s}")
