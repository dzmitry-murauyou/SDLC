package GuardianModel {
    port def UserInterfacePort;
    port def FIDO2AuthenticationPort;
    port def BrowserAutofillPort;
    port def BackupFilePort;
    port def WindowsIntegrationPort;

    part def GuardianUser {
        port ui : UserInterfacePort;
    }

    part def Windows10OrLaterEnvironment {
        port integration : WindowsIntegrationPort;
    }

    part def FIDO2WebAuthnUSBKey {
        port authentication : FIDO2AuthenticationPort;
    }

    part def WindowsBrowser {
        port autofill : BrowserAutofillPort;
    }

    part def RemovableStorage {
        port backupFile : BackupFilePort;
    }

    part def EncryptedVault {
        attribute encrypted : Boolean = true;
    }

    part def GuardianBackupFile {
        attribute encrypted : Boolean = true;
        attribute format : String = "Guardian";
        attribute credential : String = "Guardian master password";
        attribute additionalEncryptionLayer : String = "Optional; pending security design";
    }

    part def PasswordGenerator;
    part def ExternalTOTPManager;

    part def GuardianDesktopApplication {
        attribute targetOperatingSystem : String = "Windows 10 and later";
        attribute unlockFactors : String = "Guardian master password + FIDO2/WebAuthn USB security key";

        port ui : UserInterfacePort;
        port keyAuthentication : FIDO2AuthenticationPort;
        port browserAutofill : BrowserAutofillPort;
        port backupExport : BackupFilePort;
        port windowsIntegration : WindowsIntegrationPort;

        part vault : EncryptedVault;
        part passwordGenerator : PasswordGenerator;
        part externalTOTP : ExternalTOTPManager;
        part backup : GuardianBackupFile;
    }

    part user : GuardianUser;
    part windows : Windows10OrLaterEnvironment;
    part securityKey : FIDO2WebAuthnUSBKey;
    part browser : WindowsBrowser;
    part removableStorage : RemovableStorage;
    part guardian : GuardianDesktopApplication;

    connect user.ui to guardian.ui;
    connect securityKey.authentication to guardian.keyAuthentication;
    connect guardian.browserAutofill to browser.autofill;
    connect guardian.backupExport to removableStorage.backupFile;
    connect windows.integration to guardian.windowsIntegration;

    requirement def GuardianTwoFactorUnlock {
        doc /* REQ-FUNC-010: master password and enrolled FIDO2/WebAuthn USB key are required to unlock Guardian. */
        subject system : GuardianDesktopApplication;
        require constraint fido2KeyRequired {
            system.unlockFactors == "Guardian master password + FIDO2/WebAuthn USB security key"
        }
    }

    requirement def GuardianEncryptedBackup {
        doc /* REQ-FUNC-008: portable Guardian-format backup, encrypted with the Guardian master password. */
        subject system : GuardianDesktopApplication;
        require constraint backupIsEncrypted {
            system.backup.encrypted == true
        }
    }
}
