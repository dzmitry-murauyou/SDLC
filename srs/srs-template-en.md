# Software Requirements Specification
## For the "Larets" local password manager

Version 0.1  
Prepared by Dzmitry Murauyou, group 4101 (partner: {{partner name assigned by the lecturer}})  
Department of Computer Engineering, BSUIR — Software Development Life Cycle course  
2026-10-25

> **This document replaces the `srs/srs-template-en.md` template and keeps its structure.**  
> Project repository: `dzmitry-murauyou/SDLC`, laboratory work No. 3.  
> Graphical artefacts (SysML v2 → PNG): [`srs/mockups/`](mockups/),  
> source models: [`srs/mockups/`](mockups/).

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
| D. Murauyou | 2026-10-25 | First issue of the business requirements after laboratory work No. 3: application variant and project type selected, customer requirements elicited, SysML v2 GUI mock-ups produced | 0.1 |
|      |      |                    |         |

## 1. Introduction
This document captures the business requirements for "Larets", a desktop password manager that a two-person student team develops during one semester. Sections 1–2 set the context and the product boundary, Section 3 contains verifiable requirements, Section 4 defines how each requirement is verified, and Section 5 collects the graphical artefacts and traceability material.

### 1.1 Document Purpose
The SRS defines **what** "Larets" 0.1.0 must do and why the customer needs it; **how** it will be built is described separately in the SDD. The audience is the customer (acceptance and prioritisation), the two-person development team (planning and design), the QA role (verification matrix in Section 4) and the course supervisor (assessment of engineering quality). The document is normative for downstream artefacts: design description, architecture decision records, test plan and source code.

### 1.2 Product Scope
"Larets" 0.1.0 is a desktop application for Windows, Linux and macOS that keeps passwords, logins, notes and one-time codes in a single encrypted local vault. It addresses three user needs: remembering one master password instead of dozens, never reusing a password across sites, and obtaining a sufficiently strong password without relying on an external service. All data stays on the user's device; the network is used only when the user explicitly enables the breached-password check.

**In scope:** local encrypted vault; categories, tags, favourites and notes; password generator with strength estimation; two-factor authentication (TOTP) for the application itself and for stored entries; auto-lock; encrypted backups; form autofill through a browser companion extension; a minimal CSV import path (version 0.2).

**Out of scope:** cloud synchronisation across devices and family sharing; mobile clients; a server side and internet accounts; file and payment-card storage; enterprise-grade audit and SSO/SAML; AI-based password generation.

### 1.3 Definitions, Acronyms, and Abbreviations

| Term | Definition |
|------|------------|
| AEAD | Authenticated Encryption with Associated Data — encryption that detects tampering of the ciphertext |
| AES-256-GCM | Symmetric block cipher with a 256-bit key in Galois/Counter Mode; the primary protection of the vault |
| Argon2id / PBKDF2 | Password-based key derivation functions; version 0.1.0 uses PBKDF2-HMAC-SHA256 with at least 600 000 iterations, Argon2id is planned for 0.2 |
| HIBP | Have I Been Pwned — a public breached-password service supporting k-anonymity queries |
| Master password | The single password the user remembers; the vault encryption key is derived from it |
| Native Messaging | Browser mechanism (Chrome, Firefox) that exchanges JSON messages between an extension and a local application over standard I/O streams |
| PoC | Proof of Concept — feasibility validation performed before full implementation |
| SecureRandom | Cryptographically strong random number generator in Java (`java.security.SecureRandom`) |
| SRS | Software Requirements Specification — a document that describes the intended purpose, requirements and nature of a software product |
| TOTP | Time-based One-Time Password, RFC 6238; used as the second authentication factor |
| UI | User Interface — the visual part of an application through which a user interacts with the software |
| Vault | The encrypted database file that holds all user entries |
| 2FA | Two-Factor Authentication — master password plus a one-time code |

### 1.4 References

