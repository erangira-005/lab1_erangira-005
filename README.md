Lab 1: Grade Evaluator & Archiver

A two-part tool that evaluates student grades from a CSV file and archives the data using a shell script.

 Files in This Repository

File - Description 

grade-evaluator.py | Python script that reads and evaluates grades 
organizer.sh | Bash script that archives the CSV and resets the workspace 
grades.csv | Sample input data file 
Readme.md | This file 

 Requirements

Python 3.x — no external libraries needed (uses built-in `csv`, `sys`, `os`)
Bash — any Unix/Linux/macOS terminal, or Git Bash on Windows

 How to Run the Python Script

 1. Prepare your "grades.csv"

The CSV must have exactly these columns:


assignment,group,weight,score
Quiz 1,Formative,20,72
Assignment 1,Formative,40,65
Midterm Exam,Summative,20,48
Final Exam,Summative,20,55


Rules the script enforces:
- All scores must be between 0 and 100
- All weights must sum to exactly "100"
- Formative weights must sum to exactly"60"
- Summative weights must sum to exactly "40"

 2. Run the script

bash
python3 grade-evaluator.py


When prompted, type the filename:

Enter the name of the CSV file to process (e.g., grades.csv): grades.csv

3. Sample output


 Processing Grades 
Weight validation: PASSED (Total=100, Formative=60, Summative=40)

Total Grade : 63.10%
GPA         : 3.16 / 5.0

Formative group score : 67.67%  (need >= 50%)
Summative group score : 51.50%  (need >= 50%)


FINAL RESULT: PASSED



 How to Run the Shell Script

bash
chmod +x organizer.sh   # only needed once
./organizer.sh

 What it does:
1. Creates an "archive/" folder if it doesn't exist
2. Renames "grades.csv" to "grades_YYYYMMDD-HHMMSS.csv"
3. Moves the renamed file into "archive/"
4. Creates a new empty "grades.csv" ready for the next batch
5. Appends a log entry to "organizer.log"

 Sample output:

Created archive directory: archive
Archived: grades.csv → archive/grades_20251105-170000.csv
Reset: New empty grades.csv created.
Log updated: organizer.log
Done.


 Sample "organizer.log" entry:

[20251105-170000] Original: grades.csv | Archived as: archive/grades_20251105-170000.cs


 Pass/Fail Logic

A student "passes" only if they score "≥ 50% in both groups separately":

- Formative group score = weighted average of all Formative assignments
- Summative group score = weighted average of all Summative assignments

Scoring above 50% overall does "not" guarantee a pass if either group falls below 50%.


 Resubmission

If a student fails, the script identifies which "Formative" assignment they should resubmit — specifically the one with the "highest weight" among those scored below 50%. If multiple assignments share that weight, all are listed.
