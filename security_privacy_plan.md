# MiniFigure 3D Studio — Security and Privacy Plan

**Author:** Manus AI  
**Status:** Stage 1 proposal  
**Scope:** Local Windows desktop application, optional local engines, and opt-in external AI adapters

## 1. Security and Privacy Objectives

MiniFigure 3D Studio processes photographs, body appearance, face likeness, derived masks, textures, 3D geometry, names placed on bases, and external-provider credentials. The design therefore treats every project as sensitive by default, even when the user intends to publish the final model.

The principal objectives are to keep processing local unless the user knowingly selects an external service, minimize data sent outside the device, prevent secrets and images from entering logs, make engine and model provenance visible, limit damage from malformed files or native-process crashes, and provide truthful deletion behavior.

> **Privacy default:** No photograph, mask, texture, model, diagnostic bundle, or usage analytic leaves the computer unless the user explicitly enables a named operation that requires it and confirms the transfer.

## 2. Data Classification

| Class | Examples | Default handling |
|---|---|---|
| Restricted project data | Source photographs, face/body likeness, masks, textures, generated models, camera reconstruction, person name | Local project storage; excluded from logs and telemetry; explicit consent required for external transfer. |
| Secret | API keys, authorization tokens, provider credentials | Windows Credential Manager or DPAPI preferred; `.env` compatibility allowed with restrictive local storage; never stored in project or logs. |
| Sensitive metadata | EXIF, full local paths, camera model, timestamps, provider request IDs, engine manifests | Strip unneeded EXIF before external use; use project-relative identifiers in ordinary logs; retain only what is needed for reproducibility. |
| Operational metadata | Stage IDs, duration, error codes, non-sensitive versions, polygon and dimension metrics | May appear in local logs with bounded retention. No remote analytics by default. |
| Public application data | Bundled help, synthetic examples, icons, translations, license notices | Shipped with the application and safe to display. |

## 3. Data Lifecycle

The project lifecycle is explicit: import, analyze, derive, generate, repair, validate, export, retain, and delete. Each transition records the producing stage and artifact hashes. Original images are immutable; masks, normalized images, and thumbnails are derived artifacts with separate retention policies.

| Lifecycle event | Data created or moved | Control |
|---|---|---|
| Import | Managed copy, safe alias, hash, normalized preview | User chooses project folder; application does not modify the external original. |
| Quality analysis | Numeric findings and optional derived overlays | No face crops or thumbnails in logs. |
| Masking | Model input, mask revisions, cutout | Local by default; model asset and license pinned. |
| Local generation | Primary image copied to engine staging, raw mesh/textures | Staging is project-scoped, access-limited where practical, and cleaned after commit/cancel. |
| Accurate Scan | COLMAP database, camera poses, point clouds, dense workspace | Local, potentially large; retention options shown before processing. |
| External generation | User-approved image and parameters transmitted | Provider, purpose, endpoint, fields, and consent recorded before transfer. |
| Blender processing | Mesh backups, temporary `.blend`, previews, reports | No secret-bearing environment; structured result only. |
| Export | Selected final files and report | Destination verified; no hidden upload or cloud synchronization controlled by the app. |
| Delete originals | Managed source images removed | UI explains that derived likeness data may remain. |
| Delete project | Managed project tree and known caches removed | Active jobs stopped, file locks closed, failures reported, best-effort cleanup accurately labeled. |

## 4. Consent Model

Consent is attached to a concrete purpose, provider, data category, and adapter version. A general “I agree” at installation is insufficient for sending a person's photograph to an external service.

| Consent point | Required disclosure |
|---|---|
| New project | Reminder that the user must have permission to process the photographed person. |
| External adapter selection | Service legal name, local versus remote distinction, data categories, purpose, and link to current provider information. |
| Transfer confirmation | Exact selected image count, whether EXIF is stripped, request parameters, and that the transfer will begin only after confirmation. |
| Remembered consent | Narrow scope, visible expiration/revocation, and re-prompt on provider, policy, endpoint, or material adapter change. |
| Diagnostic sharing | Preview of files and fields; explicit user save/share action. No automatic submission. |

