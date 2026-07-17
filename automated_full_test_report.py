# Automated Full Test Report
# Created by Vien Tran
# July-14-2026


# imports
import glob
import os
import re

# Path to where all the files are located
directory="."

# comment out based on what you are testing
full_files = [
    #"gui_test_out.txt",
    #"gui-coverage-report.txt",
    "mux_ut_output.txt",
    "mux-coverage-report.txt",
    #"coverage-report.txt",
    #"ut-output.txt",
    #"iot_integration_report.txt"
]



# Takes directory and registry 
def locate_files(directory, full_files):
    found = []
    missing = []
    counter = 0
    for file in full_files:
        if os.path.exists(os.path.join(directory, file)):
            found.append(file)
        else:
            missing.append(file)
    return found, missing 


# Preflight_checks
# This function will basically print out a summary table to the console whether something is found or not
# takes results from locate_files
def preflight_checks(found, missing, full_files):
    # Compare between the full_files and located files 
    # if everything is true then return True or Flase if anything is wrong
    print("\n=== PRE-FLIGHT FILE CHECK ===")
    
    for file in full_files:
        if file in found:
            print(f"    [   OK] {file}")
        else:
            print(f"    [   MISSING] {file}")
    print()
    if not missing: 
        print("All files accounted for. Ready for parsing.")
        return True
    else: 
        print(f"{len(missing)} files(s) missing. Fix before running full report.")
        return False 
    

# Main Function
# Call locate_files and preflight_checks 
# Structure
# - Separate functions for each file that looks through
#   each file, returns boolean and the text that we are looking for 
# - After calling each separete function file we will call the main 
#   function that summarizes all those booleans and text that we are looking for
#   (Some of these functions will work on 2 files and will return a single boolean and text report from both those file (but its combined into one))
# - Print out a .txt file that is the automated_full_test_report with date and build number 
def main():
    found, missing = locate_files(directory, full_files)
    ready = preflight_checks(found, missing, full_files)
    if not ready:
        return "Not ready for automated full test reporting"

    mux_result = mux_test_report(directory)
    print_report_result("mux_ut_output", mux_result["mux_ut_output"], "mux_ut_output has failing test cases")
    print_coverage_result("mux_coverage", mux_result["mux_coverage"])
    


# Each Test Report:
# - Open the file(s)
# - Search for the pass text case pattern
# - Return a result (pass/fail + text case pattern itself)
#
# GUI Test Report
# Files: gui_test_out.txt & gui-coverage-report.txt
def gui_test_reports(directory):
    filepath = os.path.join(directory, "gui_test_out.txt")
    pass_text = "passed text case right here"

    passed = False
    proof_line = None
    line_number = None

    with open(filepath, "r") as f:
        for i, line in enumerate(f, start=1):
            if pass_text in line:
                passed = True
                proof_line = line.strip()
                line_number = i 
                break





    # Part 2
    cov_filepath = os.path.join(directory, "gui-coverage-report.txt")
    
    pass_text = "passed text case right here"

    cov_passed = False
    cov_proof_line = None
    cov_line_number = None

    with open(cov_filepath, "r") as f:
        for i, line in enumerate(f, start=1):
            if pass_text in line:
                cov_passed = True
                cov_proof_line = line.strip()
                cov_line_number = i 
                break


    # Return pass/fail + which file + line number (useful for summary/debug) 
    return {
        "gui_test_out": {"passed": passed, "proof": proof_line, "line": line_number},
        "gui_coverage": {"passed": cov_passed, "proof": cov_proof_line, "line": cov_line_number}
    }

