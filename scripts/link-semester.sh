#!/bin/bash
currentSemester=$(yq '.project_root' $(dirname $0)/settings.yaml)@current-semester

# Check if 
if [ ! -d $1 ]; then
	echo "Input directory does not seem to exist. Please try again."
else
	ln -sfrn $1 $currentSemester
	echo "Changing current semester to point to: $1"
fi