Consent records store no image and no secret. They include the provider ID, purpose, data categories, policy/adapter version, locale, time, and decision. Declining consent returns the user to local adapters without degrading unrelated local functions.

## 5. Local Secrets

Microsoft recommends Windows Credential Manager for credentials and DPAPI for persisted local secrets, and warns that secrets must not be hard-coded or logged.[1] The design uses the following priority:

| Priority | Mechanism | Policy |
|---|---|---|
| 1 | Windows Credential Manager | Preferred for provider API keys; project stores only a credential reference. |
| 2 | DPAPI-protected application secret store | Acceptable for local secret material requiring application-managed metadata. |
| 3 | User-local `.env` file | Supported to satisfy compatibility requirements; excluded from source control, projects, logs, diagnostic bundles, and broad backups by default. |
| Never | Source code, command line, project manifest, plaintext log | Prohibited. |

The `.env` path should reside under the user-local application configuration directory rather than beside application binaries or project files. File permissions should be restricted to the current user where practical. The UI should offer **Import from `.env` and protect with Windows** rather than describe `.env` as inherently secure.

Child processes receive a minimal environment. API keys are not placed in command-line arguments. Blender and COLMAP never receive external-provider secrets. A provider worker retrieves its own referenced credential immediately before the request and minimizes its lifetime.

## 6. Logging and Diagnostics

OWASP advises removing, masking, sanitizing, hashing, or encrypting access tokens, passwords, keys, sensitive personal data, unconsented data, and other protected values before logging; it also notes that file paths can require special treatment.[2]

| Log content | Allowed | Prohibited |
|---|---|---|
| Job identity | Random project/run/stage UUID or short alias | Person name as a routing key. |
| Paths | Project-relative safe path or hashed alias | Full source-photo path in normal logs. |
| Images | None | Pixels, thumbnails, masks, textures, base64, EXIF thumbnails. |
| Credentials | Provider configured: yes/no | Key, token, authorization header, full environment. |
| External response | Status code, provider request ID when safe, categorized error | Full body by default, especially if it can echo prompts, images, or credentials. |
| Engine output | Redacted bounded excerpt and stored local technical log | Unlimited stdout/stderr copied to clipboard. |
| Geometry | Counts, dimensions, hashes, finding codes | Binary model content in logs. |

The simplified log is user-readable and translated. The technical log remains local, UTF-8, size-limited, and redacted. **Copy Error** uses a safe template. **Export Diagnostic Bundle** shows a preview and allows the user to exclude path aliases or engine logs before saving.

## 7. Threat Model and Controls

| Threat | Example | Preventive control | Detection/recovery |
|---|---|---|---|
| Command injection | Crafted project name alters Blender command | Use executable plus argument vector through `QProcess`; generated safe paths; no shell interpolation. | Contract tests with quotes, spaces, Unicode, and metacharacters. |
| Path traversal | Imported filename writes outside project | Generate internal UUID filenames and validate canonical paths remain under managed roots. | Reject artifact paths escaping staging; log stable code. |
| Malformed image/model | Native decoder or importer crash | Decode/process in worker; enforce size limits; pin supported formats; validate before GUI use. | Worker crash isolation and retry with safe explanation. |
| Zip/XML bomb | Hostile GLB/3MF/archives consume memory/disk | File-size and expansion limits, bounded parsing, trusted libraries, staging quota. | Abort, mark input invalid, remove staging. |
| Viewer content injection | Model metadata injects script/HTML | Treat metadata as text; strict schema; CSP; local assets; disable navigation and remote requests. | Recreate renderer; security test fixtures. |
| Secret leakage | Key appears in logs or command line | Credential reference, redaction, minimal child environment, never serialize key into job protocol. | Automated secret-pattern scan on logs and diagnostic bundles. |
| Silent external upload | Library downloads model or sends analytics | Network-deny core tests, adapter allowlist, explicit engine installer, request interception. | Local network audit tests and visible outbound state. |
| Supply-chain compromise | Replaced model or engine binary | Signed manifests, SHA-256 checks, pinned sources, SBOM, vulnerability scanning. | Refuse mismatched package, roll back to last valid engine. |
| DLL search-order abuse | Malicious DLL loaded from project folder | Controlled application DLL directories, no current-directory loading, signed installer, safe subprocess working directories. | Clean-machine and planted-DLL security tests. |
| TOCTOU/artifact replacement | Output file changed after validation | Hash staged artifact, validate, atomically commit, re-check on later use. | Hash mismatch invalidates cache and blocks export. |
| Symlink/junction escape | Project deletion removes unintended files | Refuse traversal outside managed root; do not follow reparse points during recursive deletion without policy. | Stop deletion and report exact category safely. |
| GPU/native crash | Engine destabilizes application | Separate process and bounded resource supervision. | Preserve last committed checkpoint and surface actual engine status. |
| License circumvention | Hunyuan enabled in excluded territory | Separate package/release policy, eligibility gate, pinned license hash, disabled adapter when unlicensed. | Audit engine manifest and block run before image staging. |

