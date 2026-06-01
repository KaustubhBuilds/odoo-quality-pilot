"""
AI-powered Test Generator.

Reads a page object file and generates pytest test cases
that follow the project's patterns: POM, Allure decorators,
Faker data, proper assertions.

Usage:
    python ai_tools/test_generator.py pages/sales_page.py
    python ai_tools/test_generator.py pages/crm_page.py
"""

import sys

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

SYSTEM_PROMPT = """You are a senior QA automation engineer.
You generate pytest test cases from Playwright page object files.

Follow these rules strictly:
- Use pytest markers: @pytest.mark.ui
- Use Allure decorators: @allure.epic, @allure.feature, @allure.story, @allure.title
- Use the page object methods never use raw selectors in tests
- Use 'logged_in_page' as the pytest fixture for browser tests
- Add clear docstrings explaining what each test verifies
- Output ONLY valid Python code, no explanations or markdown
- Wrap tests in a class that inherits from nothing (plain class)

For test data, use ONLY these functions from utils.data_factory:
- generate_contact() returns: {"name", "email", "phone",
  "mobile", "company", "street", "city"}
- generate_lead() returns: {"customer", "opportunity",
  "expected_revenue", "lost_reason"}
- generate_product() returns: {"name", "price", "internal_ref"}
- generate_sales_order() returns: {"customer", "reference"}

Import them like: from utils.data_factory import generate_lead
Use them like: data = generate_lead(); crm.fill_customer(data["customer"])

Do NOT use Faker directly. Do NOT invent methods that don't exist.
"""


def generate_tests(page_object_path: str) -> str:
    """
    Read a page object file and generate test cases using AI.

    Args:
        page_object_path: Path to the page object Python file

    Returns:
        Generated test code as a string
    """
    # Read the page object source code
    with open(page_object_path) as f:
        page_code = f.read()

    client = OpenAI()

    response = client.responses.create(
        model="gpt-5.4-mini",
        instructions=SYSTEM_PROMPT,
        input=f"""Generate pytest test cases for this page object.
Include at least 3 tests: happy path, negative path, and edge case.

Page object code:
```python
{page_code}
```

Generate the complete test file with all imports.""",
    )

    return response.output_text


def main():
    if len(sys.argv) < 2:
        print("Usage: python ai_tools/test_generator.py <page_object_file>")
        print("Example: python ai_tools/test_generator.py pages/sales_page.py")
        sys.exit(1)

    page_path = sys.argv[1]
    print(f"Reading page object: {page_path}")
    print("Generating test cases with AI...\n")

    generated_code = generate_tests(page_path)

    print("=" * 60)
    print("GENERATED TEST CODE")
    print("=" * 60)
    print(generated_code)
    print("=" * 60)

    # Save to file
    output_path = page_path.replace("pages/", "tests/ai_generated/test_ai_")
    output_path = output_path.replace("_page.py", ".py")

    import os

    os.makedirs("tests/ai_generated", exist_ok=True)

    with open(output_path, "w") as f:
        f.write(generated_code)

    print(f"\nSaved to: {output_path}")
    print("Review the generated code before running it.")


if __name__ == "__main__":
    main()
