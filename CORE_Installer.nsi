; CORE v3.5 - NSIS Installer Script
; ====================================

!define APP_NAME "CORE"
!define APP_VERSION "3.5"
!define APP_PUBLISHER "Your Company"
!define APP_URL "https://yourwebsite.com"
!define APP_EXE "CORE.exe"

; Installer özellikleri
Name "${APP_NAME} v${APP_VERSION}"
OutFile "CORE_v${APP_VERSION}_Setup.exe"
InstallDir "$PROGRAMFILES\${APP_NAME}"
InstallDirRegKey HKLM "Software\${APP_NAME}" "InstallDir"
RequestExecutionLevel admin

; Modern UI
!include "MUI2.nsh"

; UI Ayarları
!define MUI_ABORTWARNING
!define MUI_ICON "CORE_LOGO.ico"
!define MUI_UNICON "CORE_LOGO.ico"

; Sayfa tanımları
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Kaldırma sayfaları
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

; Dil
!insertmacro MUI_LANGUAGE "Turkish"

; Installer bölümü
Section "CORE Uygulaması" SecMain
    SetOutPath "$INSTDIR"
    
    ; Dosyaları kopyala
    File "dist\CORE.exe"
    File "CORE_LOGO.png"
    
    ; Başlat menüsü kısayolu
    CreateDirectory "$SMPROGRAMS\${APP_NAME}"
    CreateShortcut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}"
    CreateShortcut "$SMPROGRAMS\${APP_NAME}\Kaldır.lnk" "$INSTDIR\Uninstall.exe"
    
    ; Masaüstü kısayolu
    CreateShortcut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}"
    
    ; Registry kayıtları
    WriteRegStr HKLM "Software\${APP_NAME}" "InstallDir" "$INSTDIR"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayName" "${APP_NAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "UninstallString" "$INSTDIR\Uninstall.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayVersion" "${APP_VERSION}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "Publisher" "${APP_PUBLISHER}"
    
    ; Uninstaller oluştur
    WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd

; Kaldırma bölümü
Section "Uninstall"
    ; Dosyaları sil
    Delete "$INSTDIR\${APP_EXE}"
    Delete "$INSTDIR\CORE_LOGO.png"
    Delete "$INSTDIR\Uninstall.exe"
    
    ; Kısayolları sil
    Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\${APP_NAME}\Kaldır.lnk"
    RMDir "$SMPROGRAMS\${APP_NAME}"
    Delete "$DESKTOP\${APP_NAME}.lnk"
    
    ; Klasörü sil
    RMDir "$INSTDIR"
    
    ; Registry temizle
    DeleteRegKey HKLM "Software\${APP_NAME}"
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
SectionEnd
