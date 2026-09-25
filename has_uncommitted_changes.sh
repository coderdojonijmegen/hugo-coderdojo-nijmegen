find . -type d -name .git -print0 |
while IFS= read -r -d '' gitdir; do
    repo="${gitdir%/.git}"
    if [ -n "$(git -C "$repo" status --porcelain)" ]; then
        echo "Changes in: $repo"
        git -C "$repo" status --short
    fi
done