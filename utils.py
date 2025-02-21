import aisuite as ai
import openpyxl

def run_test(code, tests):
    """Run the test cases for the given code with string and random modules."""
    namespace = {
            '__builtins__': __builtins__,
            'random': __import__('random'),
            'string': __import__('string'),
    }
    # Just execute and let exceptions propagate up
    exec(code, namespace)
    exec(tests, namespace)
    return 

def extract_code(text):
    start_tag = "<code>"
    end_tag = "</code>"
    start_index = text.find(start_tag) + len(start_tag)
    end_index = text.find(end_tag)
    return text[start_index:end_index].strip()

def sanity_check(sheet):
    """Run all test cases with packaged code from the supplied sheet."""
    for row in sheet.iter_rows(min_row=2, max_row=24, values_only=True):
        packaged_code = row[2]
        test_cases = row[3]
        try:
            run_test(packaged_code, test_cases)
        except Exception as e:
            print(f"Error in {row[0]} in sanity check:\n{str(e)}")
    print("Sanity check done!")

if __name__ == "__main__":
    workbook = openpyxl.load_workbook('test.xlsx')
    # Select the active sheet
    sheet = workbook.active
    sanity_check(sheet)