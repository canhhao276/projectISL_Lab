# BÁO CÁO NGHIÊN CỨU: ĐÁNH GIÁ KHẢ NĂNG SINH MÃ MỨC ĐỘ LỚP CỦA LLM TRÊN BENCHMARK CLASSEVAL

**Người thực hiện**: [Nguyễn Cảnh Hào]  
**Mô hình thử nghiệm**: Google Gemini 3.1 Flash Lite  
**Ngày thực hiện**: 10/05/2026

---

## 1. GIỚI THIỆU (INTRODUCTION)
Báo cáo này trình bày kết quả đánh giá mô hình ngôn ngữ lớn (LLM) - Gemini 3.1 Flash Lite trên benchmark **ClassEval**. Khác với các bộ đánh giá mức hàm (function-level) truyền thống như HumanEval, ClassEval tập trung vào khả năng lập trình hướng đối tượng (OOP), yêu cầu mô hình phải hiểu mối quan hệ phức tạp giữa các phương thức và trạng thái nội tại của một lớp.

---

## 2. PHƯƠNG PHÁP NGHIÊN CỨU (METHODOLOGY)

### 2.1. Quy trình đánh giá (Pipeline)
Chúng tôi xây dựng hệ thống tự động hóa hoàn chỉnh:
1.  **Dữ liệu**: Lựa chọn 10 bài toán mẫu đầu tiên từ tập dữ liệu ClassEval, thực hiện kiểm tra và hiệu chỉnh cấu trúc để đảm bảo môi trường chạy test ổn định.
2.  **Chiến lược sinh mã (RQ2 Focus)**: Tập trung vào **Holistic Generation** (Sinh mã tổng thể). Đây là chiến lược phổ biến nhất trong thực tế khi các lập trình viên sử dụng AI: yêu cầu AI hoàn thiện toàn bộ một lớp từ khung xương (Skeleton) hoặc mô tả. Đây cũng là kịch bản thách thức nhất đối với khả năng duy trì logic nhất quán của mô hình.
3.  **Prompting**: Thử nghiệm hai dạng: **Baseline** (Chỉ dẫn đơn giản) và **Structured** (Chỉ dẫn có cấu trúc).
4.  **Chấm điểm tự động**: Sử dụng công cụ `pytest` để chạy các bộ kiểm thử (test cases) trên mã nguồn AI đã viết, từ đó đo lường tỷ lệ thành công (Pass@1).
5.  **Phân tích phụ thuộc (Dependency Analysis)**: Thực hiện rà soát cấu trúc mã nguồn tự động để định lượng độ phức tạp của bài toán thông qua việc đếm số lượng lời gọi hàm nội bộ (Method Dep) và truy cập thuộc tính (Field Dep) từ mã nguồn chuẩn.

### 2.2. Các chỉ số đo lường
*   **Pass@1**: Tỷ lệ vượt qua toàn bộ Class-level tests trong một lần sinh duy nhất.
*   **Method Requirements**: Số lượng lời gọi hàm nội bộ có trong mã nguồn chuẩn (đo độ phức tạp về hàm).
*   **Field Requirements**: Số lượng truy cập biến/thuộc tính có trong mã nguồn chuẩn (đo độ phức tạp về dữ liệu).

---

## 3. KẾT QUẢ THỰC NGHIỆM (RESULTS)

| Chỉ số đánh giá | Baseline Prompt | Structured Prompt |
| :--- | :---: | :---: |
| Tổng số Task | 10 | 10 |
| Số lượng PASSED (Class-level) | 7 | 7 |
| **Chỉ số Pass@1** | **70.0%** | **70.0%** |

**Danh sách chi tiết (Pass@1):**
*   **PASSED**: Task 002, 004, 006, 007, 008, 009, 010.
*   **FAILED**: Task 001 (AccessGatewayFilter), 003 (ArgumentParser), 005 (AssessmentSystem).

---

## 4. PHÂN TÍCH LỖI CHI TIẾT (ERROR ANALYSIS - RQ4)

Chúng tôi mổ xẻ 3 trường hợp thất bại để phân loại lỗi theo tiêu chuẩn của bộ dữ liệu ClassEval:

| Task | Tên bài toán | Loại lỗi | Chi tiết kỹ thuật (Test case bị lỗi) |
| :--- | :--- | :---: | :--- |
| **001** | AccessGatewayFilter | **Wrong Return Value** | Fail `test_filter_7`, `test_filter_8`. AI thực hiện kiểm tra JWT và mức độ quyền hạn quá khắt khe so với đặc tả của bộ test. |
| **003** | ArgumentParser | **Logic Error** | Fail `test_parse_arguments_1`, `test_parse_arguments_2`, `test_convert_type_5`, `test_main`. Nguyên nhân do AI lập trình cứng việc bỏ qua 2 thành phần đầu của chuỗi (`split()[2:]`) và lỗi logic trong việc ép kiểu dữ liệu. |
| **005** | AssessmentSystem | **Logic Error (Edge case)** | Fail `test_get_course_average_2`. AI gặp lỗi `TypeError` khi tính toán trung bình cộng do không xử lý trường hợp dữ liệu bị `None` (Null-safety). |

---

## 5. THẢO LUẬN (DISCUSSION)

