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
        attribute walletRecoverySecretsEncrypted : Boolean = true;
        attribute walletSecretsMaskedByDefault : Boolean = true;
        attribute walletSecretRevealOrCopyRequiresExplicitAction : Boolean = true;
    }

    // Conceptual data type only. Its realization as a Vault record or a separate logical module is deferred in ADR-0003.
    part def CryptoWalletRecord {
        attribute hasUserProvidedMetadata : Boolean;
        attribute hasUserProvidedSeedPhrase : Boolean;
        attribute hasUserProvidedPrivateKey : Boolean;
        attribute sensitiveSecretsEncrypted : Boolean = true;
        attribute sensitiveSecretsMaskedByDefault : Boolean = true;
    }

    part def GuardianBackupFile {
        attribute encrypted : Boolean = true;
        attribute format : String = "Guardian";
        attribute credential : String = "Guardian master password";
        attribute includesWalletSecrets : Boolean = true;
        attribute additionalEncryptionLayer : String = "Optional; pending security design";
    }

    part def PasswordGenerator;
    part def ExternalTOTPManager;

    part def GuardianDesktopApplication {
        attribute targetOperatingSystem : String = "Windows 10 and later";
        attribute unlockFactors : String = "Guardian master password + FIDO2/WebAuthn USB security key";
        attribute blockchainAccessEnabled : Boolean = false;

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
        doc /* REQ-FUNC-008 and REQ-SEC-006: portable encrypted Guardian backup includes protected wallet secrets. */
        subject system : GuardianDesktopApplication;
        require constraint backupIsEncrypted {
            system.backup.encrypted == true and system.backup.includesWalletSecrets == true
        }
    }

    requirement def GuardianWalletSecretProtection {
        doc /* REQ-FUNC-011 and REQ-SEC-006: wallet recovery secrets are encrypted in the local vault. */
        subject system : GuardianDesktopApplication;
        require constraint walletSecretsEncrypted {
            system.vault.walletRecoverySecretsEncrypted == true
        }
    }

    requirement def GuardianNoBlockchainOperations {
        doc /* REQ-INT-004: Guardian 1.0 has no blockchain/RPC access or on-chain operations. */
        subject system : GuardianDesktopApplication;
        require constraint blockchainAccessDisabled {
            system.blockchainAccessEnabled == false
        }
    }

    requirement def GuardianExplicitWalletSecretAction {
        doc /* REQ-FUNC-012: wallet recovery secrets are masked and require an explicit user action to reveal or copy. */
        subject system : GuardianDesktopApplication;
        require constraint explicitRevealOrCopy {
            system.vault.walletSecretsMaskedByDefault == true and system.vault.walletSecretRevealOrCopyRequiresExplicitAction == true
        }
    }
}