| # | Document | Author / owner | Version, date | Location | Type |
|---|----------|----------------|---------------|----------|------|
| R1 | SRS template, filled in by this document | Department of Computer Engineering, BSUIR | 2026 | [`srs/srs-template.md`](srs-template.md) (this document) | Normative |
| R2 | SDD template (`sdd/sdd-template.md`) | Department of Computer Engineering, BSUIR | 2026 | [`sdd/sdd-template.md`](../sdd/sdd-template.md) | Informative |
| R3 | SysML v2 GUI mock-up model | Project team | 0.1, 2026-10-25 | [`srs/mockups/ui-mockups.sysml`](mockups/ui-mockups.sysml) | Normative |
| R4 | SysML v2 UI element library | Project team | 0.1, 2026-10-25 | [`srs/mockups/ui-library.sysml`](mockups/ui-library.sysml) | Normative |
| R5 | Context and use-case diagrams | Project team | 0.1, 2026-10-25 | [`srs/mockups/use-case-context.sysml`](mockups/use-case-context.sysml) | Normative |
| R6 | Rendered mock-ups (PNG) | Project team | 0.1, 2026-10-25 | [`srs/mockups/`](mockups/) | Normative |
| R7 | Customer business requirements (interview record) | Customer (course role) | 2026-10-23 | [Appendix 5.1](#51-customer-interview-record) | Normative |
| R8 | ISO/IEC/IEEE 29148:2018 Systems and software engineering — Life cycle processes — Requirements engineering | ISO/IEC/IEEE | 2018 | External standard | Normative |
| R9 | ISO/IEC 25010:2011 Systems and software Quality Requirements and Evaluation — Quality models | ISO/IEC | 2011 | External standard | Informative |
| R10 | RFC 6238 TOTP; RFC 4226 HOTP | IETF | 2011 / 2005 | External standard | Normative |
| R11 | NIST SP 800-63B Digital Identity Guidelines — Authentication and Lifecycle Management | NIST | 2017 (upd. 2020) | External standard | Informative |
| R12 | OWASP Password Storage Cheat Sheet | OWASP Foundation | 2024 | External source | Informative |
| R13 | Law of the Republic of Belarus No. 99-Z "On Personal Data Protection" | National Legal Internet Portal | 2021 | External legal act | Normative |

### 1.5 Document Overview
Section 2 describes the product from the outside: its place in the environment, functions, constraints and users. Section 3 contains verifiable requirements with identifiers `REQ-[AREA]-[NNN]` and acceptance criteria. Section 4 maps every requirement to a verification method, and Section 5 holds the customer interview record, the mock-up index and the traceability matrix. Conventions: "shall" marks a mandatory requirement, "should" a recommended one and "may" a permitted one; every interface image is a link to a PNG file generated from the SysML v2 model. Changes are made on laboratory-work branches and recorded in the revision history; a change in the meaning of a requirement increments its version suffix.

## 2. Product Overview

### 2.1 Product Perspective
"Larets" is a new, standalone product rather than a replacement for an existing system. It is a **desktop application** running inside the user's operating system with no server of its own: the vault, settings and backups are local files. External to the system are the user, the operating system (file system and clipboard), the browser with the companion extension (Native Messaging), the authenticator application (TOTP source) and the optional HIBP service. The product owner is the customer (course role); the team of two students implements and supports it during the semester; no SLA is established.

![System context diagram of "Larets": boundaries, external systems and data flows](mockups/07-system-context.png)

*Figure 1 — System context diagram (SysML v2, `use-case-context.sysml`, `SystemContextDiagram`).*

### 2.2 Product Functions
1. **Protected vault.** Master-password unlock, encryption of all data, automatic locking on inactivity and on window minimisation.
2. **Entry management.** Create, read, update and delete entries ("site/service") with login, password, URL, notes and TOTP secret.
3. **Categories, tags and favourites.** Category grouping, free-form tags, quick "Favourites" and "Recent" lists.
4. **Search and filtering.** Instant search over title, login, URL and tags without exposing stored passwords.
5. **Password generator.** Policy-driven passwords (length, character sets, exclusions), entropy estimation and a history of recent generations.
6. **Two-factor authentication (TOTP).** A second factor for the application itself plus stored TOTP secrets with code and backup-code generation.
7. **Clipboard handling.** Copy login and password with automatic clipboard clearing.
8. **Web form autofill.** Credential filling in the browser through the companion extension, only on an explicit user action.
9. **Backup and restore.** Automatic encrypted vault copies with rotation and one-step restore.
10. **Breach check (optional).** Local strength checking and k-anonymous HIBP queries only after the user opts in.

![Use-case diagram of "Larets"](mockups/08-use-cases.png)

*Figure 2 — Use-case diagram (SysML v2, `UseCaseDiagram`); every use case maps to a `REQ-FUNC-*` requirement in Section 3.2.*

### 2.3 Product Constraints

| ID | Constraint | Type |
|----|------------|------|
| C1 | The product shall be a desktop application; a server side and cloud sync are forbidden in version 0.1.0 | External, mandatory |
| C2 | Implementation language — Java 21 (LTS), GUI — JavaFX 21; build — Maven | External, mandatory |
| C3 | Storage — a local SQLite file; encryption — AES-256-GCM via Java Cryptography Architecture | External, mandatory |
| C4 | All graphical requirement artefacts shall be described in SysML v2; PNG files are produced by automatic rendering of the model | Academic, mandatory |
| C5 | The project budget for licences and infrastructure is 0 BYN; only open-source libraries under Apache-2.0, MIT, EPL-2.0 or BSD are allowed | External, mandatory |
| C6 | The team is two developers with one semester available; scope is prioritised with MoSCoW | Organisational |
| C7 | The product shall not collect telemetry or send any data to the network without an explicit user action | External, mandatory |
| C8 | Supported OS: Windows 10/11, Ubuntu 22.04+, macOS 13+; architectures x86-64 and arm64 | External, mandatory |
| C9 | Interface languages: English and Russian (default Russian) through resource bundles | Academic |
| C10 | Third-party cryptographic primitives are used only through JCA; custom cipher implementations are forbidden | External, mandatory |

### 2.4 User Characteristics

| User class | Description and goals | Experience | Frequency | Special needs |
|------------|-----------------------|------------|-----------|---------------|
| Primary user (student, engineer) | Keeps 30–200 passwords for study and work services; wants one master password instead of dozens | Confident PC user, not a security expert | Daily, 5–20 accesses | Fast search, one-click copy, password generation during sign-up |
| Security-conscious user | Stores work credentials and enables 2FA | Understands security basics | Daily | 2FA, auto-lock, breach monitoring, no network traffic |
| Student developer / maintainer | Maintains the product during the course | Java, SQL | As needed | Readable architecture, documentation, tests, reproducible build |
| Customer (course role) | Accepts the result, sets priorities | Not a programmer | Weekly | Clear acceptance criteria, iteration demos |
| Browser extension (software actor) | Requests credentials for the active tab | — | On user action | Narrow protocol, no access to the master password |

### 2.5 Assumptions and Dependencies

| ID | Assumption or dependency | Impact if invalid |
|----|--------------------------|-------------------|
| A1 | The user agrees to remember one master password and does not keep it next to the vault | The main unlock scenario fails; a reset with data loss is required |
| A2 | JavaFX 21 and SQLite JDBC remain available as open-source dependencies in Maven Central | The GUI framework or storage must be replaced, shifting the schedule by 1–2 weeks |
| A3 | Browsers support Native Messaging and allow installing a development extension | Autofill moves to version 0.2; the application stays usable |
| A4 | The user provides their own credentials voluntarily; the product is not used for third-party accounts | Legal and ethical risk; autofill functions are restricted |
| A5 | The HIBP service is reachable over HTTPS and allows k-anonymous requests without a key | Breach checking is disabled; only local strength estimation remains |
| A6 | The local disk is not compromised by malware that intercepts input | Threat-model guarantees degrade; an explicit warning is required in the documentation |
| A7 | The device clock is synchronised (needed for TOTP) | One-time codes fail validation; the UI must hint at clock synchronisation |
| A8 | The partner assigned by the lecturer is available for parallel work and review | Iteration speed drops and some requirements move to 0.2 |

### 2.6 Apportioning of Requirements

| Requirement | Component | Iteration (release) | Status |
|-------------|-----------|---------------------|--------|
| REQ-FUNC-001, REQ-SEC-001…005 | `vault` module (crypto, unlock) | 0.1.0 (M1) | In progress |
| REQ-FUNC-002…004, REQ-INT-001…003 | `ui` + `vault` (CRUD, search, copy) | 0.1.0 (M1) | In progress |
| REQ-FUNC-005, REQ-SEC-004, REQ-PERF-001 | `generator` module | 0.1.0 (M1) | In progress |
| REQ-FUNC-006, REQ-FUNC-008, REQ-INT-006 | `ui` module (categories, notes, settings) | 0.1.0 (M2) | Planned |
| REQ-FUNC-007, REQ-SEC-003, REQ-INT-005 | `totp` module | 0.1.0 (M2) | Planned |
| REQ-FUNC-009, REQ-INT-007 | `bridge` module + browser extension | 0.2.0 (M3) | Planned |
| REQ-FUNC-010, REQ-REL-001…002 | `backup` module | 0.1.0 (M2) | Planned |
| REQ-FUNC-011 | `leaks` module | 0.2.0 (M3) | Deferred (Could) |
| REQ-FUNC-012 (CSV import) | `import` module | 0.2.0 | Deferred (Could) |
| REQ-INST-001, REQ-DIST-001 | `jpackage` build | 0.1.0 (M3) | Planned |
| Cloud sync, mobile clients | — | Not planned | Out of scope |

## 3. Requirements
Each requirement follows the template: identifier, title, statement, rationale, acceptance criteria, verification method and more information. Identifiers are immutable; when the meaning changes, a version suffix is appended (for example `REQ-FUNC-003-V2`).

### 3.1 External Interfaces
#### 3.1.1 User Interfaces
The interface is a JavaFX desktop window with a minimum area of 1000 × 640 logical pixels, system DPI scaling, full keyboard navigation (Tab, Enter, Ctrl+F, Ctrl+N, Ctrl+L to lock) and screen-reader support (roles and labels for controls). The visual style is defined in the SysML v2 model and rendered to PNG; the images below are normative for the layout.

| ID | Screen | Image (SysML v2 → PNG) | Purpose |
|----|--------|------------------------|---------|
| UI-01 | Unlock screen | [`01-unlock-screen.png`](mockups/01-unlock-screen.png) | Master-password entry, 2FA entry point, lockout hint |
| UI-02 | Main vault window | [`02-vault-screen.png`](mockups/02-vault-screen.png) | Entry list, search, categories, entry details, TOTP code |
| UI-03 | Entry editor | [`03-entry-editor.png`](mockups/03-entry-editor.png) | Entry fields, password generation, TOTP binding |
| UI-04 | Password generator | [`04-generator.png`](mockups/04-generator.png) | Generation policy, strength estimation, history |
| UI-05 | Two-factor setup | [`05-two-factor.png`](mockups/05-two-factor.png) | QR code, code entry, backup codes |
| UI-06 | Settings | [`06-settings.png`](mockups/06-settings.png) | Autofill, auto-lock, breach check, backups |

**UI-01. Unlock screen**

![Unlock screen mock-up](mockups/01-unlock-screen.png)

*Figure 3 — `UnlockScreen`, file [`01-unlock-screen.png`](mockups/01-unlock-screen.png).*

**UI-02. Main vault window**

![Main vault window mock-up](mockups/02-vault-screen.png)

*Figure 4 — `VaultScreen`, file [`02-vault-screen.png`](mockups/02-vault-screen.png).*

**UI-03. Entry editor · UI-04. Password generator**

![Entry editor mock-up](mockups/03-entry-editor.png)

*Figure 5 — `EntryEditorScreen`, file [`03-entry-editor.png`](mockups/03-entry-editor.png).*

![Password generator mock-up](mockups/04-generator.png)

*Figure 6 — `GeneratorScreen`, file [`04-generator.png`](mockups/04-generator.png).*

**UI-05. Two-factor setup · UI-06. Settings**

![Two-factor setup mock-up](mockups/05-two-factor.png)

*Figure 7 — `TwoFactorScreen`, file [`05-two-factor.png`](mockups/05-two-factor.png).*

![Settings mock-up](mockups/06-settings.png)

*Figure 8 — `SettingsScreen`, file [`06-settings.png`](mockups/06-settings.png).*

- **ID:** REQ-INT-001
- **Title:** Unlock screen
- **Statement:** On start-up the application shall show screen UI-01 with a master-password field, an "Unlock" button and a "Sign in with a one-time code (2FA)" action; the password value shall be masked by default and revealed only on an explicit action.
- **Rationale:** This screen is the only entry point to the vault and determines both daily usability and shoulder-surfing protection.
- **Acceptance Criteria:** UI-01 is shown on first start; the password is masked with dots; "Show" toggles visibility; the "Unlock" button is disabled while the field is empty; Enter submits the unlock.
- **Verification Method:** Demonstration, Test
- **More Information:** [UI-01](mockups/01-unlock-screen.png), model element `UnlockScreen`.

- **ID:** REQ-INT-002
- **Title:** Main vault window
- **Statement:** The application shall show screen UI-02 containing side navigation (all entries, favourites, recent, categories, tools, settings, lock), a search field, the entry list and the selected-entry panel.
- **Rationale:** The main window concentrates about 80 % of daily user actions.
- **Acceptance Criteria:** all listed regions are present and visually distinct; selecting an entry refreshes the right panel within 100 ms; a "locked" state replaces the list with UI-01.
- **Verification Method:** Demonstration, Inspection
- **More Information:** [UI-02](mockups/02-vault-screen.png), model element `VaultScreen`.

- **ID:** REQ-INT-003
- **Title:** Entry editor screen
- **Statement:** The application shall provide form UI-03 with the mandatory "Title" field, optional "Login", "Site address", "TOTP secret" and "Notes" fields, and a password field with a "Generate" button.
- **Rationale:** The form defines the entry data structure and reduces input errors.
- **Acceptance Criteria:** mandatory fields are marked with "*"; saving with an empty title is blocked with an explanation; "Cancel" and "Save entry" are reachable without scrolling at 1000 × 640.
- **Verification Method:** Test, Inspection
- **More Information:** [UI-03](mockups/03-entry-editor.png), model element `EntryEditorScreen`.

- **ID:** REQ-INT-004
- **Title:** Generator screen and strength indication
- **Statement:** The application shall show generator UI-04 with the result field, generation parameters (length, character sets, exclusions) and a visual strength bar.
- **Rationale:** The user must see the result and understand why a password is considered strong.
- **Acceptance Criteria:** changing any parameter immediately refreshes the result and the strength estimate; the result is copied with one button.
- **Verification Method:** Test, Demonstration
- **More Information:** [UI-04](mockups/04-generator.png), model element `GeneratorScreen`.

- **ID:** REQ-INT-005
- **Title:** Two-factor setup screen
- **Statement:** The application shall show screen UI-05 with a QR code of an `otpauth://` URI, the textual secret, a six-digit code input and a list of backup codes.
- **Rationale:** A step-by-step setup reduces the number of abandoned second-factor enrolments.
- **Acceptance Criteria:** the QR code and the secret are visible at the same time; the input accepts exactly six digits; backup codes can be downloaded as a `.txt` file.
- **Verification Method:** Demonstration, Test
- **More Information:** [UI-05](mockups/05-two-factor.png), model element `TwoFactorScreen`.

- **ID:** REQ-INT-006
- **Title:** Settings screen
- **Statement:** The application shall provide screen UI-06 with the sections "General", "Security", "Autofill", "Backups" and "About", and shall persist changes only after "Save" is pressed.
- **Rationale:** Security settings must be reachable and understandable without editing configuration files.
- **Acceptance Criteria:** switching sections warns about unsaved changes; "Reset" restores the values captured when the screen was opened.
- **Verification Method:** Test, Inspection
- **More Information:** [UI-06](mockups/06-settings.png), model element `SettingsScreen`.

#### 3.1.2 Hardware Interfaces
- **ID:** REQ-INT-010
- **Title:** Workstation requirements
- **Statement:** The application shall run on devices with an x86-64 or arm64 processor, at least 4 GB of RAM, at least 200 MB of free disk space and a display of at least 1366 × 768.
- **Rationale:** Keeps the target audience on common office and student laptops.
- **Acceptance Criteria:** start-up and the main scenario succeed on a device with the stated minimum characteristics.
- **Verification Method:** Analysis, Demonstration
- **More Information:** validated on Windows 10 (x86-64) and Ubuntu 22.04 (x86-64); macOS where hardware allows.

No specialised hardware (tokens, biometric sensors, smart cards) is used in version 0.1.0.

#### 3.1.3 Software Interfaces
- **ID:** REQ-INT-007
- **Title:** Autofill protocol (Native Messaging)
- **Statement:** The application shall accept JSON messages from the browser extension over Native Messaging with the structure `{ "action": "fill" | "ping" | "list", "requestId": string, "domain": string }` and shall answer with the same `requestId`, carrying either `credentials` or `error`.
- **Rationale:** A single narrow protocol prevents the master password and unrelated data from reaching the extension.
- **Acceptance Criteria:** a message without `requestId` is rejected with `E_BAD_REQUEST`; the answer arrives within 500 ms; a locked vault returns `E_LOCKED` without data; the master password and the full entry list are never transmitted.
- **Verification Method:** Test
- **More Information:** native host registration manifests for Chrome and Firefox; details in the SDD Interface view.

- **ID:** REQ-INT-008
- **Title:** Vault file format
- **Statement:** The application shall store data in a single SQLite file (`vault.db`) whose content is encrypted at the application level: each entry and the vault metadata are stored as AEAD containers with a format version, a salt and a nonce.
- **Rationale:** The format determines version compatibility and the ability to recover data.
- **Acceptance Criteria:** the file opens only with the correct master password; flipping a single ciphertext byte causes a decryption failure; the format version is readable before decryption.
- **Verification Method:** Test, Analysis
- **More Information:** the container schema is described in the SDD Information view.

- **ID:** REQ-INT-009
- **Title:** Clipboard interaction
- **Statement:** The application shall place a login or password into the system clipboard and clear it after 20 seconds unless the user has replaced the clipboard content.
- **Rationale:** Reduces leakage through clipboard history and other applications.
- **Acceptance Criteria:** a clearing countdown is visible after copying; the clipboard is empty after 20 s; data copied by the user afterwards is not erased.
- **Verification Method:** Test
- **More Information:** the countdown is shown in the status bar of [UI-02](mockups/02-vault-screen.png).

### 3.2 Functional
- **ID:** REQ-FUNC-001
- **Title:** Vault unlock with the master password
- **Statement:** The system shall unlock the vault when the correct master password is entered and deny access on an incorrect one without disclosing which part of the data failed to match.
- **Rationale:** The master password is the only secret the user remembers; correct error handling prevents guessing.
- **Acceptance Criteria:** the correct password opens the main screen within 1.5 s; a wrong one shows the neutral message "Wrong password"; after five consecutive failures input is blocked for 60 s; the failure counter survives an application restart.
- **Verification Method:** Test
- **More Information:** see [UI-01](mockups/01-unlock-screen.png); REQ-SEC-005.

- **ID:** REQ-FUNC-002
- **Title:** Browse, search and filter entries
- **Statement:** The system shall display the list of entries and find entries by a substring of the title, login, site address or tag, and shall filter them by category, favourites and recent items.
- **Rationale:** Finding the right account among dozens is the user's main pain point.
- **Acceptance Criteria:** search starts after two characters; the list refreshes within 200 ms with 500 entries; passwords are never rendered in search results; an empty result shows the hint "Nothing found".
- **Verification Method:** Test
- **More Information:** implemented in the `ui` module; [UI-02](mockups/02-vault-screen.png).

- **ID:** REQ-FUNC-003
- **Title:** Create, update and delete entries
- **Statement:** The system shall allow creating, updating and deleting entries with the fields "Title", "Login", "Password", "Site address", "Category", "Tags", "Notes", "TOTP secret" and the "Favourite" flag.
- **Rationale:** The full entry lifecycle is the core value of a password manager.
- **Acceptance Criteria:** a new entry appears in the list immediately after saving; deletion requires confirmation naming the entry title; cancelling an edit leaves stored data unchanged; all changes receive a timestamp.
- **Verification Method:** Test
- **More Information:** [UI-03](mockups/03-entry-editor.png).

- **ID:** REQ-FUNC-004
- **Title:** Copy credentials
- **Statement:** The system shall copy a login, password or one-time code of an entry to the clipboard on an explicit user action, without automatically revealing the password on screen.
- **Rationale:** Copying is the most frequent way to use a stored password.
- **Acceptance Criteria:** a password is visible only after pressing "Show" or in edit mode; copying is confirmed with a discreet notification; in hidden mode the password is re-masked after 30 s.
- **Verification Method:** Test
- **More Information:** REQ-INT-009.

- **ID:** REQ-FUNC-005
- **Title:** Policy-based password generation
- **Statement:** The system shall generate passwords of 8 to 64 characters with selectable character sets (uppercase, lowercase, digits, symbols), an option to exclude look-alike characters and an entropy estimate in bits.
- **Rationale:** Weak and reused passwords are the main cause of account compromise.
- **Acceptance Criteria:** the password contains at least one character from every selected set; entropy is shown in bits and is not understated at length 8 with all sets enabled; 10 000 consecutive generations contain no duplicates; the last 10 generations are available in history and never written to disk.
- **Verification Method:** Test, Analysis
- **More Information:** [UI-04](mockups/04-generator.png); REQ-SEC-004.

- **ID:** REQ-FUNC-006
- **Title:** Categories, tags and notes
- **Statement:** The system shall support user-defined categories (at least 20), free-form tags on entries and text notes up to 4000 characters.
- **Rationale:** Grouping speeds up navigation and separates work from personal data.
- **Acceptance Criteria:** a category can be created and renamed without restarting; deleting a category requires moving its entries to another one; notes preserve line breaks; filtering by tag is available from the entry card.
- **Verification Method:** Test
- **More Information:** [UI-02](mockups/02-vault-screen.png), [UI-03](mockups/03-entry-editor.png).

- **ID:** REQ-FUNC-007
- **Title:** Two-factor authentication (TOTP)
- **Statement:** The system shall support TOTP per RFC 6238 both for protecting the vault itself and for storing entry TOTP secrets, displaying the current six-digit code and the remaining validity time in seconds.
- **Rationale:** A second factor protects the vault when the master password leaks and removes the need for a separate authenticator application.
- **Acceptance Criteria:** 2FA enrolment completes only after a successful code check; a code is accepted with a ±1 step tolerance; a wrong code is rejected with the number of remaining attempts; backup codes are single-use and at least 10 of them exist; TOTP secrets are stored encrypted.
- **Verification Method:** Test, Analysis
- **More Information:** [UI-05](mockups/05-two-factor.png); RFC 6238.

- **ID:** REQ-FUNC-008
- **Title:** Automatic locking
- **Statement:** The system shall lock the vault after a user-defined inactivity period (5 minutes by default) and when the main window is minimised, if that setting is enabled.
- **Rationale:** Most leaks happen through physical access to an unlocked device.
- **Acceptance Criteria:** the interval is chosen from 1, 5, 15 and 30 minutes ("Never" is not offered); locking removes the encryption key from memory and hides open passwords; re-entry requires the master password and, if enabled, a TOTP code.
- **Verification Method:** Test
- **More Information:** [UI-06](mockups/06-settings.png); REQ-SEC-002.

- **ID:** REQ-FUNC-009
- **Title:** Web form autofill through the extension
- **Statement:** The system shall, at the request of the companion extension, return the credentials matching the active tab's domain and fill them only after user confirmation in the extension.
- **Rationale:** Autofill saves time but needs strict limits so credentials are not handed to arbitrary sites.
- **Acceptance Criteria:** a domain with no match yields an empty result; credentials of another domain are never returned; a locked vault returns `E_LOCKED`; disabling the feature in settings immediately stops message processing.
- **Verification Method:** Test, Demonstration
- **More Information:** REQ-INT-007; delivered in version 0.2.0.

- **ID:** REQ-FUNC-010
- **Title:** Backup and restore
- **Statement:** The system shall automatically create an encrypted vault copy on every save (at most once per 10 minutes), keep the last seven copies and provide restore from a selected copy.
- **Rationale:** The vault file is the single source of data; disk damage or a user mistake must not destroy passwords.
- **Acceptance Criteria:** a new copy appears in the backup folder after an entry change; no more than seven copies are kept; restore requires the master password and confirmation; a restored copy opens and reflects the state at creation time.
- **Verification Method:** Test
- **More Information:** [UI-06](mockups/06-settings.png), "Backups" section; REQ-REL-002.

- **ID:** REQ-FUNC-011
- **Title:** Breached-password check (optional)
- **Statement:** The system shall, only after the user opts in, check stored passwords against HIBP using k-anonymity (only the first five characters of a SHA-1 hash are sent) and mark entries with matches.
- **Rationale:** The user should learn about a compromised password before an attacker exploits it.
- **Acceptance Criteria:** the feature is disabled by default; no network request is made while it is off; transmitted data cannot be used to recover a password; flagged entries appear in a separate "Needs attention" list.
- **Verification Method:** Test, Inspection
- **More Information:** delivered in version 0.2.0; [UI-06](mockups/06-settings.png).

- **ID:** REQ-FUNC-012
- **Title:** CSV import
- **Statement:** The system shall import entries from CSV exports of common managers (Chrome, Bitwarden, KeePass) with column mapping and a preview.
- **Rationale:** Lowers the barrier to switching to the product.
- **Acceptance Criteria:** entries with the same login and address are not duplicated; parse errors are reported per line; the import runs in a transaction, so a failure leaves data unchanged.
- **Verification Method:** Test
- **More Information:** deferred requirement (Could), version 0.2.0.

### 3.3 Quality of Service
#### 3.3.1 Performance
- **ID:** REQ-PERF-001
- **Title:** Responsiveness of key operations
- **Statement:** The system shall generate a password within 50 ms, run a search over 500 entries within 200 ms, unlock the vault within 1.5 s and reach the unlock screen within 3 s of start-up on target hardware.
- **Rationale:** Waiting frustrates users and pushes them back to less secure habits such as keeping passwords in a text file.
- **Acceptance Criteria:** measurements on the reference machine (4 cores, 8 GB RAM, SSD) stay within the limits at the 95th percentile of 100 repetitions.
- **Verification Method:** Test
- **More Information:** the measurement procedure and load scenario are defined in the test plan (laboratory work No. 5).

- **ID:** REQ-PERF-002
- **Title:** Resource economy
- **Statement:** The system shall use no more than 400 MB of RAM with 1000 entries and no more than 2 % CPU while idle.
- **Rationale:** The application runs alongside a browser and an IDE and must not compete for resources.
- **Acceptance Criteria:** RSS and CPU stay within the thresholds during a 30-minute idle measurement.
- **Verification Method:** Test
- **More Information:** measured with operating-system tools.

#### 3.3.2 Security
- **ID:** REQ-SEC-001
- **Title:** Vault encryption
- **Statement:** The system shall encrypt all user data with AES-256-GCM using a key derived from the master password by PBKDF2-HMAC-SHA256 with at least 600 000 iterations and a random salt of at least 128 bits.
- **Rationale:** Only strong encryption makes a stolen vault file useless to an attacker.
- **Acceptance Criteria:** no plaintext passwords, logins or titles are present in the vault file; the same master password on different devices yields different keys; flipping one ciphertext byte is detected as an authentication failure.
- **Verification Method:** Analysis, Test
- **More Information:** NIST SP 800-63B, OWASP Password Storage Cheat Sheet.

- **ID:** REQ-SEC-002
- **Title:** Key handling in memory
- **Statement:** The system shall keep the encryption key only in RAM, zero the key buffer on lock and on exit, and never write the master password or the key to logs, dumps or files.
- **Rationale:** The in-memory key is the primary target for attackers with local access.
- **Acceptance Criteria:** after locking, decryption is impossible without re-entering the password; logs and temporary files contain no master-password or key strings; code inspection finds no secret persisted to disk.
- **Verification Method:** Analysis, Inspection
- **More Information:** checked during code review and with static analysis.

- **ID:** REQ-SEC-003
- **Title:** TOTP correctness
- **Statement:** The system shall generate and validate TOTP codes per RFC 6238 (HMAC-SHA-1, 6 digits, 30-second step) with a ±1 step tolerance and shall store secrets encrypted only.
- **Rationale:** Compatibility with authenticator applications is critical for the second factor.
- **Acceptance Criteria:** codes match the RFC 6238 test vectors; a code from an adjacent step is accepted and from ±2 steps is not; the secret is not displayed after the setup screen is closed.
- **Verification Method:** Test
- **More Information:** RFC 6238, RFC 4226; [UI-05](mockups/05-two-factor.png).

- **ID:** REQ-SEC-004
- **Title:** Cryptographically strong randomness
- **Statement:** The system shall obtain passwords, salts, nonces and backup codes only from `java.security.SecureRandom`; `java.util.Random` and `Math.random()` are forbidden for these purposes.
- **Rationale:** Predictable randomness nullifies the entire strength of a password.
- **Acceptance Criteria:** static analysis finds no forbidden generators in the `generator`, `vault` and `totp` modules; the character distribution passes a χ² test at the 0.01 level.
- **Verification Method:** Analysis, Test
- **More Information:** enforced by a build rule (SpotBugs/Checkstyle).

- **ID:** REQ-SEC-005
- **Title:** Master-password guessing protection
- **Statement:** The system shall limit master-password guessing: at least 300 ms delay after each failed attempt, a 60-second lockout after five consecutive failures, and logging of the lockout event without disclosing the entered data.
- **Rationale:** Rate limiting makes offline guessing through the UI unprofitable.
- **Acceptance Criteria:** input is unavailable for 60 s on the sixth consecutive attempt; the counter resets after a successful sign-in or after the timeout; events are recorded in the local log.
- **Verification Method:** Test
- **More Information:** related to REQ-FUNC-001 and REQ-OBS-001.

- **ID:** REQ-SEC-006
- **Title:** Minimal network activity
- **Statement:** The system shall make network requests only for the user-enabled breach check, use HTTPS exclusively and contain no telemetry, analytics or auto-update channels that transmit user data.
- **Rationale:** Locality is the core product promise and the basis of user trust.
- **Acceptance Criteria:** with breach checking disabled, a network monitor records no connections from the application; the only permitted domain is `api.pwnedpasswords.com`; default settings enable no network features.
- **Verification Method:** Test, Inspection
- **More Information:** [UI-06](mockups/06-settings.png), "Breached-password check" section.

#### 3.3.3 Reliability
- **ID:** REQ-REL-001
- **Title:** Vault integrity under failures
- **Statement:** The system shall write vault changes atomically (write to a temporary file, verify integrity, replace atomically) and shall keep the previous working version if the operation is interrupted.
- **Rationale:** A power failure or a killed process must not produce an unreadable vault.
- **Acceptance Criteria:** forcing process termination during a save leaves a vault that opens in the pre-change state; no temporary files older than one session remain; a "kill -9 during save" loop (100 of 100 attempts) never corrupts data.
- **Verification Method:** Test
- **More Information:** REQ-FUNC-010.

- **ID:** REQ-REL-002
- **Title:** Recovery after corruption
- **Statement:** The system shall detect vault file corruption, inform the user about the problem and offer recovery from the latest valid backup copy.
- **Rationale:** The user must understand what happened and have a path back to the data.
- **Acceptance Criteria:** the corrupted file is not overwritten; a list of available copies with dates is offered; restoring a copy created by the normal flow succeeds.
- **Verification Method:** Test
- **More Information:** REQ-FUNC-010.

- **ID:** REQ-REL-003
- **Title:** No data loss on concurrent access
- **Statement:** The system shall lock the vault file while running and, when a second application instance starts, shall display "The vault is already open in another window" instead of allowing parallel writes.
- **Rationale:** Two processes with different vault versions overwrite each other's changes.
- **Acceptance Criteria:** the second instance does not modify the file; the message appears within 1 s of start-up; the lock is released after a crash (PID-based lock file).
- **Verification Method:** Test
- **More Information:** covered in the SDD Concurrency view.

#### 3.3.4 Availability
- **ID:** REQ-AVAIL-001
- **Title:** Full offline functionality
- **Statement:** The system shall provide all functions except the breach check and autofill without any network connection.
- **Rationale:** The main scenario is work on a train, in a classroom and on restricted networks.
- **Acceptance Criteria:** with the network interface disabled, unlock, CRUD, generation, 2FA, backup and search all work without errors.
- **Verification Method:** Test
- **More Information:** verified manually and in a network-less CI container.

- **ID:** REQ-AVAIL-002
- **Title:** Resilience to external service outages
- **Statement:** The system shall abort an HIBP request after a 5-second timeout and keep working when the service is unavailable, showing a neutral notification.
- **Rationale:** An external dependency must not block the interface.
- **Acceptance Criteria:** the UI stays responsive under a simulated timeout; an automatic retry happens at most once per day.
- **Verification Method:** Test
- **More Information:** REQ-FUNC-011.

#### 3.3.5 Observability
- **ID:** REQ-OBS-001
- **Title:** Local event log
- **Statement:** The system shall maintain a local log (INFO, WARN, ERROR levels) recording start-up, unlock, lock, save, restore and errors, never writing passwords, keys, TOTP secrets or note content.
- **Rationale:** Diagnostics without violating privacy.
- **Acceptance Criteria:** the log lives in the user directory, rotates at 5 MB with at most three files; a log search finds no test passwords; each line contains time, level and module.
- **Verification Method:** Inspection, Test
- **More Information:** accessible via "About" → "Open log".

- **ID:** REQ-OBS-002
- **Title:** Diagnostics without data disclosure
- **Statement:** The system shall provide a status report (version, OS, vault size, number of entries, 2FA state) for support requests that excludes user secrets.
- **Rationale:** It lets the team help users without requesting their data.
- **Acceptance Criteria:** the report is copied to the clipboard with one button; it contains no logins, passwords or notes.
- **Verification Method:** Inspection
- **More Information:** "About" section of [UI-06](mockups/06-settings.png).

### 3.4 Compliance
- **ID:** REQ-COMP-001
- **Title:** Cryptographic standards compliance
- **Statement:** The system shall use algorithms and parameters compliant with AES-256-GCM (NIST SP 800-38D), PBKDF2 (RFC 8018) and TOTP (RFC 6238), and shall not implement custom cryptography.
- **Rationale:** Reviewed standard primitives and parameters provide defensible strength and simplify verification.
- **Acceptance Criteria:** the encryption specification in the SDD cites the listed standards; KDF parameters and key lengths are stated explicitly; code review finds no home-grown ciphers.
- **Verification Method:** Inspection, Analysis
- **More Information:** R8, R10, R12.

- **ID:** REQ-COMP-002
- **Title:** Personal data handling
- **Statement:** The system shall process personal data (logins, addresses, notes) strictly locally, never share it with third parties and delete it when an entry or the vault is deleted.
- **Rationale:** Required by Law of the Republic of Belarus No. 99-Z and by the user's basic expectations.
- **Acceptance Criteria:** deleting an entry removes it from the vault and, through backup rotation, from later backups; a privacy statement describes local-only processing.
- **Verification Method:** Inspection, Analysis
- **More Information:** R13.

- **ID:** REQ-COMP-003
- **Title:** Licence hygiene of dependencies
- **Statement:** The system shall use only dependencies licensed under Apache-2.0, MIT, BSD or EPL-2.0 and shall ship a `THIRD-PARTY.md` file listing libraries and licences.
- **Rationale:** Removes licence risks when publishing the project openly.
- **Acceptance Criteria:** the build generates a licence report; all runtime dependencies are listed; no GPL dependency is present.
- **Verification Method:** Inspection
- **More Information:** C5 in Section 2.3.

### 3.5 Design and Implementation
#### 3.5.1 Installation
- **ID:** REQ-INST-001
- **Title:** Installation and removal
- **Statement:** The system shall install as a self-contained package bundling the Java 21 runtime, without administrator rights, into a per-user directory, and shall uninstall through standard OS means while offering to keep or delete the vault.
- **Rationale:** Students and staff often lack administrator rights on lab machines.
- **Acceptance Criteria:** installation takes at most 2 minutes; the application starts afterwards without a system-wide JRE; uninstallation keeps the vault by default and warns about it.
- **Verification Method:** Demonstration, Test
- **More Information:** packaged with `jpackage`; see REQ-DIST-001.

#### 3.5.2 Build and Delivery
- **ID:** REQ-BUILD-001
- **Title:** Reproducible build and quality gates
- **Statement:** The build shall run with Maven using pinned dependency and plugin versions, execute JUnit 5 unit tests and static analysis in CI (GitHub Actions) on every push, and publish test and coverage reports.
- **Rationale:** Reproducibility and automated quality gates are prerequisites for another student maintaining the project.
- **Acceptance Criteria:** a build from a fresh clone on a clean machine succeeds without manual steps; failing tests block merging; coverage of the `vault` and `generator` modules is at least 70 %.
- **Verification Method:** Inspection, Test
- **More Information:** CI artefacts: `target/surefire-reports`, JaCoCo report.

#### 3.5.3 Distribution
- **ID:** REQ-DIST-001
- **Title:** Distributions for target platforms
- **Statement:** The system shall be delivered as `.msi` (Windows), `.deb` (Ubuntu 22.04+) and `.dmg` (macOS) installers published as GitHub Release artefacts with SHA-256 checksums.
- **Rationale:** Users should get the installation method familiar on their OS.
- **Acceptance Criteria:** each package installs and launches on its target OS; checksums are published next to the artefacts; the package version matches the release tag.
- **Verification Method:** Test, Demonstration
- **More Information:** for 0.1.0 Windows and Ubuntu are mandatory, macOS is provided where hardware allows.

#### 3.5.4 Maintainability
- **ID:** REQ-MAINT-001
- **Title:** Modular structure and code documentation
- **Statement:** The code shall be split into the modules `ui`, `vault`, `generator`, `totp`, `backup`, `bridge`, `import` and `common`; public classes of `vault`, `generator` and `totp` shall have Javadoc; a single Checkstyle profile shall be enforced.
- **Rationale:** The project passes between students and iterations; readability outweighs brevity.
- **Acceptance Criteria:** module dependencies match the SDD; the Checkstyle-enabled build reports no errors; every public class has Javadoc describing its contract.
- **Verification Method:** Inspection
- **More Information:** the architecture is detailed in the SDD (laboratory work No. 4).

#### 3.5.5 Reusability
- **ID:** REQ-REUSE-001
- **Title:** Reusable components
- **Statement:** The system shall expose `PasswordGenerator`, `TotpService`, `VaultCrypto` and `ClipboardGuard` as JavaFX-independent components with a public API reusable in console utilities and tests.
- **Rationale:** UI independence simplifies testing and lets the logic be reused in other course projects.
- **Acceptance Criteria:** these components import no JavaFX classes; they can be used from a separate Java module without launching the application; each has unit tests.
- **Verification Method:** Inspection, Test
- **More Information:** verified through Maven dependency analysis.

#### 3.5.6 Portability
- **ID:** REQ-PORT-001
- **Title:** Cross-platform behaviour
- **Statement:** The system shall run on Windows 10/11, Ubuntu 22.04+ and macOS 13+ on x86-64 and arm64; platform-specific code is allowed only in the OS integration layer (clipboard, directories, installer).
- **Rationale:** Students and lecturers use different operating systems; the product must not be tied to one platform.
- **Acceptance Criteria:** the same source tree builds and passes tests on all three OS families in CI; behavioural differences are limited to file paths and dialog appearance.
- **Verification Method:** Test, Inspection
- **More Information:** CI matrix: windows-latest, ubuntu-22.04, macos-13.

#### 3.5.7 Cost
- **ID:** REQ-COST-001
- **Title:** Zero operating cost
- **Statement:** The project shall use only free open-source tooling and require no paid infrastructure: storage is a local disk, CI uses the free GitHub Actions tier and the build uses Maven Central.
- **Rationale:** The project has no budget and the course forbids subscriptions.
- **Acceptance Criteria:** no paid component exists in the build or delivery chain; monthly spending is 0 BYN; dependency licences satisfy REQ-COMP-003.
- **Verification Method:** Analysis
- **More Information:** C5 in Section 2.3.

#### 3.5.8 Deadline
- **ID:** REQ-DEAD-001
- **Title:** Semester milestones
- **Statement:** The project shall follow the milestones: M1 — 2026-11-08 (vault, CRUD, generator), M2 — 2026-12-06 (2FA, settings, backups, installer), M3 — 2026-12-20 (autofill, documentation, defence).
- **Rationale:** The schedule drives requirement apportioning and MoSCoW prioritisation.
- **Acceptance Criteria:** each milestone includes a demo and updated SRS/SDD; requirements from Section 2.6 are delivered in the matching iteration or explicitly deferred with justification.
- **Verification Method:** Inspection, Demonstration
- **More Information:** see Section 2.6.

#### 3.5.9 Proof of Concept
- **ID:** REQ-POC-001
- **Title:** PoC of the encrypted vault and JavaFX navigation
- **Statement:** Before 2026-11-01 the team shall prove feasibility: encrypt and decrypt a test entry set with timing measurements, demonstrate JavaFX navigation across three screens and exchange a Native Messaging message with a test extension.
- **Rationale:** The three key technical risks are validated before main development to avoid re-architecting.
- **Acceptance Criteria:** the PoC unlocks a vault with 1000 entries within 1.5 s; screen transitions work; an extension message is accepted; results are recorded in the PoC README.
- **Verification Method:** Demonstration
- **More Information:** PoC code is kept out of the documentation branch; it lives in a dedicated branch when needed.

#### 3.5.10 Change Management
- **ID:** REQ-CM-001
- **Title:** Version and change management
- **Statement:** The project shall use Git with one branch per laboratory work, semantic versioning (`MAJOR.MINOR.PATCH`), pull requests reviewed by the partner and a maintained `CHANGELOG.md`.
- **Rationale:** A transparent change history is needed by the lecturer to assess contribution and by the team to merge safely.
- **Acceptance Criteria:** every PR references a requirement; vault-format breaking changes increment MAJOR and ship a migration; `CHANGELOG.md` contains an entry for every version.
- **Verification Method:** Inspection
- **More Information:** [`CONTRIBUTING.md`](../CONTRIBUTING.md).

### 3.6 AI/ML
This section is **not applicable** to version 0.1.0: "Larets" uses no machine learning, neural networks or generative models. Password strength is estimated by a deterministic entropy formula and passwords are produced by a cryptographically secure random generator. If version 0.3 introduces a local anomaly-detection model for access attempts, this section will be completed in full.

#### 3.6.1 Model Specification
Not applicable.

#### 3.6.2 Data Management
Not applicable. User data is never used to train any model.

#### 3.6.3 Guardrails
Not applicable. The role of guardrails is performed by the security requirements in Section 3.3.2.

#### 3.6.4 Ethics
Not applicable. The ethical dimension of the product is covered by REQ-COMP-002 (local-only processing of personal data).

#### 3.6.5 Human-in-the-Loop
Not applicable. Every action in the system is initiated by the user.

#### 3.6.6 Model Lifecycle and Operations
Not applicable.

## 4. Verification
Methods: **Test** — an automated or manual test with an expected result; **Analysis** — calculation, modelling or expert assessment of parameters; **Inspection** — review of artefacts (code, configuration, documents); **Demonstration** — showing a working feature to the customer. Test artefacts will be produced in laboratory work No. 5, so the "Test/Artifact Link" column lists planned test-suite names.

| Requirement ID | Verification Method | Test/Artifact Link | Status | Evidence |
|----------------|---------------------|--------------------|--------|----------|
| REQ-INT-001 | demonstration, test | tests/ui/T01-unlock.md | Planned | [01-unlock-screen.png](mockups/01-unlock-screen.png) |
| REQ-INT-002 | demonstration, inspection | tests/ui/T02-vault.md | Planned | [02-vault-screen.png](mockups/02-vault-screen.png) |
| REQ-INT-003 | test, inspection | tests/ui/T03-editor.md | Planned | [03-entry-editor.png](mockups/03-entry-editor.png) |
| REQ-INT-004 | test, demonstration | tests/ui/T04-generator.md | Planned | [04-generator.png](mockups/04-generator.png) |
| REQ-INT-005 | demonstration, test | tests/totp/T05-setup.md | Planned | [05-two-factor.png](mockups/05-two-factor.png) |
| REQ-INT-006 | test, inspection | tests/ui/T06-settings.md | Planned | [06-settings.png](mockups/06-settings.png) |
| REQ-INT-007 | test | tests/bridge/T07-native-messaging.md | Planned | — |
| REQ-INT-008 | test, analysis | tests/vault/T08-format.md | Planned | — |
| REQ-INT-009 | test | tests/ui/T09-clipboard.md | Planned | — |
| REQ-INT-010 | analysis, demonstration | docs/hardware-baseline.md | Planned | — |
| REQ-FUNC-001 | test | tests/vault/T10-unlock.md | Planned | [01-unlock-screen.png](mockups/01-unlock-screen.png) |
| REQ-FUNC-002 | test | tests/vault/T11-search.md | Planned | — |
| REQ-FUNC-003 | test | tests/vault/T12-crud.md | Planned | — |
| REQ-FUNC-004 | test | tests/ui/T13-copy.md | Planned | — |
| REQ-FUNC-005 | test, analysis | tests/generator/T14-generate.md | Planned | [04-generator.png](mockups/04-generator.png) |
| REQ-FUNC-006 | test | tests/vault/T15-categories.md | Planned | — |
| REQ-FUNC-007 | test, analysis | tests/totp/T16-totp.md | Planned | [05-two-factor.png](mockups/05-two-factor.png) |
| REQ-FUNC-008 | test | tests/vault/T17-autolock.md | Planned | [06-settings.png](mockups/06-settings.png) |
| REQ-FUNC-009 | test, demonstration | tests/bridge/T18-autofill.md | Planned | — |
| REQ-FUNC-010 | test | tests/backup/T19-backup.md | Planned | — |
| REQ-FUNC-011 | test, inspection | tests/leaks/T20-hibp.md | Planned | — |
| REQ-FUNC-012 | test | tests/import/T21-csv.md | Planned | — |
| REQ-PERF-001 | test | tests/perf/T22-latency.md | Planned | — |
| REQ-PERF-002 | test | tests/perf/T23-resources.md | Planned | — |
| REQ-SEC-001 | analysis, test | docs/crypto-spec.md, tests/vault/T24-crypto.md | Planned | — |
| REQ-SEC-002 | analysis, inspection | docs/key-handling.md | Planned | — |
| REQ-SEC-003 | test | tests/totp/T25-rfc-vectors.md | Planned | RFC 6238 test vectors |
| REQ-SEC-004 | analysis, test | build/spotbugs-xml.xml, tests/generator/T26-rng.md | Planned | — |
| REQ-SEC-005 | test | tests/vault/T27-lockout.md | Planned | — |
| REQ-SEC-006 | test, inspection | tests/net/T28-no-network.md | Planned | — |
| REQ-REL-001 | test | tests/vault/T29-atomic-save.md | Planned | — |
| REQ-REL-002 | test | tests/backup/T30-recovery.md | Planned | — |
| REQ-REL-003 | test | tests/vault/T31-single-instance.md | Planned | — |
| REQ-AVAIL-001 | test | tests/net/T32-offline.md | Planned | — |
| REQ-AVAIL-002 | test | tests/leaks/T33-timeout.md | Planned | — |
| REQ-OBS-001 | inspection, test | tests/log/T34-logging.md | Planned | — |
| REQ-OBS-002 | inspection | docs/support-report.md | Planned | — |
| REQ-COMP-001 | inspection, analysis | docs/crypto-spec.md | Planned | — |
| REQ-COMP-002 | inspection, analysis | docs/privacy.md | Planned | — |
| REQ-COMP-003 | inspection | THIRD-PARTY.md | Planned | — |
| REQ-INST-001 | demonstration, test | tests/install/T35-install.md | Planned | — |
| REQ-BUILD-001 | inspection, test | .github/workflows/build.yml | Planned | — |
| REQ-DIST-001 | test, demonstration | release/manifest.md | Planned | — |
| REQ-MAINT-001 | inspection | checkstyle.xml, javadoc | Planned | — |
| REQ-REUSE-001 | inspection, test | tests/core/T36-modularity.md | Planned | — |
| REQ-PORT-001 | test, inspection | .github/workflows/build.yml (matrix) | Planned | — |
| REQ-COST-001 | analysis | docs/cost.md | Planned | — |
| REQ-DEAD-001 | inspection, demonstration | docs/roadmap.md | Planned | — |
| REQ-POC-001 | demonstration | README-PoC.md | Planned | — |
| REQ-CM-001 | inspection | CONTRIBUTING.md, CHANGELOG.md | Planned | — |

## 5. Appendixes

### 5.1 Customer Interview Record
Date: 2026-10-23. Participants: the customer (course role) and the project team (two people). Format: 30-minute face-to-face session.

| # | Question | Customer answer | Requirement |
|---|----------|-----------------|-------------|
| 1 | Why do you need a password manager if browsers have one? | "Browser managers sync passwords to the cloud. I need a local vault that works without the internet." | REQ-AVAIL-001, REQ-SEC-006 |
| 2 | What data must be stored? | "Site, login, password, comment. Sometimes one-time codes." | REQ-FUNC-003, REQ-FUNC-007 |
| 3 | How many entries? | "About 80 for me, up to 300 for colleagues." | REQ-PERF-001, REQ-FUNC-002 |
| 4 | How often do you look up a password? | "Several times a day, usually by site name." | REQ-FUNC-002 |
| 5 | What annoys you in existing tools? | "Slow master-password entry and the inability to generate a password right inside the sign-up form." | REQ-PERF-001, REQ-FUNC-005, REQ-INT-003 |
| 6 | Do you need two-factor authentication? | "Yes, for the vault itself. And I want to see site codes without reaching for my phone." | REQ-FUNC-007, REQ-SEC-003 |
| 7 | What if the computer is lost? | "I need backups, but they must be unreadable without the password." | REQ-FUNC-010, REQ-SEC-001 |
| 8 | Do you need sync between devices? | "Not this semester — start with local operation." | Section 1.2 (exclusion), REQ-COST-001 |
| 9 | What about online breach checking? | "Useful, but only if I turn it on myself." | REQ-FUNC-011, REQ-SEC-006 |
| 10 | Must the program be installed on lab computers? | "Yes, and there are no administrator rights there." | REQ-INST-001 |
| 11 | Which operating systems will you use? | "Windows at home, Ubuntu at the university." | REQ-PORT-001, REQ-DIST-001 |
| 12 | What matters more by the end of the semester — autofill or 2FA? | "2FA matters more; autofill can come later." | Section 2.6 |

**Business goals agreed with the customer:**

1. Reduce the time to reach a required password to 5 seconds (currently 30 seconds or more).
2. Eliminate password reuse: at least 90 % of the user's entries must have a unique generated password.
3. Guarantee that the application makes no network connections by default.
4. Let the user restore data after a failure in one step.

### 5.2 Graphical Artefacts (SysML v2 → PNG)
| PNG file | Model definition | Model file | Used by |
|----------|------------------|------------|---------|
| [`01-unlock-screen.png`](mockups/01-unlock-screen.png) | `UnlockScreen` | [`ui-mockups.sysml`](mockups/ui-mockups.sysml) | REQ-INT-001, REQ-FUNC-001, REQ-SEC-005 |
| [`02-vault-screen.png`](mockups/02-vault-screen.png) | `VaultScreen` | [`ui-mockups.sysml`](mockups/ui-mockups.sysml) | REQ-INT-002, REQ-FUNC-002…004, REQ-INT-009 |
| [`03-entry-editor.png`](mockups/03-entry-editor.png) | `EntryEditorScreen` | [`ui-mockups.sysml`](mockups/ui-mockups.sysml) | REQ-INT-003, REQ-FUNC-003, REQ-FUNC-005 |
| [`04-generator.png`](mockups/04-generator.png) | `GeneratorScreen` | [`ui-mockups.sysml`](mockups/ui-mockups.sysml) | REQ-INT-004, REQ-FUNC-005, REQ-SEC-004 |
| [`05-two-factor.png`](mockups/05-two-factor.png) | `TwoFactorScreen` | [`ui-mockups.sysml`](mockups/ui-mockups.sysml) | REQ-INT-005, REQ-FUNC-007, REQ-SEC-003 |
| [`06-settings.png`](mockups/06-settings.png) | `SettingsScreen` | [`ui-mockups.sysml`](mockups/ui-mockups.sysml) | REQ-INT-006, REQ-FUNC-008…011 |
| [`07-system-context.png`](mockups/07-system-context.png) | `SystemContextDiagram` | [`use-case-context.sysml`](mockups/use-case-context.sysml) | Section 2.1 |
| [`08-use-cases.png`](mockups/08-use-cases.png) | `UseCaseDiagram` | [`use-case-context.sysml`](mockups/use-case-context.sysml) | Section 2.2 |

All images are produced by automatic rendering of the model:

```bash
cd srs/mockups
python3 render_mockups.py --extra use-case-context.sysml
```

### 5.3 Business Goal → Requirement → Artefact Traceability
| Business goal (Section 5.1) | Requirements | Artefact |
|-----------------------------|--------------|----------|
| BG-1. Reach a password in 5 seconds | REQ-FUNC-002, REQ-FUNC-004, REQ-PERF-001, REQ-INT-002 | [02-vault-screen.png](mockups/02-vault-screen.png) |
| BG-2. Unique strong passwords | REQ-FUNC-005, REQ-SEC-004, REQ-FUNC-011 | [04-generator.png](mockups/04-generator.png) |
| BG-3. No network connections by default | REQ-SEC-006, REQ-AVAIL-001, REQ-FUNC-011 | [06-settings.png](mockups/06-settings.png) |
| BG-4. One-step data restore | REQ-FUNC-010, REQ-REL-001, REQ-REL-002 | [06-settings.png](mockups/06-settings.png) |
| Additional: second-factor protection | REQ-FUNC-007, REQ-SEC-003, REQ-INT-005 | [05-two-factor.png](mockups/05-two-factor.png) |

### 5.4 Threat Model (Summary)
| Threat | Scenario | Mitigation |
|--------|----------|------------|
| T1. Vault file theft | Copying `vault.db` from the disk or a backup | REQ-SEC-001 (AES-256-GCM + PBKDF2) |
| T2. Master-password guessing through the UI | Automated entry attempts | REQ-SEC-005, REQ-FUNC-001 |
| T3. In-memory secret interception | Process dump, malware | REQ-SEC-002 (key zeroing) |
| T4. Clipboard leakage | Another application reads the clipboard | REQ-INT-009 (clear after 20 s) |
| T5. Malicious browser extension | A rogue extension requests data | REQ-INT-007 (narrow protocol), REQ-FUNC-009 |
| T6. Unattended workstation | Window left open | REQ-FUNC-008 (auto-lock) |
| T7. Data loss on failure | Interrupted write, disk damage | REQ-REL-001, REQ-REL-002, REQ-FUNC-010 |

### 5.5 Tools Used
| Task | Tool |
|------|------|
| Requirements documentation | Markdown (`srs/srs-template.md`, `srs/srs-template-en.md`) |
| GUI prototyping | SysML v2 (`srs/mockups/*.sysml`) with the `ui-library.sysml` element library |
| PNG generation | `srs/mockups/render_mockups.py` (Python 3 + Pillow) |
| Version control | Git, dedicated laboratory-work branch, pull request into `main` |
