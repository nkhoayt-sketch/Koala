param (
    [int]$Port = 5500
)

$hostUrl = "http://localhost:$Port/"
$rootDir = $PSScriptRoot
if (-not $rootDir) { $rootDir = Get-Location }

$mimeTypes = @{
    ".html" = "text/html; charset=utf-8"
    ".htm"  = "text/html; charset=utf-8"
    ".css"  = "text/css; charset=utf-8"
    ".js"   = "application/javascript; charset=utf-8"
    ".json" = "application/json; charset=utf-8"
    ".png"  = "image/png"
    ".jpg"  = "image/jpeg"
    ".jpeg" = "image/jpeg"
    ".svg"  = "image/svg+xml"
    ".ico"  = "image/x-icon"
    ".txt"  = "text/plain; charset=utf-8"
    ".mp3"  = "audio/mpeg"
    ".wav"  = "audio/wav"
}

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add($hostUrl)

try {
    $listener.Start()
} catch {
    # If 5500 is busy, try 8080
    $Port = 8080
    $hostUrl = "http://localhost:$Port/"
    $listener = New-Object System.Net.HttpListener
    $listener.Prefixes.Add($hostUrl)
    $listener.Start()
}

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  N1 Quiz Web Server dang chay thanh cong!" -ForegroundColor Green
Write-Host "  Dia chi truy cap: $hostUrl" -ForegroundColor Yellow
Write-Host "  Thu muc goc:     $rootDir" -ForegroundColor Gray
Write-Host "  Nhan Ctrl + C de dung server." -ForegroundColor DarkGray
Write-Host "========================================================" -ForegroundColor Cyan

try {
    while ($listener.IsListening) {
        $context = $listener.GetContext()
        $request = $context.Request
        $response = $context.Response

        $urlPath = $request.Url.LocalPath.TrimStart('/')
        if ([string]::IsNullOrWhiteSpace($urlPath)) {
            $urlPath = "index.html"
        }

        # Prevent directory traversal
        $urlPath = $urlPath.Replace('/', [System.IO.Path]::DirectorySeparatorChar)
        $filePath = [System.IO.Path]::Combine($rootDir, $urlPath)

        # CORS header
        $response.Headers.Add("Access-Control-Allow-Origin", "*")

        if ([System.IO.File]::Exists($filePath)) {
            $ext = [System.IO.Path]::GetExtension($filePath).ToLower()
            $mime = "application/octet-stream"
            if ($mimeTypes.ContainsKey($ext)) {
                $mime = $mimeTypes[$ext]
            }

            $response.ContentType = $mime
            $response.Headers.Add("Accept-Ranges", "bytes")

            # Prevent caching for JS and JSON files so browsers always load latest version
            if ($ext -eq ".js" -or $ext -eq ".json") {
                $response.Headers.Add("Cache-Control", "no-cache, no-store, must-revalidate")
                $response.Headers.Add("Pragma", "no-cache")
                $response.Headers.Add("Expires", "0")
            }

            try {
                $fileInfo = New-Object System.IO.FileInfo($filePath)
                $fileLen = $fileInfo.Length

                if ($request.HttpMethod -eq "HEAD") {
                    $response.StatusCode = 200
                    $response.ContentLength64 = $fileLen
                } else {
                    $rangeHeader = $request.Headers["Range"]
                    if ($rangeHeader -and $rangeHeader.StartsWith("bytes=")) {
                        $rangeParts = $rangeHeader.Substring(6).Split("-")
                        $start = [int64]$rangeParts[0]
                        $end = $fileLen - 1
                        if ($rangeParts.Length -gt 1 -and -not [string]::IsNullOrWhiteSpace($rangeParts[1])) {
                            $end = [int64]$rangeParts[1]
                        }
                        $length = $end - $start + 1
                        $response.StatusCode = 206
                        $response.Headers.Add("Content-Range", "bytes $start-$end/$fileLen")
                        $response.ContentLength64 = $length
                        
                        $fs = [System.IO.File]::OpenRead($filePath)
                        $fs.Seek($start, [System.IO.SeekOrigin]::Begin) | Out-Null
                        $buffer = New-Object byte[] 65536
                        $bytesToRead = $length
                        while ($bytesToRead -gt 0) {
                            $chunk = [Math]::Min($bytesToRead, $buffer.Length)
                            $read = $fs.Read($buffer, 0, $chunk)
                            if ($read -le 0) { break }
                            $response.OutputStream.Write($buffer, 0, $read)
                            $bytesToRead -= $read
                        }
                        $fs.Close()
                    } else {
                        $response.StatusCode = 200
                        $response.ContentLength64 = $fileLen
                        $fs = [System.IO.File]::OpenRead($filePath)
                        $fs.CopyTo($response.OutputStream)
                        $fs.Close()
                    }
                }
            } catch {
                $response.StatusCode = 500
            }
        } else {
            $response.StatusCode = 404
            $notFoundBytes = [System.Text.Encoding]::UTF8.GetBytes("404 Not Found: $urlPath")
            $response.ContentLength64 = $notFoundBytes.Length
            $response.OutputStream.Write($notFoundBytes, 0, $notFoundBytes.Length)
        }

        $response.Close()
    }
} finally {
    if ($listener.IsListening) {
        $listener.Stop()
    }
    $listener.Close()
}
