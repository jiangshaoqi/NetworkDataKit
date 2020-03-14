# automatically generate ping_file and traceRoute_file
# ping_date_time.txt and traceRoute_data_time.txt

# read each website website.txt file and output to ping_file and traceRoute_file
$website_num = (Get-Content .\website.txt | Measure-Object -Line).Lines
for($i = 0; $i -lt $website_num; $i ++)
{
    $site = (Get-Content -Path .\website.txt)[$i]
    Test-Connection -ComputerName $site > ping_file
    Test-NetConnection -ComputerName $site -TraceRoute > traceRoute_file
}