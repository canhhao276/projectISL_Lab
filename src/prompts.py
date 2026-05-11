# src/prompts.py

BASELINE_TEMPLATE = """
Task Description: {description}

Please complete the following Python class:

{skeleton}

Provide only the completed code for the class.
"""

STRUCTURED_TEMPLATE = """
Task: Class-Level Code Generation
Context: {description}

Instructions:
1. Complete the Python class provided below.
2. Ensure all methods are implemented according to their docstrings.
3. Maintain the internal state and dependencies between methods.
4. Output only the source code.

Skeleton:
{skeleton}
"""

def get_prompt(skeleton, description="", prompt_type="baseline"):
    # Nếu không có description, ta để chuỗi trống hoặc câu thông báo mặc định
    desc = description if description else "Complete the class based on the skeleton."
    
    if prompt_type == "baseline":
        return BASELINE_TEMPLATE.format(skeleton=skeleton, description=desc)
    else:
        return STRUCTURED_TEMPLATE.format(skeleton=skeleton, description=desc)
