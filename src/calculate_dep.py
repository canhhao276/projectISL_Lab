import ast
import os

def count_requirements(file_path):
    if not os.path.exists(file_path):
        return 0, 0
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read())
        except:
            return 0, 0
    m_deps = 0
    f_deps = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name) and node.func.value.id == 'self':
                m_deps += 1
        elif isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            if node.value.id == 'self':
                f_deps += 1
    return m_deps, max(0, f_deps - m_deps)

def main():
    print(f"{'Task ID':<10} | {'Field Requirements':<20} | {'Method Requirements':<20}")
    print("-" * 55)
    for i in range(1, 11):
        task_id = f"task_{i:03d}"
        sol_path = f"dataset/{task_id}/solution.py"
        m, f = count_requirements(sol_path)
        print(f"{task_id:<10} | {f:<20} | {m:<20}")

if __name__ == "__main__":
    main()
