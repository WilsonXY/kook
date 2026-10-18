# Export a PowerPoint deck (.ppt or .pptx) to one PNG per slide plus all its text, using PowerPoint itself.
# Windows with PowerPoint installed only; for PDFs use export_pdf.py.
#
#   powershell -ExecutionPolicy Bypass -File export_slides.ps1 -Deck "Lecture 1.pptx" -OutDir ..\_source\ch01
#
# Writes slide_01.png, slide_02.png, ... and slides.txt ("=== Slide N ===" blocks: titles, body text,
# table cells as "a | b | c" rows, grouped shapes, and speaker notes).
param(
    [Parameter(Mandatory = $true)][string]$Deck,
    [string]$OutDir = "",
    [int]$Width = 1600
)
$ErrorActionPreference = "Stop"
$deckPath = (Resolve-Path $Deck).Path
if (-not $OutDir) {
    $OutDir = Join-Path (Split-Path $deckPath) ([IO.Path]::GetFileNameWithoutExtension($deckPath) + "_export")
}
New-Item -ItemType Directory -Force $OutDir | Out-Null
$OutDir = (Resolve-Path $OutDir).Path

function Get-ShapeText($shape) {
    $lines = @()
    if ($shape.Type -eq 6) {  # msoGroup
        foreach ($item in $shape.GroupItems) { $lines += Get-ShapeText $item }
        return $lines
    }
    if ($shape.HasTable) {
        $t = $shape.Table
        for ($r = 1; $r -le $t.Rows.Count; $r++) {
            $cells = @()
            for ($c = 1; $c -le $t.Columns.Count; $c++) {
                $cells += ($t.Cell($r, $c).Shape.TextFrame.TextRange.Text -replace "\s+", " ").Trim()
            }
            $lines += ($cells -join " | ")
        }
        return $lines
    }
    if ($shape.HasTextFrame -and $shape.TextFrame.HasText) {
        $lines += ($shape.TextFrame.TextRange.Text -replace "`r", "`n")
    }
    return $lines
}

$app = New-Object -ComObject PowerPoint.Application
try {
    # ReadOnly, Untitled, WithWindow = false
    $pres = $app.Presentations.Open($deckPath, $true, $false, $false)
    $height = [int]($Width * $pres.PageSetup.SlideHeight / $pres.PageSetup.SlideWidth)
    $sb = New-Object System.Text.StringBuilder
    foreach ($slide in $pres.Slides) {
        $n = $slide.SlideIndex
        $slide.Export((Join-Path $OutDir ("slide_{0:D2}.png" -f $n)), "PNG", $Width, $height)
        [void]$sb.AppendLine("=== Slide $n ===")
        foreach ($shape in $slide.Shapes) {
            foreach ($line in (Get-ShapeText $shape)) { if ($line.Trim()) { [void]$sb.AppendLine($line.Trim()) } }
        }
        try {
            $notes = $slide.NotesPage.Shapes.Placeholders(2).TextFrame.TextRange.Text
            if ($notes.Trim()) { [void]$sb.AppendLine("[notes] " + $notes.Trim()) }
        } catch { }
        [void]$sb.AppendLine("")
    }
    $count = $pres.Slides.Count
    $pres.Close()
    [IO.File]::WriteAllText((Join-Path $OutDir "slides.txt"), $sb.ToString(), (New-Object System.Text.UTF8Encoding $false))
    Write-Output "Exported $count slides to $OutDir"
} finally {
    $app.Quit()
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($app)
}
