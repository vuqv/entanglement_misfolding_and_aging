#!/bin/bash

# Script to check if G and Q files in trajectory folders have the correct line count
# Expected: 13334 lines (13335 total but last line is empty)

EXPECTED_LINES=20000

echo "=================================="

# Loop through trajectories 0 to 49
for i in {0..49}; do
    G_FILE="$i/GQ/G/$i.G"
    Q_FILE="$i/GQ/Q/$i.Q"
    
    # Check if both files exist
    if [[ ! -f "$G_FILE" ]] || [[ ! -f "$Q_FILE" ]]; then
        echo "Trajectory $i: WARNING - Files missing!"
        echo "  G file exists: $([[ -f "$G_FILE" ]] && echo "Yes" || echo "No")"
        echo "  Q file exists: $([[ -f "$Q_FILE" ]] && echo "Yes" || echo "No")"
        continue
    fi
    
    # Get line counts (excluding empty last line)
    G_LINES=$(wc -l < "$G_FILE")
    Q_LINES=$(wc -l < "$Q_FILE")
    
    # Remove trailing empty line if it exists
    if [[ $(tail -c1 "$G_FILE" | wc -l) -eq 0 ]]; then
        G_LINES=$((G_LINES - 1))
    fi
    if [[ $(tail -c1 "$Q_FILE" | wc -l) -eq 0 ]]; then
        Q_LINES=$((Q_LINES - 1))
    fi
    
    # Check if both files have the expected line count
    if [[ $G_LINES -eq $EXPECTED_LINES ]] && [[ $Q_LINES -eq $EXPECTED_LINES ]]; then
        echo "Trajectory $i: Done"
    else
        echo "Trajectory $i: WARNING - Trajectory not complete!"
        echo "  G file lines: $G_LINES (expected: $EXPECTED_LINES)"
        echo "  Q file lines: $Q_LINES (expected: $EXPECTED_LINES)"
    fi
done

echo "=================================="
echo "Check complete!" 