# src/generate.py
import google.generativeai as genai
from src.config import GEMINI_API_KEY, MODEL_NAME
from src.utils import load_task_data, save_generated_code
from src.prompts import get_prompt
import time

# Cấu hình Gemini
genai.configure(api_key=GEMINI_API_KEY)

def generate_solution(task_id, prompt_type="baseline"):
    """
    Hàm gọi API Gemini để sinh code cho một task cụ thể, 
    kết hợp cả code skeleton và mô tả bài toán.
    """
    print(f"--- Generating {task_id} using {prompt_type} prompt ---")
    
    # 1. Đọc dữ liệu task (bao gồm skeleton, test và prompt_text)
    data = load_task_data(task_id)
    if not data["skeleton"]:
        print(f"Error: Skeleton for {task_id} not found!")
        return
    
    # 2. Xây dựng prompt tích hợp mô tả từ prompt.txt
    description = data.get("prompt_text", "")
    prompt = get_prompt(data["skeleton"], description, prompt_type)
    
    try:
        # 3. Khởi tạo mô hình và gọi API
        model = genai.GenerativeModel(MODEL_NAME)
        
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.2, 
            )
        )
        
        # 4. Kiểm tra và trích xuất code
        if not response.text:
            print(f"AI returned empty response for {task_id}")
            return

        # Làm sạch code (bỏ dấu markdown ```python ... ```)
        clean_code = response.text.replace("```python", "").replace("```", "").strip()
        
        # 5. Lưu kết quả vào folder outputs tương ứng
        save_path = save_generated_code(task_id, clean_code, prompt_type)
        print(f"Successfully saved to: {save_path}")
        
    except Exception as e:
        print(f"API Error for {task_id}: {e}")

if __name__ == "__main__":
    # Chạy thử nghiệm cho task_001 với 2 loại prompt
    # Chạy Baseline
    generate_solution("task_001", prompt_type="baseline")
    
    # Nghỉ 5 giây để tránh lỗi Rate Limit (vì chúng ta dùng bản Free)
    print("Waiting 5s for API quota reset...")
    time.sleep(5)
    
    # Chạy Structured
    generate_solution("task_001", prompt_type="structured")
