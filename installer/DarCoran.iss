#define MyAppName "Dar Coran"
#define MyAppVersion GetEnv("version")
#define MyAppPublisher "Dar Coran"
#define MyAppExeName "Gestion.exe"

[Setup]
AppId={{YOUR-GUID-HERE}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={autopf}\Dar Coran
DefaultGroupName=Dar Coran

OutputDir=installer_output
OutputBaseFilename=DarCoran-Setup

SetupIconFile=..\icon.ico

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