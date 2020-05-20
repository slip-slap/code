#!/bin/bash
fswatch  -e modify ./presentation.log | while read change; do
    echo "change detected"
    osascript -e 'quit app "Adobe Acrobat Reader DC"'
    open presentation.pdf
#    osascript -e 'tell application "System Events"
#        tell application "Adobe Acrobat Reader DC" to activate
#        keystroke "h" using {command down, control down}
#        end tell'
done
