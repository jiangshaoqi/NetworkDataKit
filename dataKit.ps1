# automatically generate ping_file and traceRoute_file
# ping_date_time.txt and traceRoute_data_time.txt
$ping_name = "ping" + (Get-Date -DisplayHint Date -Format "MM_dd_yyyy") + ".txt"
$traceRoute_name = "traceRoute" + (Get-Date -DisplayHint Date -Format "MM_dd_yyyy") + ".txt"

# read each website website.txt file and output to ping_file and traceRoute_file
Test-Connection -ComputerName (Get-Content -Path .\website.txt)[0] > $ping_name
Test-NetConnection -ComputerName (Get-Content -Path .\website.txt)[0] -TraceRoute > $traceRoute_name
$website_num = (Get-Content .\website.txt | Measure-Object -Line).Lines
for($i = 1; $i -lt $website_num; $i ++)
{
    $site = (Get-Content -Path .\website.txt)[$i]
    Test-Connection -ComputerName $site >> $ping_name
    Test-NetConnection -ComputerName $site -TraceRoute >> $traceRoute_name
}