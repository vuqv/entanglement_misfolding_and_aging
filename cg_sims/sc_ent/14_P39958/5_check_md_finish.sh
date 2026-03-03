#!/bin/bash

for i in $(seq 0 49); do
    folder="$i"
    dcd_file="${i}_prod.dcd"
    fQ_file="fQ.dat"

    if [[ -d "$folder" ]]; then
        cd "$folder" || continue

        if [[ -f "$dcd_file" ]]; then
            #echo "${dcd_file} presented"
            if [[ -f "$fQ_file" ]]; then
                last_val=$(awk 'END {print $2}' "$fQ_file")
                if [[ "$last_val" == "100000000" ]]; then
                    echo "Folder $folder: PASS (second column of last row is 100000000)"
                else
                    echo "Folder $folder: FAIL (second column is $last_val, expected 100000000)"
                fi
            else
                echo "!!!!!!! Folder $folder: fQ.dat not found"
            fi
        else
            echo "!!!!!!!!! Folder $folder: $dcd_file not found"
        fi

        cd ..
    else
        echo "!!!!!!!!!!Folder $folder does not exist"
    fi
done