### 5.1. Khả năng sinh mã mức Class (RQ1)
Mô hình Gemini 3.1 Flash Lite đạt hiệu năng khá tốt (**70% Pass@1** ở mức Class-level). Tuy nhiên, khi nhìn sâu hơn vào kết quả ở mức độ phương thức (**Method-level/Test-case level**), mô hình cho thấy sự xuất sắc vượt trội:
*   Ngay cả ở các Task bị tính là FAILED, AI thường vượt qua hầu hết các bài kiểm tra. Ví dụ: **Task 005 (vượt qua 30/31 test cases)** và **Task 003 (vượt qua 17/21 test cases)**.
*   **Nhận xét**: Điều này chứng tỏ Gemini 3.1 có khả năng viết mã đơn lẻ cực kỳ chính xác. Sự thất bại ở mức Class-level (Pass@1) không phải do AI không biết viết code, mà do "lỗi tích tụ" hoặc sai sót ở một phương thức then chốt làm ảnh hưởng đến toàn bộ tính nhất quán của Class.

### 5.2. Chiến lược sinh mã tổng thể (RQ2 - Generation Strategy)
Nghiên cứu tập trung vào chiến lược **Holistic Generation** (Sinh mã tổng thể) - chiến lược thực tiễn nhất cho các mô hình có khả năng Instruction-Following mạnh.
*   **Kết quả**: Việc thay đổi định dạng từ Baseline sang Structured Prompt trong cùng chiến lược Holistic không tạo ra sự khác biệt về Pass@1.
*   **Thảo luận**: Điều này chỉ ra rằng với Gemini 3.1, chiến lược Holistic là cực kỳ ổn định. Mô hình không nhạy cảm với cách trình bày prompt mà tập trung hoàn toàn vào nội dung Skeleton được cung cấp. Kết quả này ủng hộ quan điểm cho rằng chiến lược Holistic là đủ hiệu quả cho các mô hình LLM tiên tiến mà không nhất thiết phải chia nhỏ bài toán (Incremental).

### 5.3. Phân tích phụ thuộc (RQ3 - Dependency Analysis)
Dựa trên việc rà soát cấu trúc mã nguồn chuẩn (`solution.py`), chúng tôi đo lường độ phức tạp của bài toán thông qua số lượng phụ thuộc thực tế:
*   **Phát hiện 1**: Các bài toán có độ phức tạp phụ thuộc phương thức cao (**Method Requirements >= 2** như Task 001, 003) đều dẫn đến thất bại. Ở mức độ phụ thuộc thấp hơn (1 yêu cầu), mô hình vẫn có thể thất bại nếu logic nghiệp vụ đi kèm các trường hợp biên phức tạp (như lỗi Null-safety ở Task 005).
*   **Phát hiện 2**: Ngược lại, mô hình đạt tỷ lệ thành công tuyệt đối ở các bài toán có **Method Requirements = 0** hoặc các bài toán tập trung vào phụ thuộc thuộc tính (**Field Requirements** cao như Task 002, 009).
*   **Kết luận**: Kết quả này củng cố **Finding 4** của bài báo gốc: Việc điều phối logic giữa các hàm (Method-invoking) là thách thức lớn nhất. Khi độ phức tạp của các mối liên kết tăng lên, AI bắt đầu bộc lộ các lỗ hổng trong việc duy trì tính nhất quán của dữ liệu.

### 5.4. Phân tích lỗi chi tiết (RQ4 - Bad Case Analysis)
Chúng tôi thực hiện phân tích sâu các lỗi thực thi (Runtime Errors) để hiểu giới hạn của mô hình trong việc duy trì ràng buộc ngữ cảnh.
*   **Trường hợp tiêu biểu (Task 005)**: Mô hình gặp lỗi **`TypeError: unsupported operand type(s) for +=: 'int' and 'NoneType'`**. Điều này xảy ra khi AI cố gắng thực hiện tính toán trên một biến thuộc tính chưa được khởi tạo hoặc bị gán giá trị `None`. 
*   **Nhận xét**: Lỗi này hoàn toàn trùng khớp với **Finding 5** của bài báo gốc: LLM thường xuyên gặp khó khăn trong việc hiểu và đáp ứng các ràng buộc về kiểu dữ liệu (semantic constraints) trong môi trường Class-level phức tạp.
*   **Kết luận (Finding 5)**: Các lớp mã nguồn do LLM sinh ra thường mắc lỗi `TypeError` và `AttributeError`. Điều này cho thấy mô hình vẫn còn hạn chế trong việc hiểu sâu các phụ thuộc trạng thái (state dependencies) bên trong một Class, dẫn đến việc thao tác sai trên các biến thành viên.

---

## 6. KẾT LUẬN & HƯỚNG PHÁT TRIỂN
Dự án đã xây dựng thành công Pipeline đánh giá chuẩn hóa cho ClassEval. Kết quả nghiên cứu chỉ ra rằng Gemini 3.1 Flash Lite là một công cụ mạnh mẽ cho lập trình OOP nhưng vẫn cần sự giám sát của con người ở các khâu xử lý ngoại lệ và logic nghiệp vụ phức tạp.

**Hướng phát triển**: Mở rộng sang các chiến lược **Incremental** và **Compositional Generation** để đánh giá sự thay đổi hiệu năng khi chia nhỏ bài toán.

---
**Chữ ký xác nhận**  
*Nguyễn Cảnh Hào*
