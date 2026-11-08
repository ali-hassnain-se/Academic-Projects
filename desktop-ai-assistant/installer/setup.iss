; Inno Setup script for Desktop AI Assistant
; Build:  open this file in "Inno Setup Compiler" and press Ctrl+F9
;         (or run:  ISCC.exe installer\setup.iss)
; Needs the folder  dist\DesktopAIAssistant  (made by installer\build.bat)
; Output:  dist\installer\DesktopAIAssistant-Setup.exe

#define MyAppName "Desktop AI Assistant"
#define MyAppVersion "1.0.0"
#define MyAppExeName "DesktopAIAssistant.exe"

[Setup]
; AppId must stay the same in every version (it identifies the app for upgrades/uninstall).
; Make your own with Inno Setup: Tools > Generate GUID.
AppId={{8F3C2A1E-5B7D-4C9A-9E21-6D4F0A7B3C58}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
DefaultDirName={autopf}\DesktopAIAssistant
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
; Installs for the current user only: no administrator password needed.
PrivilegesRequired=lowest
OutputDir=..\dist\installer
OutputBaseFilename=DesktopAIAssistant-Setup
SetupIconFile=..\assets\icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Shortcuts:"; Flags: unchecked
Name: "autostart"; Description: "Start with &Windows"; GroupDescription: "Options:"; Flags: unchecked

[Files]
Source: "..\dist\DesktopAIAssistant\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Registry]
; Same value name as assistant/system/autostart.py (_NAME), removed again on uninstall.
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "DesktopAIAssistant"; ValueData: """{app}\{#MyAppExeName}"""; Flags: uninsdeletevalue; Tasks: autostart

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent
