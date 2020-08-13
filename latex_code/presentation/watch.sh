#!/bin/bash
fswatch  -e modify ./$1".log" | while read change; do
    echo "change detected"
    osascript -e 'quit app "Adobe Acrobat Reader DC"'
    open $1".pdf"
#    osascript -e 'tell application "System Events"
#        tell application "Adobe Acrobat Reader DC" to activate
#        keystroke "h" using {command down, control down}
#        end tell'
done
