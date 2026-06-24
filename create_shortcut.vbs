' Create Desktop Shortcut for Bharat AI School V6
Set WshShell = CreateObject("WScript.Shell")
strDesktop = WshShell.SpecialFolders("Desktop")
strProjectPath = "C:\Users\pc\Desktop\gurjas ai\bharat_ai_school_v6"

' Create shortcut
Set oShortcut = WshShell.CreateShortcut(strDesktop & "\Bharat AI School V6.lnk")
oShortcut.TargetPath = strProjectPath & "\START_HERE.bat"
oShortcut.WorkingDirectory = strProjectPath
oShortcut.Description = "Bharat AI School V6 — ₹20/माह में AI सीखें"
oShortcut.IconLocation = "%SystemRoot%\System32\imageres.dll, 194"
oShortcut.WindowStyle = 1
oShortcut.Save

' Also create a desktop folder shortcut for easy access
Set oFolder = WshShell.CreateShortcut(strDesktop & "\Bharat AI School - Files.lnk")
oFolder.TargetPath = strProjectPath
oFolder.Description = "Bharat AI School V6 Project Files"
oFolder.IconLocation = "%SystemRoot%\System32\imageres.dll, 3"
oFolder.WindowStyle = 1
oFolder.Save

MsgBox "✅ Desktop shortcut create ho gaya!" & vbCrLf & vbCrLf & "Double-click karein 'Bharat AI School V6' icon ko. App automatically khul jayegi!", vbInformation, "Bharat AI School V6"
