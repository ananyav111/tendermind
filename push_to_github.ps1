param (
    [string]$RepoUrl
)

if (-not $RepoUrl) {
    $RepoUrl = Read-Host "Enter your GitHub repository URL (e.g., https://github.com/your-username/tendermind.git)"
}

if (-not $RepoUrl) {
    Write-Host "Repository URL cannot be empty." -ForegroundColor Red
    exit 1
}

Write-Host "Setting remote origin to $RepoUrl..." -ForegroundColor Cyan
git remote remove origin 2>$null
git remote add origin $RepoUrl
git branch -M main

Write-Host "Pushing to GitHub..." -ForegroundColor Green
git push -u origin main

Write-Host "`nSuccessfully pushed to $RepoUrl!" -ForegroundColor Green
