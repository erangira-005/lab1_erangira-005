#!/bin/bash

# organizer.sh — Archives grades.csv and resets the workspace

GRADES_FILE="grades.csv"
ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"


# a) Check if the archive directory exists; create if not

if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir "$ARCHIVE_DIR"
    echo "Created archive directory: $ARCHIVE_DIR"
fi

# b) Generate a timestamp 

TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

# c) Rename grades.csv with the timestamp and move to archive

ARCHIVED_NAME="grades_${TIMESTAMP}.csv"

if [ ! -f "$GRADES_FILE" ]; then
    echo "Error: '$GRADES_FILE' not found. Nothing to archive."
    exit 1
fi

mv "$GRADES_FILE" "${ARCHIVE_DIR}/${ARCHIVED_NAME}"
echo "Archived: $GRADES_FILE → ${ARCHIVE_DIR}/${ARCHIVED_NAME}"

# d) Create a fresh empty grades.csv for the next batch

touch "$GRADES_FILE"
echo "Reset: New empty $GRADES_FILE created."

# e) Append a log entry to organizer.log (never overwrite)

echo "[${TIMESTAMP}] Original: ${GRADES_FILE} | Archived as: ${ARCHIVE_DIR}/${ARCHIVED_NAME}" >> "$LOG_FILE"
echo "Log updated: $LOG_FILE"

echo "Done."
