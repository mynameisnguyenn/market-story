' One-click launch with no console to babysit: runs the .bat minimized (not hidden, so a
' stuck server is still findable in the taskbar). Point your Desktop shortcut at THIS file.
Set fso = CreateObject("Scripting.FileSystemObject")
Set sh = CreateObject("WScript.Shell")
projectDir = fso.GetParentFolderName(WScript.ScriptFullName)
sh.CurrentDirectory = projectDir
sh.Run """" & projectDir & "\Launch Market Story.bat""", 7, False   ' 7 = minimized window
