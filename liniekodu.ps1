# Znajdź wszystkie pliki .py, ale pomijając wszystkie foldery zawierające 'venv'
$files = Get-ChildItem -Path . -Filter "*.py" -Recurse |
    Where-Object { $_.FullName -notmatch "venv" }

# Zlicz linie w każdym pliku
$totalLines = 0
$fileCount = 0

foreach ($file in $files) {
    $lines = (Get-Content $file.FullName | Where-Object { $_.Trim() -ne "" -and -not $_.Trim().StartsWith("#") }).Count
    Write-Host "$($file.Name): $lines lines"
    $totalLines += $lines
    $fileCount++
}

Write-Host "`nTotal files: $fileCount"
Write-Host "Total lines of code: $totalLines"