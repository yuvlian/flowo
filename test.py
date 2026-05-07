from flowo import Flow, Type, Arccosh
from main import main as run_main


def test_snake_case():
    flow = Flow()
    try:
        with flow.function("Main"):
            flow.declare("my_variable", Type.INTEGER)
        print("FAIL: Snake case should not be allowed")
    except ValueError as e:
        print(f"PASS: {e}")


def test_reserved_word():
    flow = Flow()
    try:
        with flow.function("Main"):
            flow.declare("integer", Type.INTEGER)
        print("FAIL: Reserved word 'integer' should not be allowed")
    except ValueError as e:
        print(f"PASS: {e}")


def test_start_with_number():
    flow = Flow()
    try:
        with flow.function("Main"):
            flow.declare("1var", Type.INTEGER)
        print("FAIL: Name starting with number should not be allowed")
    except ValueError as e:
        print(f"PASS: {e}")


def test_undeclared_variable():
    flow = Flow()
    try:
        with flow.function("Main"):
            flow.assign("x", "10")
        print("FAIL: Undeclared variable 'x' should not be allowed")
    except RuntimeError as e:
        print(f"PASS: {e}")


def test_reserved_intrinsic():
    flow = Flow()
    try:
        with flow.function("Main"):
            flow.declare("x", Type.REAL)
            flow.assign("x", Arccosh("1.0"))
        print("FAIL: Reserved intrinsic Arccosh should not be allowed")
    except NotImplementedError as e:
        print(f"PASS: {e}")


def test_valid_program():
    try:
        run_main()
        print("PASS: Valid program (main.py) worked")
    except Exception as e:
        print(f"FAIL: {e}")


def main():
    tests = [
        test_snake_case,
        test_reserved_word,
        test_start_with_number,
        test_undeclared_variable,
        test_reserved_intrinsic,
        test_valid_program,
    ]

    print("Running Flowo Tests...")
    for test in tests:
        test()


if __name__ == "__main__":
    main()
