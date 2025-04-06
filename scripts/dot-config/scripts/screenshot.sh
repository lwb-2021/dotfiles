#! /bin/bash
grim -g "$(slurp)" -t png "$HOME/Pictures/screenshots/$(date +%Y-%m-%d-%H%M%S).png"
