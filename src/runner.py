# src/runner.py
import pandas as pd
import time
import os
from src.generate import generate_solution
from src.evaluate import run_test
from src.config import RESULTS_DIR, DATASET_DIR

def main():
    # 1. Tự động lấy danh sách 10 task (task_001 đến task_010)
    tasks = sorted([d.name for d in DATASET_DIR.iterdir() if d.is_dir() and d.name.startswith("task_")])
    prompt_types = ["baseline", "structured"]
    
    all_results = []
    
    print(f"🚀 Bắt đầu Pipeline nghiên cứu cho {len(tasks)} tasks...")
    print("Dự kiến thời gian chạy: ~5-7 phút (do nghỉ để tránh Rate Limit API)")
    
    for task_id in tasks:
        print(f"\n" + "="*20)
        print(f"ĐANG XỬ LÝ: {task_id}")
        print("="*20)
        
        for p_type in prompt_types:
            # 1. AI viết code (PHASE 3)
            generate_solution(task_id, p_type)
            
            # 2. Nghỉ 15 giây (Bắt buộc cho bản Gemini Free để không bị lỗi 429)
            print(f"Nghỉ 15s để API reset hạn mức...")
            time.sleep(15)
            
            # 3. Chấm điểm (PHASE 4)
            status = run_test(task_id, p_type)
            
            all_results.append({
                "task": task_id,
                "prompt": p_type,
                "status": status
            })
            
    # 4. Xuất kết quả và Báo cáo (PHASE 5)
    df = pd.DataFrame(all_results)
    df.to_csv(RESULTS_DIR / "summary_results.csv", index=False)
    
    # Tính Pass Rate %
    pass_rate = df.groupby("prompt")["status"].apply(lambda x: (x == "PASSED").mean() * 100)
    
    print("\n" + "#"*50)
    print("KẾT QUẢ NGHIÊN CỨU CUỐI CÙNG (PASS RATE %)")
    print("#"*50)
    print(pass_rate)
    print("#"*50)
    print(f"Báo cáo chi tiết đã lưu tại: {RESULTS_DIR}/summary_results.csv")

if __name__ == "__main__":
    main()