## 8. Engine and Model Supply Chain

Every optional runtime has a manifest containing package ID, version, architecture, source URL, release date, binary and asset hashes, signing identity where available, license identifier and hash, supported regions, required notices, dependencies, capabilities, minimum application protocol, and self-test result.

The engine manager performs download only after explicit user action and license display. Downloads use HTTPS, resumable staging, size limits, checksum verification, and atomic installation. The application does not execute a downloaded package before validation. Rollback retains the previous validated engine until the new self-test succeeds.

Hunyuan3D 2.1 requires special treatment because the reviewed community license excludes the European Union, United Kingdom, and South Korea and restricts use and distribution outside the licensed territory.[3] The universal installer must not contain those works under the reviewed license. A separate license or alternative engine is required for excluded territories.

## 9. External API Security

External providers implement a common adapter contract but keep provider-specific HTTP details private. The adapter must expose its service name, endpoint domains, uploaded fields, supported inputs, retention/privacy links, timeout behavior, and cancellation limitations before it is eligible for the UI.

| Control | Requirement |
|---|---|
| Transport | HTTPS with normal certificate verification; no user-facing “ignore TLS errors” option. |
| Authentication | Retrieve secret by reference; never log or persist request headers. |
| Data minimization | Send only the selected image and necessary parameters; strip unneeded EXIF. |
| Timeouts | Separate connect/read/overall limits; show whether remote processing may continue after local cancellation. |
| Retries | Retry only safe/idempotent operations or provider-supported resumable jobs; prevent duplicate paid submissions. |
| Response validation | Enforce content type, size, schema, download hash where available, and safe archive extraction. |
| Cancellation | Distinguish cancelling local polling from cancelling the provider job; state the actual result. |
| Cost | Display provider pricing responsibility or unknown status without making billing commitments. |

## 10. Privacy-Preserving Viewer

The viewer uses a pinned local Three.js build. Network access is denied through a restrictive content-security policy and Qt WebEngine request interception. Only a narrow schema-validated WebChannel bridge is exposed. The viewer cannot enumerate project files, open arbitrary local paths, navigate, create popups, or initiate uncontrolled downloads.

Models are copied or exposed to a viewer-specific read-only cache using generated names. Source image paths and provider credentials never cross the bridge. Screenshots are created only after a user action and written to a selected path.

## 11. Project Storage and Retention

The application offers retention choices at project creation and in Privacy settings. The conservative default keeps originals and derived assets locally until the user deletes them, because automatic deletion could destroy the only reproducible inputs. A post-generation reminder offers to delete imported originals while clearly listing remaining derived likeness data.

| Data category | Default retention | User control |
|---|---|---|
| Imported originals | Project lifetime | Delete after generation or manually. |
| Normalized working copies | Project lifetime while originals exist; review after original deletion | Remove with originals when no stage depends on them. |
| Masks and cutouts | Project lifetime | Delete separately with impact warning. |
| Raw engine outputs | Retain latest successful run | Remove intermediates after accepted processed artifact. |
| COLMAP dense workspace | Retain until user accepts mesh; large-size warning | Remove dense intermediates while preserving selected results. |
| Processed models/reports | Project lifetime | User-controlled. |
| Logs | Bounded by days and size | Clear now; exclude from project backup. |
| Engine/model packages | Application-wide | Uninstall independently; does not delete projects. |

