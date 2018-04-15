Add-Type -AssemblyName Microsoft.Office.Interop.Excel
$xlFixedFormat = [Microsoft.Office.Interop.Excel.XlFileFormat]::xlOpenXMLWorkbook
"write-host $xlFixedFormat"
$excel = New-Object -ComObject excel.application
$excel.visible = $true
$folderpath = $PSScriptRoot
$filetype ="*.xls"
Get-ChildItem -Path $folderpath -Include $filetype -recurse | 
ForEach-Object {
	$path = ($_.fullname).substring(0, ($_.FullName).lastindexOf("."))
	
	"Converting $path"
	$workbook = $excel.workbooks.open($_.fullname)
	$worksheet = $workbook.worksheets.item(1)
	$worksheet.name = "Data"

	$path += ".xlsx"
	$workbook.saveas($path, $xlFixedFormat)
	$workbook.close()	
	
	$_.Delete()
}
$excel.Quit()
$excel = $null
[gc]::collect()
[gc]::WaitForPendingFinalizers()