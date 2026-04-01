import csv
import sys
import os


def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists,
    and extracts all fields into a list of dictionaries.
    Handles: missing file, empty file.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ").strip()

    # If not an absolute path, resolve relative to the script's directory
    if not os.path.isabs(filename):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(script_dir, filename)

    # Check if file exists
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    assignments = []
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numeric fields to floats for calculations
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

    return assignments


def evaluate_grades(data):
    """
    Evaluates student grades from the loaded CSV data.

    Steps:
      a) Validate all scores are between 0 and 100
      b) Validate weights: total=100, Formative=60, Summative=40
      c) Calculate weighted total grade and GPA
      d) Determine Pass/Fail (>= 50% in BOTH groups separately)
      e) Identify failed formative assignments for resubmission
      f) Print final decision
    """
    print("\n--- Processing Grades ---")

    # Handle empty file (e.g. after organizer.sh has run)
    if not data:
        print("Error: The CSV file is empty. No grades to process.")
        sys.exit(1)

    # a) Score Validation — every score must be 0 to 100

    invalid_scores = []
    for row in data:
        if not (0 <= row['score'] <= 100):
            invalid_scores.append(row['assignment'])

    if invalid_scores:
        print(f"Warning: Invalid scores detected in: {', '.join(invalid_scores)}")
        print("         Scores must be between 0 and 100.")

    
    # b) Weight Validation — total=100, Formative=60, Summative=40
    
    total_weight     = sum(row['weight'] for row in data)
    formative_weight = sum(row['weight'] for row in data if row['group'] == 'Formative')
    summative_weight = sum(row['weight'] for row in data if row['group'] == 'Summative')

    if total_weight != 100:
        print(f"Error: Total weights sum to {total_weight}, but must equal 100.")
        sys.exit(1)

    if formative_weight != 60:
        print(f"Error: Formative weights sum to {formative_weight}, but must equal 60.")
        sys.exit(1)

    if summative_weight != 40:
        print(f"Error: Summative weights sum to {summative_weight}, but must equal 40.")
        sys.exit(1)

    print("Weight validation: PASSED (Total=100, Formative=60, Summative=40)")


    # c) Calculate Final Grade and GPA
    #    Formula: GPA = (total_grade / 100) * 5.0
   
    total_grade = sum((row['score'] * row['weight']) / 100 for row in data)
    gpa = (total_grade / 100) * 5.0

    print(f"\nTotal Grade : {total_grade:.2f}%")
    print(f"GPA         : {gpa:.2f} / 5.0")

    
    # d) Pass/Fail — student must score >= 50% in BOTH groups
    #    Group score = weighted sum within group / group weight * 100
   
    formative_rows = [row for row in data if row['group'] == 'Formative']
    summative_rows = [row for row in data if row['group'] == 'Summative']

    # Weighted score earned in each group
    formative_earned  = sum((row['score'] * row['weight']) / 100 for row in formative_rows)
    summative_earned  = sum((row['score'] * row['weight']) / 100 for row in summative_rows)

    # Convert to a percentage relative to each group's total weight
    formative_pct = (formative_earned / formative_weight) * 100
    summative_pct = (summative_earned / summative_weight) * 100

    print(f"\nFormative group score : {formative_pct:.2f}%  (need >= 50%)")
    print(f"Summative group score : {summative_pct:.2f}%  (need >= 50%)")

    passed = formative_pct >= 50 and summative_pct >= 50

    
    # e) Resubmission Logic — only applies when student FAILED
    #    Find failed formative assignments (score < 50)
    #    then pick the one with the HIGHEST weight
  
    if not passed:
        failed_formative = [row for row in formative_rows if row['score'] < 50]

        if failed_formative:
            max_weight = max(row['weight'] for row in failed_formative)
            resubmit_candidates = [
                row['assignment'] for row in failed_formative
                if row['weight'] == max_weight
            ]
            print(f"\nResubmission recommended : {', '.join(resubmit_candidates)}")
            print(f"(Highest-weight failed formative assignment(s) — weight: {max_weight})")
        else:
            # Student failed overall but no individual formative < 50
            print("\nNo individual formative assignments scored below 50%.")
            print("Review overall performance with your instructor.")

    
    # f) Print Final Decision
   
    print("\n" + "=" * 40)
    if passed:
        print("FINAL RESULT: PASSED")
    else:
        print("FINAL RESULT: FAILED")
    print("=" * 40)


if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()

    # 2. Evaluate and print the results
    evaluate_grades(course_data)
