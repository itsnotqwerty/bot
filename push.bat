@echo on
echo Beginning push...
set \p commitMessage=Enter a commit message:
git add .
git commit -m "Commit on %date% at %time%: %commitMessage%"
git push github main
echo Push finished.