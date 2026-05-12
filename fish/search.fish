# search
# ------
# Fuzzy-search files and copy the selected path to clipboard.
#
# Dependencies:
#   fzf, wl-copy
#
# Usage:
#   search
#
# Notes:
#   - Outputs nothing, copies result directly
#   - Uses Wayland clipboard (wl-copy)

function search
    fzf --preview='cat {}' | wl-copy
end