# Mux Test Report 
# Files: mux_ut_output.txt && mux-coverage-report.txt
def mux_test_report(directory):
    # --- mux_ut_output.txt --- 
    filepath = os.path.join(directory, "mux_ut_output.txt")
    pass_text1 = "test result: ok."
    pass_text2 = "; 0 failed;"
    pass_text3 = "; 0 ignored;"

    passed = False
    proof_line = None
    line_number = None 
    # "test result: ok, 1022 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 35.90s"
    # Very important to note is that the 1022 and the 35.90s has to be ignored, and the 0 failed is the most important thing 
    with open(filepath, "r") as f:
        for i, line in enumerate(f, start=1):
            if pass_text1 in line and pass_text2 in line and pass_text3 in line:
                passed = True 
                proof_line = line.strip() 
                line_number = i 
                break 

    # --- mux-coverage-report.txt ---
    # "53.96% coverage, 3841/6989 lines covered"
    # the numbers may vary but the code covereage HAS to be more than 50% to be a pass test case
    # if the number is less than 50% then its a failed case 
    cov_filepath = os.path.join(directory, "mux-coverage-report.txt")
    
    pass_text4 = "coverage,"
    pass_text5 = "lines covered"

    cov_passed = False 
    cov_proof_line = None 
    cov_line_number = None
    cov_percentage = None

    with open(cov_filepath, "r") as f:
        for i, line in enumerate(f, start=1):
            if "% coverage" in line and pass_text4 in line and pass_text5 in line:
    
                match = re.search(r"(\d+\.\d+)%", line)
                if match: 
                    percentage = float(match.group(1))
                    cov_percentage = percentage # store percentage 
                    if percentage >= 50.0:
                        cov_passed = True
                        cov_proof_line = line.strip()
                        cov_line_number = i 
                break

    return {
        "mux_ut_output": {"status": passed, "proof": proof_line, "line": line_number},
        "mux_coverage": {"status": cov_passed, "proof": cov_proof_line, "line": cov_line_number, "percentage": cov_percentage}
    }    


# Firmware Test Report 
# Files: coverage-report.txt & ut_output.txt
def firmware_unit_test(directory):
     # --- ut_output.txt ---
    filepath = os.path.join(directory, "ut_output.txt")

    passed = False
    proof_line = None
    line_number = None

    with open(filepath, "r") as f:
        for i, line in enumerate(f, start=1):
            if "OK (" in line:
                passed = True
                match = re.search(r"OK \((.+)\)", line)
                if match:
                    proof_line = "test result: ok. " + match.group(1)
                line_number = i
                break

    # --- coverage-report.txt ---
    cov_filepath = os.path.join(directory, "coverage-report.txt")

    top100_files = []
    most_changed_files = []
    current_section = None

    with open(cov_filepath, "r") as f:
        for line in f:
            stripped = line.strip()
            if "List of top 100 files that need exception reports" in stripped:
                current_section = "top100"
            elif "Most changed files that need exception report" in stripped:
                current_section = "most_changed"
            elif stripped == "":
                current_section = None
            elif current_section == "top100":
                top100_files.append(stripped)
            elif current_section == "most_changed":
                most_changed_files.append(stripped)

    return {
        "ut_output": {"status": passed, "proof": proof_line, "line": line_number},
        "coverage": {"top100_files": top100_files, "most_changed_files": most_changed_files}
    }

# Rest API Test Report
# Files: report-YYYY-MM-DD.txt
def rest_api_test():
    return None

# IOT Interface Test Report
# Files: iot_integration_report.txt
def iot_test_report():
    return None


# Helper function for test reports 
def print_report_result(report_name, result, fail_message):
    print(f"\n{report_name} results:")
    if result["proof"]:
        print(f"{result['proof']}")
    if result["status"]:
        print("All test Passed")
    else:
        print(f"There is a test failure, {fail_message}")

# Helper function for percentage for code coverage reports 
def print_coverage_result(report_name, result):
    print(f"\n{report_name}-report:")
    print(f"Code Coverage: {result['percentage']}%")
    if result["status"]:
        print(f"Code coverage Passed, {result['percentage']}% is >= 50%")
    else:
        print(f"Code coverage Failed, {result['percentage']}% is < 50%")

# Helper function for the firmware coverage:
def print_firmware_coverage_result(result):
    print("\ncoverage-report:")
    print("List of top 100 files that need to be included in the exception report:")
    for f in result["top100_files"]:
        print(f)
    print("\nMost changed files that need to be included in the exception report:")
    for f in result["most_changed_files"]:
        print(f)


if __name__ == "__main__":
    main()
