#define MyAppName "Dar Coran"
#ifndef MyAppVersion
  #error "MyAppVersion is not defined. Compile with /DMyAppVersion=x.y.z"
#endif
#define MyAppPublisher "Yahia Boukharrata"
#define MyAppExeName "Gestion.exe"
#define AppGUID "053dbfa0-767d-4e58-a27a-77c8b2665426"

[Setup]
AppId={#AppGUID}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={autopf}\Dar Coran
DefaultGroupName=Dar Coran

OutputDir=installer_output
OutputBaseFilename=DarCoran-Setup

SetupIconFile=..\icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

Compression=lzma
SolidCompression=yes

WizardStyle=modern

ArchitecturesInstallIn64BitMode=x64compatible

[Files]
Source: "..\dist\Gestion.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Dar Coran"; Filename: "{app}\Gestion.exe"
Name: "{autodesktop}\Dar Coran"; Filename: "{app}\Gestion.exe"

[Run]
Filename: "{app}\Gestion.exe"; \
    Description: "Launch Dar Coran"; \
    Flags: nowait postinstall skipifsilent