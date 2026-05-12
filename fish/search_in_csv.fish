# search_in_csv
# -------------
# Search for a string inside a chosen CSV file (interactive or via argument).
#
# Dependencies:
#   rg (ripgrep), fzf, optional: parallel
#
# Usage:
#   search-in-csv <query>            # choose CSV via fzf
#   search-in-csv <query> <file>     # specify CSV directly
#
# Notes:
#   - Case-insensitive search
#   - Shows filename + matches
#   - Uses parallel if available

function search-in-csv
    if test (count $argv) -lt 1
        echo "Usage: search-in-csv <query> [file]"
        return 1
    end

    set query $argv[1]

    # Select file
    if test (count $argv) -ge 2
        set file $argv[2]
    else
        set file (ls *.csv | fzf --prompt="Select CSV: ")
    end

    if test -z "$file"
        echo "No file selected"
        return 1
    end

    if not test -f "$file"
        echo "File not found: $file"
        return 1
    end

    # Search
    if type -q parallel
        echo $file | parallel rg -i --with-filename "$query" {}
    else
        rg -i --with-filename "$query" "$file"
    end
end