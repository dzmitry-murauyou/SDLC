# Software Requirements Specification
## For Guardian — Password Manager

Version 0.1  
Prepared by Not specified  
Organization not specified  
2026-10-26

## Table of Contents
<!-- TOC -->
* [1. Introduction](#1-introduction)
    * [1.1 Document Purpose](#11-document-purpose)
    * [1.2 Product Scope](#12-product-scope)
    * [1.3 Definitions, Acronyms, and Abbreviations](#13-definitions-acronyms-and-abbreviations)
    * [1.4 References](#14-references)
    * [1.5 Document Overview](#15-document-overview)
* [2. Product Overview](#2-product-overview)
    * [2.1 Product Perspective](#21-product-perspective)
    * [2.2 Product Functions](#22-product-functions)
    * [2.3 Product Constraints](#23-product-constraints)
    * [2.4 User Characteristics](#24-user-characteristics)
    * [2.5 Assumptions and Dependencies](#25-assumptions-and-dependencies)
    * [2.6 Apportioning of Requirements](#26-apportioning-of-requirements)
* [3. Requirements](#3-requirements)
    * [3.1 External Interfaces](#31-external-interfaces)
    * [3.2 Functional](#32-functional)
    * [3.3 Quality of Service](#33-quality-of-service)
    * [3.4 Compliance](#34-compliance)
    * [3.5 Design and Implementation](#35-design-and-implementation)
    * [3.6 AI/ML](#36-aiml)
* [4. Verification](#4-verification)
* [5. Appendixes](#5-appendixes)
<!-- TOC -->

## Revision History

| Name | Date | Reason For Changes | Version |
|------|------|--------------------|---------|
| Not specified | 2026-10-26 | Initial SRS draft for Guardian | 0.1 |

## 1. Introduction

This document specifies the requirements for Guardian, an application for securely managing passwords and related secrets. It defines the intended capabilities, first-release boundaries, constraints, quality attributes, and verification methods; it does not prescribe the internal architecture except for the explicit requirement to use Java. The document is intended for the product owner, developers, testers, and security specialists. Unknown parameters are identified as assumptions or decisions requiring confirmation.

### 1.1 Document Purpose

This SRS defines **what** Guardian must do and the criteria for accepting the result. The product owner uses it to agree on scope; developers use it for design and implementation; QA and security specialists use it to prepare verification and analyze risks. Architectural decisions and specific cryptographic parameters must be documented separately and are not established by this document.

### 1.2 Product Scope

Guardian (release 1.0) is a password manager intended to create and securely store credentials, organize them into categories, and use them safely to sign in to supported services. Users will be able to create records containing a username, password, website address, notes, and optional TOTP secrets; find and edit records; generate strong passwords; and initiate autofill. Access to the vault is protected by a master password, and secrets must be encrypted at rest. The application must be implemented using Java.

**In scope:** a secure local vault for one user; password and note records; categories and search; a password generator; autofill in explicitly supported environments; storage of TOTP secrets and generation of one-time codes; vault locking; and backup of encrypted data.

**Out of scope for release 1.0:** team/shared vaults, server-side synchronization across devices, enterprise administration, operator-assisted master-password recovery, importing passwords from arbitrary applications, AI-based features, and guarantees of compliance with any specific legislation. The platforms on which the application and autofill will be available must be agreed before interface design.

### 1.3 Definitions, Acronyms, and Abbreviations

| Term | Definition |
|---|---|
| Autofill | Transfer of credentials selected by the user into a login field on a supported website or application. |
| Encrypted vault / vault | A set of user records saved in encrypted form. |
| Master password | A secret set by the user to unlock the vault; it must not be stored in plaintext. |
| TOTP | Time-Based One-Time Password — a one-time code calculated using a secret and the current time. |
| MFA / 2FA | Multi-factor / two-factor authentication; access confirmation using two or more independent factors. |
| SRS | Software Requirements Specification — a specification of software requirements. |
| Java | The programming language and runtime required for Guardian implementation by the original request. |

### 1.4 References

| Title | Owner | Version / Date | Location | Status and Application |
|---|---|---|---|---|
| SRS template | Project repository | Repository version as of 2026-10-26 | `srs/srs-template-en.md` | Informative: structure and preparation guidance. |
| RFC 6238, TOTP: Time-Based One-Time Password Algorithm | IETF | RFC 6238, 2011-05 | https://www.rfc-editor.org/rfc/rfc6238 | Normative for TOTP generation compatibility and test vectors. |
| OWASP Application Security Verification Standard (ASVS) | OWASP Foundation | 5.0.0, 2025 | https://owasp.org/www-project-application-security-verification-standard/ | Informative security checklist; Guardian compliance is not claimed pending a separate assessment. |
| ISO/IEC/IEEE 29148, Systems and software engineering — Requirements engineering | ISO / IEC / IEEE | 29148:2018 | `docs/standards.md` | Informative requirements-engineering reference; formal conformance is not claimed. |
| Java Platform, Standard Edition Documentation | Oracle / OpenJDK | Target JDK release and documentation date to be fixed after release selection | https://docs.oracle.com/en/java/javase/ | Normative after the supported JDK is approved. |

### 1.5 Document Overview

Section 2 defines the product context, user classes, constraints, assumptions, and release allocation. Section 3 contains interface, functional, quality, and implementation requirements; mandatory statements use “shall,” and each requirement has a unique ID and acceptance criteria. Section 4 maps requirements to verification methods and artifacts, while Section 5 records open questions and draft limitations. Changes are approved by the product owner and, where applicable, the security specialist, and are recorded in the revision history.

---

## 2. Product Overview

### 2.1 Product Perspective

Guardian is a new standalone product for an individual user, replacing password storage in notes, browser forms, or spreadsheets. Data is held in a local encrypted vault; autofill interacts only with a browser or application explicitly selected and supported for the release. External account and synchronization services are outside the scope of version 1.0. A product owner and support team must be assigned before release; a network SLA does not apply to the offline application, and support is limited to documentation and diagnostics without support-staff access to secrets.

```text
User ──> Guardian (interface, encrypted vault, generator, TOTP)
                    │
                    └──> Supported browser/application (autofill only)
```

### 2.2 Product Functions

- Create, unlock, lock, and delete a personal vault.
- Add, view, edit, and delete records containing credentials and notes.
- Organize records into user-defined categories and search permitted metadata.
- Generate random passwords using parameters selected by the user.
- Autofill credentials in supported environments after checking the record’s source match.
- Store TOTP secrets and display current one-time codes.
- Prevent accidental disclosure through secret masking, automatic locking, and clipboard clearing.
- Create and restore backups in an encrypted format.

### 2.3 Product Constraints

| ID | Constraint |
|---|---|
| CON-01 | Guardian application logic must be implemented in Java. The target JDK release and supported operating systems remain to be agreed. |
| CON-02 | Vault secret fields must be encrypted when saved; the plaintext master password and decryption key must not be written to files, logs, or telemetry. |
| CON-03 | Autofill is allowed only in environments for which a secure integration mechanism has been defined and verified; the platform list remains an open decision. |
| CON-04 | Release 1.0 does not assume server-side synchronization, vault sharing, or operator-assisted secret recovery. |
| CON-05 | Requirements do not prescribe specific encryption algorithms, a KDF, UI framework, or integration protocol. These must be selected and justified in design documentation using supported cryptographic facilities. |
| CON-06 | Jurisdiction, legal obligations, target devices, and budget are unspecified; applicable requirements must be reviewed before release. |

### 2.4 User Characteristics

| User Class | Skills and Goals | Access |
|---|---|---|
| Vault owner | An ordinary user who wants to create, find, and use secrets without having to remember every password. May not have specialized cryptography knowledge. | Full access to their own vault after unlocking it. |
| Autofill user | Frequently signs in to websites/applications and expects to select an appropriate record without disclosing it to an unrelated source. | Selects and fills a matching record; a secret is revealed only after an explicit action. |
| Support engineer/developer | Maintains the application and diagnoses errors, but must not access user vault contents. | No routine access to user secrets. |

The first release interface and documentation must be available in Russian; the interface structure should allow English localization. Accessibility conformance and platform-specific guidelines must be established after target platforms are selected.

### 2.5 Assumptions and Dependencies

| ID | Assumption / Dependency | Owner | Impact if False | Mitigation / Action |
|---|---|---|---|---|
| A-01 | The first release serves one user and one local vault, without cloud synchronization. | Product owner (to be assigned) | Server architecture, accounts, synchronization, conflict resolution, and a separate threat model will be required. | Confirm scope before architecture approval; track synchronization as a separate change request. |
| A-02 | The user keeps the master password separately and understands that losing it may make data impossible to decrypt. | Product owner / UX (to be assigned) | The user may permanently lose access; operator recovery would increase compromise risk. | Warn users during vault creation and document secure backup practices. |
| A-03 | Guardian runs on a supported, uncompromised device. | User; security team owns threat-model disclosure | Protection against malware, keyloggers, and physical access to an unlocked device cannot be guaranteed. | Document assurance boundaries; perform threat analysis; use automatic locking and minimize secret lifetime in memory. |
| A-04 | Specific browsers/OSs with supported official APIs will be selected for autofill. | Product owner / tech lead (to be assigned) | Interface design, integration testing, and autofill risk assessment cannot be completed. | Approve a platform matrix before implementing integration; autofill remains blocked until then. |
| A-05 | Supported cryptography and random-generation libraries are available for the selected Java runtime and pass license and security reviews. | Tech lead / security specialist (to be assigned) | The platform or feature set may need to change; custom cryptography would introduce unacceptable risk. | Review libraries and licenses during the PoC; do not use custom cryptographic primitives. |
| A-06 | “Two-factor authentication” in release 1.0 means storing TOTP secrets for external accounts; MFA for signing in to Guardian itself is not confirmed. | Product owner (to be assigned) | Authentication scope and UX will change if MFA is required for Guardian itself. | Confirm interpretation before design; track in the open questions in Section 5.1. |
| A-07 | The user's device provides system time accurate enough for TOTP calculation. | User / platform-integration owner | Generated codes may be rejected by the external service when the device clock is wrong. | Indicate device-time status or warn the user about clock drift; determine the exact mechanism after platform selection. |

### 2.6 Apportioning of Requirements

| Area / Requirements | Subsystem or Increment | Status |
|---|---|---|
| REQ-FUNC-001–005, REQ-FUNC-008–009 | Release 1.0: local vault, records, categories, generation, notes, backup, and locking | Planned |
| REQ-FUNC-006–007, REQ-INT-003 | Release 1.0: autofill and TOTP, subject to selection of a supported platform | Platform to be confirmed |
| REQ-SEC-001–005, REQ-REL-001–002 | Release 1.0: baseline data protection and recovery | Mandatory for release |
| REQ-INT-001–003, REQ-PERF-001–002, REQ-OBS-001 | Release 1.0: interface, integration, and measurable QoS | Planned; target devices to be confirmed |
| REQ-AVAIL-001, REQ-COMP-001–002, REQ-INST-001, REQ-BUILD-001, REQ-MAINT-001, REQ-PORT-001, REQ-POC-001, REQ-CM-001 | Release 1.0: release readiness, operations, and proof of feasibility | Project decisions required |
| Synchronization, sharing, enterprise management, AI | Potential future releases | Out of scope for release 1.0; separate change requests |

Platform allocations, dates, and budget remain product-owner decisions; until confirmed, they are tracked as open questions in Section 5.1 and are not release commitments. An owner shall be assigned to each deferred requirement when the corresponding increment is planned.

---

## 3. Requirements

Requirements shall be verifiable, unambiguous, and uniquely identified. “Shall” and “shall not” are mandatory for release 1.0 unless a requirement is marked as awaiting agreement. Performance and timer values in this draft are targets and must be confirmed on target devices before the requirements baseline is approved.

📃 Requirement template:
```markdown
- ID: REQ-FUNC-EXAMPLE
- Title: Short requirement title
- Statement: The system shall...
- Rationale: ...
- Acceptance Criteria: ...
- Verification Method: Test | Analysis | Inspection | Demonstration | Other
- More Information: Additional context or links
```

**Identifier scheme:** `REQ-[AREA]-[NNN]-[VER]`, where `-[VER]` is optional; identifiers are unique and immutable. Requirement changes are recorded in the document history. Each test artifact shall reference the applicable requirement ID.

### 3.1 External Interfaces

#### 3.1.1 User Interfaces

The interface shall let users manage the vault, records, categories, generator, and TOTP without manually editing files. Secrets shall be masked by default; revealing or copying them shall require an explicit user action. Errors during unlock, save, import/export, and autofill shall explain what happened without displaying secret values. Exact screens and platform-specific flows will be specified in a separate UX specification after target operating systems are selected.

#### 3.1.2 Hardware Interfaces

No specialized hardware is required. Installation shall run on devices that meet the minimum requirements of the selected Java runtime and target operating system. If autofill on a platform requires system integration or a biometric sensor, that dependency shall be stated explicitly and shall not be mandatory for vault access unless separately agreed.

#### 3.1.3 Software Interfaces

- Interaction with a browser or operating system for autofill is permitted only through an officially supported interface of the selected platform.
- The record format shall support a title, username, password, URL/source identifier, categories, notes, and optional TOTP data.
- An external network API, cloud synchronization, and third-party analytics SDKs are outside the scope of version 1.0.

```markdown
- ID: REQ-INT-001
- Title: Secret-management interface
- Statement: The user interface shall mask secret values by default and require an explicit user action to reveal, copy, or autofill a secret.
- Rationale: Prevents accidental disclosure during ordinary navigation.
- Acceptance Criteria: Passwords and TOTP secrets are not displayed in record lists; revealing/copying requires a separate action; interface errors contain no secret values.
- Verification Method: Inspection, functional test.
- More Information: CON-02; related: REQ-SEC-002.
```

```markdown
- ID: REQ-INT-002
- Title: External integration restrictions
- Statement: In release 1.0, the system shall not transmit vault data to external network services; browser or operating-system integration is permitted only for user-initiated autofill.
- Rationale: Preserves the product’s local nature and limits the data-leak surface.
- Acceptance Criteria: Network-traffic analysis detects no outbound requests containing vault data; all permitted integration calls are related to documented autofill flows.
- Verification Method: Traffic analysis, inspection.
- More Information: CON-04; related: REQ-AVAIL-001.
```

```markdown
- ID: REQ-INT-003
- Title: Secure autofill integration
- Statement: Integration with the selected browser or operating system shall transfer only fields from the record selected by the user to an explicitly confirmed target context.
- Rationale: Limits the data available to an external application.
- Acceptance Criteria: An integration test confirms that only selected fields are transferred and that unsupported or mismatched contexts are rejected.
- Verification Method: Integration test, demonstration.
- More Information: CON-03; related: REQ-FUNC-006, REQ-SEC-005.
```

### 3.2 Functional

```markdown
- ID: REQ-FUNC-001
- Title: Vault creation and unlock
- Statement: The system shall allow the user to create a vault, set a master password, and unlock the vault only after validating the entered secret.
- Rationale: The master password is the primary user method of accessing data.
- Acceptance Criteria: Records are available with the correct secret; with an incorrect secret, secret fields are not revealed and the application displays a neutral error message; the master password is not stored in plaintext.
- Verification Method: Test, analysis.
- More Information: CON-02, CON-05; related: REQ-SEC-001, REQ-SEC-002.
```

```markdown
- ID: REQ-FUNC-002
- Title: Record management
- Statement: The system shall allow the user to add, view, edit, and delete a record containing a title, username, password, URL or other source identifier, and user-defined additional fields.
- Rationale: This is the core password-manager workflow.
- Acceptance Criteria: Saved changes persist after the application is closed and reopened; a deleted record is not displayed in the normal list; save failures do not cause partial or silent data loss.
- Verification Method: Functional test.
- More Information: CON-02; related: REQ-REL-001.
```

```markdown
- ID: REQ-FUNC-003
- Title: Categories, filtering, and search
- Statement: The system shall allow the user to assign records to user-defined categories and find records by title, username, category, or source address.
- Rationale: Categorization simplifies management of a growing vault.
- Acceptance Criteria: A category can be created, renamed, assigned, and deleted; deleting a category does not delete records; search results match the query and do not expose passwords.
- Verification Method: Functional test.
- More Information: CON-02.
```

```markdown
- ID: REQ-FUNC-004
- Title: Password generation
- Statement: The system shall generate a password from 8 to 128 characters long using user-selected character classes and a cryptographically secure random source provided by the Java runtime.
- Rationale: Random, unique passwords reduce guessing and reuse risks.
- Acceptance Criteria: The user can set the length and enable lowercase, uppercase, numeric, and special characters; if a class is selected, the result contains at least one character from each selected class; lengths 8 and 128 are supported and values outside the range are rejected; incompatible settings produce a clear error; testing confirms that no predictable random source is used.
- Verification Method: Test, analysis.
- More Information: CON-01; related: REQ-POC-001.
```

```markdown
- ID: REQ-FUNC-005
- Title: Secure notes
- Statement: The system shall allow users to create and edit notes containing text related to the vault and shall store them with the same confidentiality protection as other secret data.
- Rationale: Users may need to protect information that is not a username or password.
- Acceptance Criteria: A note is available only after unlock; its contents do not appear in logs, external system search suggestions, or plaintext vault files.
- Verification Method: Functional test, inspection.
- More Information: CON-02; related: REQ-SEC-001, REQ-OBS-001.
```

```markdown
- ID: REQ-FUNC-006
- Title: Safe autofill
- Statement: The system shall offer autofill only for a record explicitly selected by the user and only when the scheme, host name, and effective port match the saved source; navigation to another source shall require revalidation.
- Rationale: Autofill must not send secrets to a lookalike or unrelated website.
- Acceptance Criteria: An exact source match is allowed; a lookalike domain, different port or scheme, or ambiguous URL is rejected; subdomains are not treated as matches automatically; filling occurs only after explicit user selection and the source is revalidated after redirects.
- Verification Method: Integration and negative testing.
- More Information: CON-03; related: REQ-INT-003, REQ-SEC-005.
```

```markdown
- ID: REQ-FUNC-007
- Title: TOTP codes for saved accounts
- Statement: The system shall allow the user to add a TOTP secret to a record and shall display the current one-time code, its remaining validity time, and non-default algorithm parameters.
- Rationale: The user requested two-factor authentication support for external accounts.
- Acceptance Criteria: RFC 6238 test vectors produce the expected codes; defaults are 6 digits, a 30-second period, and HMAC-SHA-1; explicitly supplied parameters from a QR/otpauth URI or manual entry are supported; the TOTP secret is encrypted at rest and excluded from unencrypted export; remaining validity time is displayed.
- Verification Method: Test, analysis.
- More Information: CON-02; RFC 6238; related: REQ-SEC-001.
```

```markdown
- ID: REQ-FUNC-008
- Title: Backup and restore
- Statement: The system shall allow the user to create a backup of the vault in a protected format and restore it after user confirmation.
- Rationale: This protects against data loss due to failure or reinstallation.
- Acceptance Criteria: The backup does not contain secret fields in plaintext; restoring a valid backup returns records without changing their values; a corrupted or unsupported backup is rejected without overwriting the current vault.
- Verification Method: Test, format inspection.
- More Information: CON-02; related: REQ-SEC-001, REQ-REL-002.
```

```markdown
- ID: REQ-FUNC-009
- Title: Locking and revealing secrets
- Statement: The system shall let users lock the vault immediately, shall mask passwords and notes by default, and shall require an explicit action to reveal a secret temporarily.
- Rationale: This reduces the chance of accidental secret exposure.
- Acceptance Criteria: Record contents are unavailable through the interface after locking; a revealed secret is masked again after a short configured interval or when the record screen is left.
- Verification Method: Functional test.
- More Information: CON-02; related: REQ-SEC-003.
```

### 3.3 Quality of Service

#### 3.3.1 Performance

```markdown
- ID: REQ-PERF-001
- Title: Unlock and search response time
- Statement: On an agreed target device, the system shall unlock a local vault of up to 5,000 records within 3 seconds at the 95th percentile after entry of a correct master password; metadata search shall complete within 500 ms at the 95th percentile.
- Rationale: Provides acceptable responsiveness for everyday use.
- Acceptance Criteria: The metrics are confirmed by a repeatable test on a recorded configuration; measurements do not include artificial network access.
- Verification Method: Load test.
- More Information: Target-device decision is open in Section 5.1.
```

```markdown
- ID: REQ-PERF-002
- Title: Response to user actions
- Statement: For ordinary local operations (opening a record, changing a category, or saving a record), the system shall provide a visible result within 1 second at the 95th percentile on the target device.
- Rationale: Vault-management operations should feel immediate.
- Acceptance Criteria: The metric is measured with up to 5,000 records and a published test configuration.
- Verification Method: Performance test.
- More Information: Target-device decision is open in Section 5.1.
```

#### 3.3.2 Security

```markdown
- ID: REQ-SEC-001
- Title: Vault encryption
- Statement: The system shall encrypt secret fields and backups using current, widely reviewed cryptographic mechanisms from a supported library; the specific algorithms, parameters, and key-management scheme shall be approved in design documentation before release.
- Rationale: Protects data confidentiality when device files or a backup are accessed.
- Acceptance Criteria: Inspection of configuration and format confirms encryption; reading the file without the key does not reveal secret-field contents; no custom cryptographic primitives are used without an approved exception.
- Verification Method: Analysis, inspection.
- More Information: CON-02, CON-05; cryptographic parameters require approval before release.
```

```markdown
- ID: REQ-SEC-002
- Title: Master-password and key protection
- Statement: The system shall not store the master password or decryption key in plaintext, and any derived values shall be stored only in a form approved by a security analysis.
- Rationale: Disclosure of an application or vault file must not directly reveal the access secret.
- Acceptance Criteria: The master password and key are absent from files, logs, crash reports, and telemetry; key-derivation parameters are documented and reviewed by a security specialist.
- Verification Method: Analysis, test.
- More Information: CON-02, CON-05; related: REQ-FUNC-001, REQ-OBS-001.
```

```markdown
- ID: REQ-SEC-003
- Title: Automatic locking
- Statement: The system shall automatically lock an unlocked vault after 5 minutes of inactivity; the user may select an interval from 1 to 15 minutes but shall not disable locking entirely in release 1.0.
- Rationale: Limits the time window in which an unlocked vault can be accessed.
- Acceptance Criteria: The vault locks when the inactivity timer expires; the 1- and 15-minute boundaries are supported and values outside the range are rejected; records remain unavailable until re-authentication.
- Verification Method: Test.
- More Information: CON-02; related: REQ-FUNC-009.
```

```markdown
- ID: REQ-SEC-004
- Title: Clipboard protection
- Statement: If the user copies a password to the clipboard, the system shall clear it within 30 seconds or when the vault is locked, if the platform allows clipboard control.
- Rationale: Reduces the time for which another application can access a secret.
- Acceptance Criteria: On a supported platform, timed clearing and clearing on lock are verified; if the operating system does not permit clearing, the user is warned before copying.
- Verification Method: Integration test, demonstration.
- More Information: CON-02, CON-03; clipboard support depends on the selected platform.
```

```markdown
- ID: REQ-SEC-005
- Title: Autofill source verification
- Statement: The system shall allow autofill only when the scheme, host name, and effective port match the record source; the source shall be revalidated after redirects.
- Rationale: Protects against phishing and inadvertent password disclosure.
- Acceptance Criteria: Exact matches are allowed; lookalike domains, different ports or schemes, unknown domains, and ambiguous URLs are rejected; subdomains are not automatically treated as matches; negative tests confirm rejection in every disallowed case.
- Verification Method: Negative test, analysis.
- More Information: CON-03; related: REQ-FUNC-006, REQ-INT-003.
```

#### 3.3.3 Reliability

```markdown
- ID: REQ-REL-001
- Title: Integrity in case of failure
- Statement: The system shall save vault changes atomically to the extent supported by the selected format, so that an interrupted write does not cause silent loss or alteration of previously saved data.
- Rationale: Vault corruption may cause irrecoverable loss of secrets.
- Acceptance Criteria: An injected interruption during a save does not leave a partially accepted record; the application reports unreadable data and preserves the original file/copy for recovery.
- Verification Method: Fault-tolerance test.
- More Information: CON-02; related: REQ-FUNC-002, REQ-FUNC-008.
```

```markdown
- ID: REQ-REL-002
- Title: Backup validation
- Statement: The system shall validate the integrity and format of a backup before restoration and shall not replace the active vault with unverified data.
- Rationale: Protects against corrupted, tampered, or incompatible backups.
- Acceptance Criteria: Corrupted and incorrectly authenticated backups are rejected; the original vault remains accessible.
- Verification Method: Negative test.
- More Information: CON-02; related: REQ-FUNC-008.
```

#### 3.3.4 Availability

```markdown
- ID: REQ-AVAIL-001
- Title: Offline availability
- Statement: After installation and vault creation, the user shall be able to perform local operations without a network connection.
- Rationale: Passwords should remain available without a network, and the product has no external service dependency in release 1.0.
- Acceptance Criteria: Creation, unlock, search, editing, generation, TOTP, and local backup work in an isolated network; the application does not attempt to send vault contents over an external network.
- Verification Method: Isolated-environment test, network-traffic analysis.
- More Information: CON-04; related: REQ-INT-002.
```

#### 3.3.5 Observability

In release 1.0, remote telemetry, usage analytics, and trace collection are disabled; diagnostics are local and minimal. A diagnostic report may be exported only with the user’s explicit consent.

```markdown
- ID: REQ-OBS-001
- Title: Safe diagnostics
- Statement: The system shall provide local diagnostic messages about failures and operation status without passwords, the master password, TOTP secrets, notes, keys, or plaintext record contents; remote telemetry shall be disabled in release 1.0.
- Rationale: Diagnostics are needed to fix problems, but logs must not become a data-leak channel.
- Acceptance Criteria: Log and report inspection confirms the absence of secrets; URLs and usernames are masked or omitted; network monitoring detects no telemetry; export of a sanitized report requires explicit user consent.
- Verification Method: Inspection, test.
- More Information: CON-02, CON-04; related: REQ-SEC-002.
```

### 3.4 Compliance

```markdown
- ID: REQ-COMP-001
- Title: Dependency and license review
- Statement: Before release, the team shall inventory third-party libraries, record their versions and licenses, and check for known critical vulnerabilities.
- Rationale: Reduces legal and operational risks from dependencies.
- Acceptance Criteria: Each release includes a component list and review results; critical vulnerabilities are not released without documented risk acceptance.
- Verification Method: Release-artifact inspection.
- More Information: CON-06; legal jurisdiction remains an open question in Section 5.1.
```

```markdown
- ID: REQ-COMP-002
- Title: Identify applicable legal requirements
- Statement: Before public release, the product owner shall identify legal and regulatory requirements applicable to target jurisdictions, document applicability, and assign owners for compliance.
- Rationale: Requirements for personal data, consumer notices, accessibility, and software distribution depend on the release market.
- Acceptance Criteria: An approved compliance checklist identifies jurisdictions, applicable requirements, a control owner, and evidence for each control; any requirement deemed inapplicable has a documented rationale.
- Verification Method: Inspection.
- More Information: CON-06; target jurisdictions are an open question in Section 5.1.
```

The jurisdiction and target market are not yet defined. Before public release, the product owner shall identify applicable requirements for personal-data protection, consumer notices, data export and retention, accessibility, licensing, and software distribution; a compliance owner shall record applicability and evidence. This SRS does not claim certification or legal compliance.

### 3.5 Design and Implementation

#### 3.5.1 Installation

```markdown
- ID: REQ-INST-001
- Title: Supported installation
- Statement: A release shall include documented installation steps, Java runtime requirements, and a list of supported operating systems once these have been approved.
- Rationale: Users must be able to install the application without undocumented dependencies.
- Acceptance Criteria: A clean installation is verified on every target OS; documentation lists supported OSs and JDK requirements; uninstall warns before data deletion and does not remove the vault without confirmation; the update rollback procedure preserves user data.
- Verification Method: Demonstration, inspection.
- More Information: CON-01, CON-06; target operating systems and JDK are open in Section 5.1.
```

#### 3.5.2 Build and Delivery

```markdown
- ID: REQ-BUILD-001
- Title: Reproducible and verifiable delivery
- Statement: The team shall pin JDK and dependency versions, build release artifacts through an automated process, verify them, and publish artifact checksums and a digital release signature.
- Rationale: Provides release traceability and integrity.
- Acceptance Criteria: Each version has a version number, component/license list, checksums, a verifiable signature, and build instructions; the release passes automated tests and dependency checks; only a verified artifact is promoted between environments.
- Verification Method: Inspection, repeat build.
- More Information: CON-01; related: REQ-PORT-001.
```

#### 3.5.3 Distribution

Release 1.0 is intended to be installed and store data on the user’s device. Replication mechanisms, distributed servers, and horizontal scaling are not required. Any addition of network synchronization requires revisiting product scope, the threat model, and availability and confidentiality requirements.

#### 3.5.4 Maintainability

```markdown
- ID: REQ-MAINT-001
- Title: Documentation and change-impact analysis
- Statement: The codebase shall include build and test instructions, a description of the vault format, and cryptography design decisions; changes to the format or secret handling shall include an assessment of compatibility and data migration impact.
- Rationale: Safe changes require understanding their consequences for user vaults.
- Acceptance Criteria: Documentation is available in the repository; change review includes a migration test or a rationale for why one is unnecessary.
- Verification Method: Inspection.
- More Information: CON-05; related: REQ-SEC-001, REQ-REL-002.
```

#### 3.5.5 Reusability

Separate password-generation, serialization, and TOTP-processing components may be made reusable only if they have stable interfaces and independent tests. Publishing libraries or promising a stable external API is not required for release 1.0.

#### 3.5.6 Portability

```markdown
- ID: REQ-PORT-001
- Title: Portability of Java components
- Statement: Java components shall build and pass automated tests on the approved JDK release; platform-dependent features shall be isolated from vault logic.
- Rationale: Simplifies support for target platforms and reduces platform-specific differences in critical logic.
- Acceptance Criteria: A supported runtime is specified for each target environment; common tests pass without platform-specific workarounds; autofill integration is tested separately.
- Verification Method: Build and test on target platforms.
- More Information: CON-01; target JDK and operating systems are open in Section 5.1.
```

#### 3.5.7 Cost

No budget, licensing model, or spending limit has been provided. In release 1.0, the product shall not depend on a paid external service for local vault access. Third-party library selection shall consider license obligations and support costs; financial targets will be added after the business model is agreed.

#### 3.5.8 Deadline

Milestone and release dates have not been defined. Milestone dependencies are: the product owner approves platforms and JDK; the PoC validates critical integrations and cryptographic assumptions; architecture and threat model are then baselined; the release candidate passes functional, integration, negative, performance, and security tests. Release 1.0 readiness criteria are: no unresolved critical vulnerabilities without documented risk acceptance; backup and restore verified; installation, migration, and rollback instructions published; and release approval from the product owner and security specialist.

#### 3.5.9 Proof of Concept

```markdown
- ID: REQ-POC-001
- Title: Validation of critical technical risks
- Statement: Before the architecture is baselined, the team shall conduct a limited feasibility study of local-vault encryption, password generation, TOTP storage, and safe autofill on the selected platform.
- Rationale: Autofill and secure secret handling depend on the platform and need early validation.
- Acceptance Criteria: The PoC is timeboxed to two calendar weeks after platform approval; it demonstrates vault creation/unlock and correct rejection of an incorrect password; test secrets do not appear in plaintext files or logs; autofill refuses an unsuitable source; results, limitations, and a go/revise decision are documented.
- Verification Method: Demonstration, analysis.
- More Information: CON-03, CON-05; results gate the architecture baseline.
```

#### 3.5.10 Change Management

Changes shall be classified as bug fixes, compatible additions, or breaking changes. Each change request shall be reviewed by the product owner; security and vault-format changes shall also be reviewed by the security specialist. Every approved change shall be recorded in the revision history and release notes; incompatible changes shall provide migration instructions and a rollback plan before installation.

```markdown
- ID: REQ-CM-001
- Title: Change control and communication
- Statement: The team shall classify, assess, approve, and document changes to Guardian requirements and releases before including each change in a release.
- Rationale: Controlled change management prevents data loss and unintended reduction in security.
- Acceptance Criteria: Each change records its category, security/compatibility impact assessment, approval by the product owner and, where applicable, the security specialist; format changes include migration and rollback plans; releases include a changelog and user guidance when needed.
- Verification Method: Inspection, analysis.
- More Information: Related to REQ-MAINT-001, REQ-SEC-001, and REQ-REL-002.
```

### 3.6 AI/ML

Guardian version 1.0 does not use machine learning or generative AI. These subsections are not applicable; adding AI in a future version will require a separate description of the model, data, guardrails, human oversight, and ethical-risk assessment.

#### 3.6.1 Model Specification

Not applicable: no ML models are included in release 1.0. The password generator is not an ML model and shall use a cryptographically secure random-number generator.

#### 3.6.2 Data Management

No data is collected or used for ML training. Vault secrets shall not be sent to train models or to external analytics services.

#### 3.6.3 Guardrails

ML guardrails are not applicable. Safety of actions and autofill is governed by REQ-SEC-004, REQ-SEC-005, and REQ-FUNC-006.

#### 3.6.4 Ethics

ML ethics assessment is not applicable because there are no ML components. The interface shall not mislead users about where a secret is sent or what guarantees the application provides.

#### 3.6.5 Human-in-the-Loop

There are no ML-driven decisions. Selecting a record for autofill and revealing a secret require explicit user action as specified by the functional requirements.

#### 3.6.6 Model Lifecycle and Operations

Not applicable: no models are deployed, retrained, or monitored.

---

## 4. Verification

Each requirement shall be verified on supported target devices, which must be identified before release. Security requirements require both positive and negative scenarios. Test data shall be synthetic and shall not contain real user secrets.

| Requirement ID | Verification Method | Test / Artifact | Status | Evidence |
|---|---|---|---|---|
| REQ-INT-001 | Inspection, functional test | Planned artifact: `tests/verification/REQ-INT-001.md` | Planned | — |
| REQ-INT-002 | Traffic analysis, inspection | Planned artifact: `tests/verification/REQ-INT-002.md` | Planned | — |
| REQ-INT-003 | Integration test, demonstration | Planned artifact: `tests/verification/REQ-INT-003.md` | Blocked by platform selection | — |
| REQ-FUNC-001 | Test, analysis | Planned artifact: `tests/verification/REQ-FUNC-001.md` | Planned | — |
| REQ-FUNC-002 | Functional test | Planned artifact: `tests/verification/REQ-FUNC-002.md` | Planned | — |
| REQ-FUNC-003 | Functional test | Planned artifact: `tests/verification/REQ-FUNC-003.md` | Planned | — |
| REQ-FUNC-004 | Test, analysis | Planned artifact: `tests/verification/REQ-FUNC-004.md` | Planned | — |
| REQ-FUNC-005 | Test, inspection | Planned artifact: `tests/verification/REQ-FUNC-005.md` | Planned | — |
| REQ-FUNC-006 | Integration, negative test | Planned artifact: `tests/verification/REQ-FUNC-006.md` | Blocked by platform selection | — |
| REQ-FUNC-007 | Test, analysis | Planned artifact: `tests/verification/REQ-FUNC-007.md` | Planned | — |
| REQ-FUNC-008 | Test, inspection | Planned artifact: `tests/verification/REQ-FUNC-008.md` | Planned | — |
| REQ-FUNC-009 | Functional test | Planned artifact: `tests/verification/REQ-FUNC-009.md` | Planned | — |
| REQ-PERF-001 | Load test | Planned artifact: `tests/verification/REQ-PERF-001.md` | Blocked by target device | — |
| REQ-PERF-002 | Performance test | Planned artifact: `tests/verification/REQ-PERF-002.md` | Blocked by target device | — |
| REQ-SEC-001 | Analysis, inspection | Planned artifact: `tests/verification/REQ-SEC-001.md` | Planned | — |
| REQ-SEC-002 | Analysis, test | Planned artifact: `tests/verification/REQ-SEC-002.md` | Planned | — |
| REQ-SEC-003 | Test | Planned artifact: `tests/verification/REQ-SEC-003.md` | Planned | — |
| REQ-SEC-004 | Integration test | Planned artifact: `tests/verification/REQ-SEC-004.md` | Blocked by platform selection | — |
| REQ-SEC-005 | Negative test, analysis | Planned artifact: `tests/verification/REQ-SEC-005.md` | Blocked by platform selection | — |
| REQ-REL-001 | Fault-tolerance test | Planned artifact: `tests/verification/REQ-REL-001.md` | Planned | — |
| REQ-REL-002 | Negative test | Planned artifact: `tests/verification/REQ-REL-002.md` | Planned | — |
| REQ-AVAIL-001 | Isolated-environment test | Planned artifact: `tests/verification/REQ-AVAIL-001.md` | Planned | — |
| REQ-OBS-001 | Inspection, test | Planned artifact: `tests/verification/REQ-OBS-001.md` | Planned | — |
| REQ-COMP-001 | Inspection | Planned artifact: `tests/verification/REQ-COMP-001.md` | Planned | — |
| REQ-COMP-002 | Inspection | Planned artifact: `tests/verification/REQ-COMP-002.md` | Planned | — |
| REQ-INST-001 | Demonstration, inspection | Planned artifact: `tests/verification/REQ-INST-001.md` | Blocked by platform selection | — |
| REQ-BUILD-001 | Inspection, repeat build | Planned artifact: `tests/verification/REQ-BUILD-001.md` | Planned | — |
| REQ-MAINT-001 | Inspection | Planned artifact: `tests/verification/REQ-MAINT-001.md` | Planned | — |
| REQ-PORT-001 | Build and test | Planned artifact: `tests/verification/REQ-PORT-001.md` | Blocked by platform selection | — |
| REQ-POC-001 | Demonstration, analysis | Planned artifact: `tests/verification/REQ-POC-001.md` | Planned | — |
| REQ-CM-001 | Inspection, analysis | Planned artifact: `tests/verification/REQ-CM-001.md` | Planned | — |

Test paths in the matrix are planned locations: artifacts shall be added to the repository with the tests; until created, status remains “Planned” or “Blocked” according to dependencies. Evidence shall link to a CI report or verification record.


---
## 5. Appendixes

### 5.1 Open Questions

1. Which platforms are in the first release: desktop, mobile, browser extension, or a combination?
2. Which supported Java/JDK release is required?
3. Is two-factor verification for signing in to Guardian itself required, in addition to storing TOTP codes for other services?
4. Are synchronization, a Guardian account, or moving data between devices required in the first release?
5. What import/export and compatibility requirements are expected for other password managers?
6. What are the localization, accessibility, licensing, and applicable-law requirements?
7. Are the proposed performance targets and automatic-lock timers approved?

### 5.2 Draft Limitations

This SRS was prepared from a short description: a password manager with password generation and storage, autofill, categories, notes, two-factor authentication, and Java implementation. The platform, distribution model, and specific cryptographic decisions were not provided. Platform requirements and numerical QoS thresholds are therefore preliminary and require agreement with the product owner and a security specialist before the SRS baseline is approved.
