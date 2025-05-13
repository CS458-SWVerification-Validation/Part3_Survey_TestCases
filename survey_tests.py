from test import Test

if __name__ == "__main__":
    tester = Test("http://127.0.0.1:5000")

    # Log in
    if not tester.login("duru@ug.bilkent.edu.tr", "98765432"):
        print("[-] Login failed. Aborting tests.")
        exit()

    # Test Case 1: A valid survey
    tester.test_create_survey("Cool Survey", [
        {
            "text": "What’s your favorite food?",
            "type": "Dropdown",
            "options": ["Pizza", "Sushi", "Tacos"],
            "required": True
        },
        {
            "text": "Why do you love it?",
            "type": "Open Text",
            "required": False,
            "conditional": {
                "question": "q0",
                "value": "Pizza"
            }
        }
    ])

    # Test Case 2: Valid title but no questions
    tester.test_create_survey("No Questions Survey", [])  # Expected: Failure

    # Test Case 3: One question with empty text
    tester.test_create_survey("Empty Question Text", [{
        "text": "",
        "type": "Multiple Choice",
        "options": ["Option A", "Option B"],
        "required": False
    }])  # Expected: Failure (question text required)

    # Test Case 4: Multiple Choice question with no options
    tester.test_create_survey("No Options MCQ", [{
        "text": "Choose one",
        "type": "Multiple Choice",
        "options": [],
        "required": True
    }])  # Expected: Failure (options required)

    # Test Case 5: Valid Open Text question
    tester.test_create_survey("Open Text Valid", [{
        "text": "Say something meaningful:",
        "type": "Open Text",
        "options": [],
        "required": True
    }])  # Expected: Success

    # Test Case 6: Conditional logic with non-existent question reference
    tester.test_create_survey("Invalid Logic", [{
        "text": "What’s your favorite color?",
        "type": "Dropdown",
        "options": ["Red", "Blue"],
        "required": False,
        "conditional": {
            "question": "q999",
            "value": "Whatever"
        }
    }])  # Expected: Failure (q999 doesn’t exist)

    # Test Case 7: Valid conditional logic
    tester.test_create_survey("Conditional Logic Test", [
        {
            "text": "Do you like pizza?",
            "type": "Multiple Choice",
            "options": ["Yes", "No"],
            "required": True
        },
        {
            "text": "What's your favorite topping?",
            "type": "Open Text",
            "options": [],
            "required": False,
            "conditional": {
                "question": "q0",
                "value": "Yes"
            }
        }
    ])  # Expected: Success

    # Test Case 8: A mix of question types
    tester.test_create_survey("Mixed Types Survey", [
        {
            "text": "Rate this form",
            "type": "Rating (1-5)",
            "options": [],
            "required": True
        },
        {
            "text": "Pick your mood",
            "type": "Checkboxes",
            "options": ["Happy", "Tired", "Inspired"],
            "required": False
        },
        {
            "text": "Any additional thoughts?",
            "type": "Open Text",
            "options": [],
            "required": False
        }
    ])  # Expected: Success

    # Test Case 9: Empty survey title and no questions
    tester.test_create_survey("", [])  # Expected: Failure (title required)

