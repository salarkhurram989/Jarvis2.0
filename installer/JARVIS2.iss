; JARVIS 2.0 Windows installer
#define MyAppName "JARVIS 2.0"
#define MyAppVersion "2.0.0"
#define MyAppPublisher "Salar Khurram"
#define MyAppExeName "JARVIS2.exe"

[Setup]
AppId={{8B0B1B8C-0A65-4B4C-9A5E-2F4B7C1D2A90}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\JARVIS 2.0
DefaultGroupName={#MyAppName}
OutputDir=..\installer
OutputBaseFilename=JARVIS-Setup
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
WizardStyle=modern
PrivilegesRequired=admin
UninstallDisplayName={#MyAppName}
Uninstallable=yes

[Files]
Source: "..\dist\JARVIS2.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\JARVIS 2.0"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\JARVIS 2.0"; Filename: "{app}\{#MyAppExeName}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch JARVIS 2.0"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: files; Name: "{app}\JARVIS2.exe"
