# open
# ----
# Fuzzy-select a file using fzf and open it in nvim with a preview.
#
# Dependencies:
#   fzf, nvim
#
# Usage:
#   open
#
# Notes:
#   - Uses `cat` for preview (simple, fast)
#   - Only opens if a file is selected

function open
    set file (fzf --preview='cat {}')
    if test -n "$file"
        nvim "$file"
    end
end