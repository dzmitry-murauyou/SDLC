# Software Requirements Specification

## Guardian — Password Manager

Version 0.1 (Draft)  
Prepared by: Not specified  
Organization: Not specified  
Date modified: 2026-10-26

## Table of Contents

1. [Introduction](#1-introduction)
   1. [Document Purpose](#11-document-purpose)
   2. [Product Scope](#12-product-scope)
   3. [Definitions, Acronyms, and Abbreviations](#13-definitions-acronyms-and-abbreviations)
   4. [References](#14-references)
   5. [Document Overview](#15-document-overview)
2. [Product Overview](#2-product-overview)
   1. [Product Perspective](#21-product-perspective)
   2. [Product Functions](#22-product-functions)
   3. [Product Constraints](#23-product-constraints)
   4. [User Characteristics](#24-user-characteristics)
   5. [Assumptions and Dependencies](#25-assumptions-and-dependencies)
   6. [Apportioning of Requirements](#26-apportioning-of-requirements)
3. [Requirements](#3-requirements)
   1. [External Interfaces](#31-external-interfaces)
   2. [Functional Requirements](#32-functional-requirements)
   3. [Quality of Service](#33-quality-of-service)
   4. [Compliance](#34-compliance)
   5. [Design and Implementation](#35-design-and-implementation)
   6. [AI/ML](#36-aiml)
4. [Verification](#4-verification)
5. [Appendixes](#5-appendixes)

## Revision History

| Author | Date | Reason for Change | Version |
|---|---|---|---|
| Not specified | 2026-10-26 | Initial SRS draft based on the brief product description | 0.1 |

---

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

| Source | Version / Date | Status and Application |
|---|---|---|
| `srs/srs-template-en.md` in this repository | Current repository version | Informative: structure and guidance for preparing an SRS. |
| RFC 6238, TOTP: Time-Based One-Time Password Algorithm | 2011 | Informative; applicable to TOTP code generation if this feature is confirmed for the release. |
| OWASP Application Security Verification Standard (ASVS) | Version to be fixed during development | Informative security-verification reference; this SRS does not claim compliance. |
| Java documentation and the selected supported JDK release | Release not yet selected | Normative after the project fixes the target JDK. |

### 1.5 Document Overview

Section 2 describes Guardian’s context, users, constraints, and assumptions. Section 3 contains verifiable requirements for interfaces, functions, quality, compliance, and implementation; Section 4 maps each requirement to a verification method. Section 5 records additional decisions, open questions, and limitations of this draft. Requirements use unique identifiers in the form `REQ-[AREA]-[NNN]`, and changes to the specification are recorded in the revision history.

---

## 2. Product Overview

### 2.1 Product Perspective

Guardian is a new standalone product for an individual user, replacing password storage in notes, browser forms, or spreadsheets. Its primary asset is a local store of secrets; the autofill interface interacts with supported browsers or applications depending on the selected platform. An external account or synchronization service is outside the scope of version 1.0. The product owner, support model, target platforms, and SLA requirements have not yet been defined.

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

| ID | Assumption / Dependency | If False |
|---|---|---|
| A-01 | The first release serves one user and one local vault, without cloud synchronization. | Server architecture, account management, synchronization, conflict resolution, and a separate threat model will be required. |
| A-02 | The user keeps the master password separately and understands that losing it may make the data impossible to decrypt. | A separately designed recovery process will be needed, increasing abuse risks. |
| A-03 | The user runs Guardian on a supported, uncompromised device. | The application cannot guarantee protection against malware, keyloggers, or physical access to an unlocked device. |
| A-04 | Specific browsers/operating systems with available APIs will be selected for autofill. | Interface, security, and testing requirements must be revised. |
| A-05 | Cryptography and random-number-generation libraries will be available for the selected Java runtime and will pass license and security reviews. | The target platform or feature set may need to change; custom cryptography is not permitted without separate justification. |
| A-06 | The built-in two-factor feature means storing a website’s TOTP secret and generating its code; MFA for signing in to Guardian itself may be added only after the platform and authentication model are clarified. | The 2FA requirements must be clarified before design. |

### 2.6 Apportioning of Requirements

| Area / Requirements | Subsystem or Increment | Status |
|---|---|---|
| REQ-FUNC-001–005 | Release 1.0: local vault, records, categories, generation, notes | Planned |
| REQ-FUNC-006–007, REQ-INT-003 | Release 1.0: autofill and TOTP, subject to selection of a supported platform | Platform to be confirmed |
| REQ-SEC-001–005, REQ-REL-001–002 | Release 1.0: baseline data protection and recovery | Mandatory for release |
| REQ-INT-001–003, REQ-PERF-001–002, REQ-OBS-001 | Release 1.0: interface, integration, and measurable QoS | Planned; target devices to be confirmed |
| REQ-AVAIL-001, REQ-COMP-001, REQ-INST-001, REQ-BUILD-001, REQ-MAINT-001, REQ-PORT-001, REQ-POC-001 | Release 1.0: release readiness, operations, and proof of feasibility | Project decisions required |
| Synchronization, sharing, enterprise management, AI | Potential future releases | Out of scope for release 1.0 |

---

## 3. Requirements

Each requirement below defines a verifiable obligation for Guardian. Performance and timer values are draft targets and must be confirmed on target devices before the requirements baseline is approved. “Shall” and “shall not” are mandatory for release 1.0 unless a requirement is explicitly marked as awaiting agreement.

### 3.1 External Interfaces

#### 3.1.1 User Interfaces

The interface shall let users manage the vault, records, categories, generator, and TOTP without manually editing files. Secrets shall be masked by default; revealing or copying them shall require an explicit user action. Errors during unlock, save, import/export, and autofill shall explain what happened without displaying secret values. Exact screens and platform-specific flows will be specified in a separate UX specification after target operating systems are selected.

#### 3.1.2 Hardware Interfaces

No specialized hardware is required. Installation shall run on devices that meet the minimum requirements of the selected Java runtime and target operating system. If autofill on a platform requires system integration or a biometric sensor, that dependency shall be stated explicitly and shall not be mandatory for vault access unless separately agreed.

#### 3.1.3 Software Interfaces

- Interaction with a browser or operating system for autofill is permitted only through an officially supported interface of the selected platform.
- The record format shall support a title, username, password, URL/source identifier, categories, notes, and optional TOTP data.
- An external network API, cloud synchronization, and third-party analytics SDKs are outside the scope of version 1.0.

- **ID:** REQ-INT-001  
  **Title:** Secret-management interface  
  **Statement:** The user interface shall mask secret values by default and require an explicit user action to reveal, copy, or autofill a secret.  
  **Rationale:** Prevents accidental disclosure during ordinary navigation.  
  **Acceptance Criteria:** Passwords and TOTP secrets are not displayed in record lists; revealing/copying requires a separate action; interface errors contain no secret values.  
  **Verification Method:** Inspection, functional test.

- **ID:** REQ-INT-002  
  **Title:** External integration restrictions  
  **Statement:** In release 1.0, the system shall not transmit vault data to external network services; browser or operating-system integration is permitted only for user-initiated autofill.  
  **Rationale:** Preserves the product’s local nature and limits the data-leak surface.  
  **Acceptance Criteria:** Network-traffic analysis detects no outbound requests containing vault data; all permitted integration calls are related to documented autofill flows.  
  **Verification Method:** Traffic analysis, inspection.

- **ID:** REQ-INT-003  
  **Title:** Secure autofill integration  
  **Statement:** Integration with the selected browser or operating system shall transfer only fields from the record selected by the user to an explicitly confirmed target context.  
  **Rationale:** Limits the data available to an external application.  
  **Acceptance Criteria:** An integration test confirms that only selected fields are transferred and that unsupported or mismatched contexts are rejected.  
  **Verification Method:** Integration test, demonstration.

### 3.2 Functional Requirements

- **ID:** REQ-FUNC-001  
  **Title:** Vault creation and unlock  
  **Statement:** The system shall allow the user to create a vault, set a master password, and unlock the vault only after validating the entered secret.  
  **Rationale:** The master password is the primary user method of accessing data.  
  **Acceptance Criteria:** Records are available with the correct secret; with an incorrect secret, secret fields are not revealed and the application displays a neutral error message; the master password is not stored in plaintext.  
  **Verification Method:** Test, analysis.

- **ID:** REQ-FUNC-002  
  **Title:** Record management  
  **Statement:** The system shall allow the user to add, view, edit, and delete a record containing a title, username, password, URL or other source identifier, and user-defined additional fields.  
  **Rationale:** This is the core password-manager workflow.  
  **Acceptance Criteria:** Saved changes persist after the application is closed and reopened; a deleted record is not displayed in the normal list; save failures do not cause partial or silent data loss.  
  **Verification Method:** Functional test.

- **ID:** REQ-FUNC-003  
  **Title:** Categories, filtering, and search  
  **Statement:** The system shall allow the user to assign records to user-defined categories and find records by title, username, category, or source address.  
  **Rationale:** Categorization simplifies management of a growing vault.  
  **Acceptance Criteria:** A category can be created, renamed, assigned, and deleted; deleting a category does not delete records; search results match the query and do not expose passwords.  
  **Verification Method:** Functional test.

- **ID:** REQ-FUNC-004  
  **Title:** Password generation  
  **Statement:** The system shall generate a password using a platform cryptographically secure random source, with a user-selected length and selected character classes.  
  **Rationale:** Random, unique passwords reduce guessing and reuse risks.  
  **Acceptance Criteria:** The result satisfies the selected constraints; if settings are incompatible or the length is invalid, the system reports an error and does not produce a password that violates the settings; the generator does not use a predictable random source.  
  **Verification Method:** Test, analysis.

- **ID:** REQ-FUNC-005  
  **Title:** Secure notes  
  **Statement:** The system shall allow users to create and edit notes containing text related to the vault and shall store them with the same confidentiality protection as other secret data.  
  **Rationale:** Users may need to protect information that is not a username or password.  
  **Acceptance Criteria:** A note is available only after unlock; its contents do not appear in logs, external system search suggestions, or plaintext vault files.  
  **Verification Method:** Functional test, inspection.

- **ID:** REQ-FUNC-006  
  **Title:** Safe autofill  
  **Statement:** The system shall offer autofill only for a record selected by the user and only when the source matches the saved URL/source identifier according to the selected platform’s rules.  
  **Rationale:** Autofill must not send secrets to a lookalike or unrelated website.  
  **Acceptance Criteria:** For an allowed exact match, the user is shown the target record; on mismatch, an ambiguous source, or an unsupported context, the password is not transferred; filling occurs only after the user explicitly selects the record.  
  **Verification Method:** Integration and negative testing.

- **ID:** REQ-FUNC-007  
  **Title:** TOTP codes for saved accounts  
  **Statement:** The system shall allow a TOTP secret to be stored with a record and shall display the current one-time code and the time remaining until it changes.  
  **Rationale:** The user requested two-factor authentication support.  
  **Acceptance Criteria:** The code matches the expected values for RFC 6238 test vectors; the TOTP secret is encrypted at rest; the code’s remaining lifetime is displayed; the secret is not included in a regular plaintext export.  
  **Verification Method:** Test, analysis.

- **ID:** REQ-FUNC-008  
  **Title:** Backup and restore  
  **Statement:** The system shall allow the user to create a backup of the vault in a protected format and restore it after user confirmation.  
  **Rationale:** This protects against data loss due to failure or reinstallation.  
  **Acceptance Criteria:** The backup does not contain secret fields in plaintext; restoring a valid backup returns records without changing their values; a corrupted or unsupported backup is rejected without overwriting the current vault.  
  **Verification Method:** Test, format inspection.

- **ID:** REQ-FUNC-009  
  **Title:** Locking and revealing secrets  
  **Statement:** The system shall let users lock the vault immediately, shall mask passwords and notes by default, and shall require an explicit action to reveal a secret temporarily.  
  **Rationale:** This reduces the chance of accidental secret exposure.  
  **Acceptance Criteria:** Record contents are unavailable through the interface after locking; a revealed secret is masked again after a short configured interval or when the record screen is left.  
  **Verification Method:** Functional test.

### 3.3 Quality of Service

#### 3.3.1 Performance

- **ID:** REQ-PERF-001  
  **Title:** Unlock and search response time  
  **Statement:** On an agreed target device, the system shall unlock a local vault of up to 5,000 records within 3 seconds at the 95th percentile after entry of a correct master password; metadata search shall complete within 500 ms at the 95th percentile.  
  **Rationale:** Provides acceptable responsiveness for everyday use.  
  **Acceptance Criteria:** The metrics are confirmed by a repeatable test on a recorded configuration; measurements do not include artificial network access.  
  **Verification Method:** Load test.

- **ID:** REQ-PERF-002  
  **Title:** Response to user actions  
  **Statement:** For ordinary local operations (opening a record, changing a category, or saving a record), the system shall provide a visible result within 1 second at the 95th percentile on the target device.  
  **Rationale:** Vault-management operations should feel immediate.  
  **Acceptance Criteria:** The metric is measured with up to 5,000 records and a published test configuration.  
  **Verification Method:** Performance test.

#### 3.3.2 Security

- **ID:** REQ-SEC-001  
  **Title:** Vault encryption  
  **Statement:** The system shall encrypt secret fields and backups using current, widely reviewed cryptographic mechanisms from a supported library; the specific algorithms, parameters, and key-management scheme shall be approved in design documentation before release.  
  **Rationale:** Protects data confidentiality when device files or a backup are accessed.  
  **Acceptance Criteria:** Inspection of configuration and format confirms encryption; reading the file without the key does not reveal secret-field contents; no custom cryptographic primitives are used without an approved exception.  
  **Verification Method:** Analysis, inspection.

- **ID:** REQ-SEC-002  
  **Title:** Master-password and key protection  
  **Statement:** The system shall not store the master password or decryption key in plaintext, and any derived values shall be stored only in a form approved by a security analysis.  
  **Rationale:** Disclosure of an application or vault file must not directly reveal the access secret.  
  **Acceptance Criteria:** The master password and key are absent from files, logs, crash reports, and telemetry; key-derivation parameters are documented and reviewed by a security specialist.  
  **Verification Method:** Analysis, test.

- **ID:** REQ-SEC-003  
  **Title:** Automatic locking  
  **Statement:** The system shall automatically lock an unlocked vault after 5 minutes of inactivity; the value shall be configurable by the user but shall not be fully disabled in release 1.0.  
  **Rationale:** Limits the time window in which an unlocked vault can be accessed.  
  **Acceptance Criteria:** The vault locks after the inactivity timer expires; secret records remain unavailable until re-authentication.  
  **Verification Method:** Test.

- **ID:** REQ-SEC-004  
  **Title:** Clipboard protection  
  **Statement:** If the user copies a password to the clipboard, the system shall clear it within 30 seconds or when the vault is locked, if the platform allows clipboard control.  
  **Rationale:** Reduces the time for which another application can access a secret.  
  **Acceptance Criteria:** On a supported platform, timed clearing and clearing on lock are verified; if the operating system does not permit clearing, the user is warned before copying.  
  **Verification Method:** Integration test, demonstration.

- **ID:** REQ-SEC-005  
  **Title:** Autofill source verification  
  **Statement:** The system shall verify the autofill source identifier using the platform’s safe rules and shall not fill a secret when the source does not match.  
  **Rationale:** Protects against phishing and inadvertent password disclosure.  
  **Acceptance Criteria:** The test suite covers a matching domain, lookalike domain, subdomain, non-default port, invalid scheme, and ambiguous URL; filling is allowed only in documented acceptable cases.  
  **Verification Method:** Negative test, analysis.

#### 3.3.3 Reliability

- **ID:** REQ-REL-001  
  **Title:** Integrity in case of failure  
  **Statement:** The system shall save vault changes atomically to the extent supported by the selected format, so that an interrupted write does not cause silent loss or alteration of previously saved data.  
  **Rationale:** Vault corruption may cause irrecoverable loss of secrets.  
  **Acceptance Criteria:** An injected interruption during a save does not leave a partially accepted record; the application reports unreadable data and preserves the original file/copy for recovery.  
  **Verification Method:** Fault-tolerance test.

- **ID:** REQ-REL-002  
  **Title:** Backup validation  
  **Statement:** The system shall validate the integrity and format of a backup before restoration and shall not replace the active vault with unverified data.  
  **Rationale:** Protects against corrupted, tampered, or incompatible backups.  
  **Acceptance Criteria:** Corrupted and incorrectly authenticated backups are rejected; the original vault remains accessible.  
  **Verification Method:** Negative test.

#### 3.3.4 Availability

- **ID:** REQ-AVAIL-001  
  **Title:** Offline availability  
  **Statement:** After installation and vault creation, the user shall be able to perform local operations without a network connection.  
  **Rationale:** Passwords should remain available without a network, and the product has no external service dependency in release 1.0.  
  **Acceptance Criteria:** Creation, unlock, search, editing, generation, TOTP, and local backup work in an isolated network; the application does not attempt to send vault contents over an external network.  
  **Verification Method:** Isolated-environment test, network-traffic analysis.

#### 3.3.5 Observability

- **ID:** REQ-OBS-001  
  **Title:** Safe diagnostics  
  **Statement:** The system shall provide diagnostic messages about failures and operation status without including passwords, the master password, TOTP secrets, notes, keys, or plaintext record contents.  
  **Rationale:** Diagnostics are needed to fix problems, but logs must not become a data-leak channel.  
  **Acceptance Criteria:** Inspection of logs and reports after test operations confirms the absence of secrets; URL/username values are masked or omitted when they could identify an account.  
  **Verification Method:** Inspection, test.

### 3.4 Compliance

- **ID:** REQ-COMP-001  
  **Title:** Dependency and license review  
  **Statement:** Before release, the team shall inventory third-party libraries, record their versions and licenses, and check for known critical vulnerabilities.  
  **Rationale:** Reduces legal and operational risks from dependencies.  
  **Acceptance Criteria:** Each release includes a component list and review results; critical vulnerabilities are not released without documented risk acceptance.  
  **Verification Method:** Release-artifact inspection.

Specific legal requirements and regulatory standards depend on jurisdiction and target market; the product owner must identify them before public release. This document does not claim certification or regulatory compliance.

### 3.5 Design and Implementation

#### 3.5.1 Installation

- **ID:** REQ-INST-001  
  **Title:** Supported installation  
  **Statement:** A release shall include documented installation steps, Java runtime requirements, and a list of supported operating systems once these have been approved.  
  **Rationale:** Users must be able to install the application without undocumented dependencies.  
  **Acceptance Criteria:** A clean installation is verified on every target OS; the uninstall procedure describes what happens to the local vault and warns the user before data deletion.  
  **Verification Method:** Demonstration, inspection.

#### 3.5.2 Build and Delivery

- **ID:** REQ-BUILD-001  
  **Title:** Reproducible and verifiable delivery  
  **Statement:** The team shall pin Java and dependency versions, build release artifacts through an automated process, and publish artifact checksums.  
  **Rationale:** Provides release traceability and integrity.  
  **Acceptance Criteria:** Each version has a version number, dependency list, checksums, and build instructions; the release artifact passes automated checks.  
  **Verification Method:** Inspection, repeat build.

#### 3.5.3 Distribution

Release 1.0 is intended to be installed and store data on the user’s device. Replication mechanisms, distributed servers, and horizontal scaling are not required. Any addition of network synchronization requires revisiting product scope, the threat model, and availability and confidentiality requirements.

#### 3.5.4 Maintainability

- **ID:** REQ-MAINT-001  
  **Title:** Documentation and change-impact analysis  
  **Statement:** The codebase shall include build and test instructions, a description of the vault format, and cryptography design decisions; changes to the format or secret handling shall include an assessment of compatibility and data migration impact.  
  **Rationale:** Safe changes require understanding their consequences for user vaults.  
  **Acceptance Criteria:** Documentation is available in the repository; change review includes a migration test or a rationale for why one is unnecessary.  
  **Verification Method:** Inspection.

#### 3.5.5 Reusability

Separate password-generation, serialization, and TOTP-processing components may be made reusable only if they have stable interfaces and independent tests. Publishing libraries or promising a stable external API is not required for release 1.0.

#### 3.5.6 Portability

- **ID:** REQ-PORT-001  
  **Title:** Portability of Java components  
  **Statement:** Java components shall build and pass automated tests on the approved JDK release; platform-dependent features shall be isolated from vault logic.  
  **Rationale:** Simplifies support for target platforms and reduces platform-specific differences in critical logic.  
  **Acceptance Criteria:** A supported runtime is specified for each target environment; common tests pass without platform-specific workarounds; autofill integration is tested separately.  
  **Verification Method:** Build and test on target platforms.

#### 3.5.7 Cost

No budget, licensing model, or spending limit has been provided. In release 1.0, the product shall not depend on a paid external service for local vault access. Third-party library selection shall consider license obligations and support costs; financial targets will be added after the business model is agreed.

#### 3.5.8 Deadline

Milestone and release dates have not been defined. Recommended release 1.0 readiness criteria are: target platforms and JDK approved; security requirements addressed; functional, integration, and negative autofill tests passed; backup restoration verified; dependency analysis completed; and a security review performed.

#### 3.5.9 Proof of Concept

- **ID:** REQ-POC-001  
  **Title:** Validation of critical technical risks  
  **Statement:** Before the architecture is baselined, the team shall conduct a limited feasibility study of local-vault encryption, password generation, TOTP storage, and safe autofill on the selected platform.  
  **Rationale:** Autofill and secure secret handling depend on the platform and need early validation.  
  **Acceptance Criteria:** The study demonstrates vault creation/unlock and correct rejection of an incorrect password; test secrets do not appear in plaintext files or logs; autofill refuses an unsuitable source; limitations and results are documented.  
  **Verification Method:** Demonstration, analysis.

#### 3.5.10 Change Management

Changes to functional and security requirements shall be made through SRS review and recorded in the revision history. Changes to the vault format, cryptographic parameters, autofill, or lock timers shall include an impact assessment for security, backward compatibility, and migration. Changes that may make an existing backup unreadable require a migration plan or an explicit warning before an update is installed.

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
| REQ-INT-001 | Inspection, functional test | View, reveal, and copy scenarios | Planned | — |
| REQ-INT-002 | Traffic analysis, inspection | Network flows and permitted calls | Planned | — |
| REQ-INT-003 | Integration test, demonstration | Field/context transfer matrix | Blocked by platform selection | — |
| REQ-FUNC-001 | Test, analysis | Create/unlock with correct and incorrect secrets | Planned | — |
| REQ-FUNC-002 | Functional test | Record CRUD, persistence after restart, deletion | Planned | — |
| REQ-FUNC-003 | Functional test | Categories and search query set | Planned | — |
| REQ-FUNC-004 | Test, analysis | Boundary settings and random-source review | Planned | — |
| REQ-FUNC-005 | Test, inspection | Note after locking; file/log inspection | Planned | — |
| REQ-FUNC-006 | Integration, negative test | Matrix of valid and unsuitable sources | Blocked by platform selection | — |
| REQ-FUNC-007 | Test, analysis | RFC 6238 vectors and stored-data inspection | Planned | — |
| REQ-FUNC-008 | Test, inspection | Backup/restore round trip and corrupted backup | Planned | — |
| REQ-FUNC-009 | Functional test | Masking, reveal, and timed locking | Planned | — |
| REQ-PERF-001 | Load test | 5,000-record dataset, p95 measurements | Blocked by target device | — |
| REQ-PERF-002 | Performance test | Local operations, p95 measurements | Blocked by target device | — |
| REQ-SEC-001 | Analysis, inspection | Vault format and cryptography review | Planned | — |
| REQ-SEC-002 | Analysis, test | Secret search in files, logs, and crash reports | Planned | — |
| REQ-SEC-003 | Test | Automatic lock and re-authentication | Planned | — |
| REQ-SEC-004 | Integration test | Clipboard clearing and OS limitation warning | Blocked by platform selection | — |
| REQ-SEC-005 | Negative test, analysis | Domain, URL, and autofill-context checks | Blocked by platform selection | — |
| REQ-REL-001 | Fault-tolerance test | Interrupted write and recovery | Planned | — |
| REQ-REL-002 | Negative test | Corrupt and incorrectly authenticated backup | Planned | — |
| REQ-AVAIL-001 | Isolated-environment test | Offline local flows and traffic analysis | Planned | — |
| REQ-OBS-001 | Inspection, test | Log and diagnostic-artifact review | Planned | — |
| REQ-COMP-001 | Inspection | Dependency list, licenses, vulnerability report | Planned | — |
| REQ-INST-001 | Demonstration, inspection | Clean install and uninstall on target OSs | Blocked by platform selection | — |
| REQ-BUILD-001 | Inspection, repeat build | CI release, checksums, SBOM/component list | Planned | — |
| REQ-MAINT-001 | Inspection | Documentation and format-change assessment | Planned | — |
| REQ-PORT-001 | Build and test | CI on approved JDK releases/target OSs | Blocked by platform selection | — |
| REQ-POC-001 | Demonstration, analysis | PoC report using safe test data | Planned | — |

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