## 12. Delete Project and Enhanced Local Cleanup

Delete Project first acquires a project-wide operation lock, requests cancellation, waits or terminates supervised process trees, closes viewer and file handles, and inventories managed content. The confirmation separates originals, derived likeness data, exports, logs, and optional shared caches.

Deletion does not follow unexpected reparse points or delete outside the canonical project root. Each category is removed, failures are collected, and the result reports Complete, Complete with Remaining Items, or Failed. The application never reports success merely because the top-level folder disappeared.

NIST defines media sanitization as rendering access to target data infeasible for a chosen level of effort and treats sanitization as media- and risk-dependent.[4] An application-level overwrite and delete cannot guarantee sanitization across SSD wear leveling, snapshots, cloud synchronization, backups, or filesystem metadata. Therefore:

| Label | Meaning |
|---|---|
| Delete Project | Remove the managed project and known application artifacts. |
| Enhanced Local Cleanup | Best-effort overwrite of eligible regular files before deletion plus cache cleanup; not a device-sanitization guarantee. |
| Device sanitization | Outside application scope; user follows storage/vendor/organizational procedure appropriate to the threat model. |

The documentation recommends full-disk encryption and separately deleting cloud or backup copies. A deletion receipt records categories, counts, time, and failures without retaining sensitive filenames in external telemetry.

## 13. Privacy by Design for Tests and Support

No real-person photographs enter the repository. Synthetic images and programmatically generated meshes are preferred. Any licensed test asset has an asset manifest recording source, license, permitted use, and checksum.

Crash and support flows do not auto-attach projects. Diagnostic bundles are locally generated, previewable ZIP files containing selected redacted logs, configuration without secrets, engine manifests, and system capability data. Image or model attachment requires a separate explicit file selection and warning.

## 14. Compliance and Release Checklist

| Gate | Pass condition |
|---|---|
| Secrets | Automated scans find no hard-coded keys; keys do not appear in logs, process command lines, project files, or diagnostic bundles. |
| Network | Core application and local workflows pass with all outbound network blocked. |
| Consent | Every external transfer is impossible without a current matching consent record or immediate confirmation. |
| Models | Each installed model has source, revision, checksum, license hash, region policy, and explicit installation event. |
| Dependencies | SBOM and third-party notices match the exact shipped environment. |
| Viewer | CSP and request interception block remote resources and navigation. |
| Paths | Arabic, long, spaced, quoted, and metacharacter paths pass import, processing, export, and deletion tests. |
| Deletion | Active jobs stop; managed files are inventoried; failures are reported; no reparse-point escape occurs. |
| Logs | Redaction unit tests and seeded-secret scans pass. |
| Updates | Engine package signature/hash failure is blocked and previous version remains usable. |

## 15. Open Security and Privacy Decisions

| Decision | Recommendation |
|---|---|
| Project encryption | Evaluate an optional per-project encrypted container or per-artifact encryption in Stage 3; do not delay basic local-first MVP if full-disk encryption guidance is clear. |
| Analytics | Keep disabled and unimplemented initially. If added later, require separate opt-in and a data inventory that excludes likeness data. |
| Crash reporting | Local report by default. Any remote crash service requires a new consent and scrubbing design. |
| External provider history | Store only provider/job IDs needed for recovery, with user-clearable history. |
| Hunyuan region policy | Require legal review and a compliant alternative before worldwide release. |
| Background model | Select only after commercial-rights and redistribution review; do not inherit a library's default silently. |

## References

[1]: https://learn.microsoft.com/en-us/windows/win32/secbp/handling-passwords "Microsoft: Handling Passwords"
[2]: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html "OWASP Logging Cheat Sheet"
[3]: https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2.1/main/LICENSE "Tencent Hunyuan 3D 2.1 Community License"
[4]: https://csrc.nist.gov/pubs/sp/800/88/r2/final "NIST SP 800-88 Rev. 2: Guidelines for Media Sanitization"
