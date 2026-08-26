# MiniFigure 3D Studio — Stage 2 Test Matrix

**Author:** Manus AI  
**Status:** Planned verification; no test is reported as executed

## 1. Evidence Rules

Every result records its test ID, source revision, environment manifest, command or job ID, start/end time, result, duration, relevant versions, and evidence artifacts. Allowed results are **Passed**, **Failed**, **Skipped**, **Not Run**, or **Blocked**. Only Passed satisfies a gate. A test skipped because Blender, a GPU, an operating-system tier, or a model is unavailable remains unsatisfied.

Synthetic images and meshes are the repository default. Real-person photographs do not enter source control, CI artifacts, screenshots, or diagnostic bundles. Any approved local manual test with a real person remains outside the repository and records permission without copying the image into the report.

## 2. Environment Codes

| Code | Environment |
|---|---|
| U | Portable Python 3.11 unit-test environment. |
| W11-C | Native Windows 11 x64 CPU environment. |
| W11-G | Native Windows 11 x64 with the supported GPU/runtime for the selected generator. |
| W10-C | Clean Windows 10 x64 CPU smoke environment. |
| WN | Native Windows environment with outbound networking denied. |
| WF | Native Windows fault-injection environment. |
| BL | Supported real Blender LTS in background mode. |
| VW | Qt WebEngine plus bundled viewer on native Windows. |
| PKG | Clean machine running the Stage 2 development package. |

## 3. Repository, Domain, and Schema Tests

| ID | Test | Env | Pass criterion | Gate |
|---|---|---|---|---|
| FND-001 | Root metadata and tool configuration parse | U/W11-C | Build metadata, test, lint, and type settings load successfully. | M1 |
| FND-002 | Secret scan | U | Seeded secret is detected; repository baseline contains none. | M1/M12 |
| FND-003 | Asset manifest completeness | U | Every binary fixture is declared with source/license/hash/purpose; seeded unknown file fails. | M1/M12 |
| FND-004 | Real-person fixture policy | U | Unexpected photo/EXIF risk is flagged; approved synthetic set passes. | M1 |
| DOM-001 | Project value-object invariants | U | Invalid IDs, versions, names, and state references are rejected. | M2 |
| DOM-002 | Artifact immutability/provenance | U | Mutation and parent/run mismatch fail; valid lineage round-trips. | M2 |
| DOM-003 | Task state transitions | U | Allowed transitions pass and illegal transitions fail. | M4 |
| DOM-004 | Error retryability rules | U | Codes derive correct user action and retry eligibility. | M4 |
| SCH-001 | Project schema fixtures | U | Valid fixture passes; required-field/type/path violations fail. | M2 |
| SCH-002 | Engine manifest schema | U | License, region, hash, protocol, capability, and self-test omissions fail. | M6/M9 |
| SCH-003 | Worker request/result schemas | U | Versioned examples pass; stale IDs, absolute external paths, and malformed outputs fail. | M4 |
| SCH-004 | Validation report schema | U | Three states and findings validate; blocker/status inconsistency fails. | M11 |
| ARCH-001 | Domain import boundaries | U | Domain/models import no PySide6, HTTP, Blender, ONNX, or generator runtime. | M1–M12 |
| ARCH-002 | UI/service boundary | U | UI does not launch raw subprocesses or construct engine commands. | M3–M12 |

## 4. Filesystem, Project, Recovery, and Privacy Tests

| ID | Test | Env | Pass criterion | Gate |
|---|---|---|---|---|
| FS-001 | Atomic manifest commit | W11-C/WF | Failure before replace leaves prior manifest valid; success commits complete new manifest. | M2 |
| FS-002 | Stage then promote artifact | W11-C | Unvalidated staging is absent from project authority; valid artifact promotes with hash/provenance. | M2 |
| FS-003 | Path traversal rejection | W11-C | `..`, absolute external paths, drive changes, and crafted separators cannot escape roots. | M2 |
| FS-004 | Reparse-point deletion guard | W11-C | Deletion does not follow unexpected junction/symlink outside project; result reports it. | M2 |
| FS-005 | Arabic and mixed path round trip | W11-C | Create/open/write/hash/reopen/delete works with Arabic, spaces, quotes, and long names. | M2 |
| FS-006 | Locked-file deletion | WF | Deletion reports remaining locked file and does not claim Complete. | M2 |
| FS-007 | Disk-full atomic write | WF | Existing valid file remains intact; staged partial is reported/cleaned. | M2/M11 |
| REC-001 | Interrupted running-stage recovery | WF | Restart identifies abandoned stage and retains last committed artifact. | M2/M4 |
| REC-002 | Unknown future project schema | U/W11-C | Opens read-only with clear error; no destructive migration. | M2 |
| REC-003 | Known migration | U/W11-C | Migration deterministic, backup preserved, output schema valid. | M2 |
| LOG-001 | Log redaction | U | Seeded keys, auth headers, passwords, unsafe paths, and image markers are absent. | M2/M4 |
| LOG-002 | Copy Error redaction | W11-C | Clipboard contains useful diagnostics but no seeded secret/path. | M4 |
| LOG-003 | Bounded retention | U/W11-C | Limits rotate safely and never delete project artifacts. | M2 |
| PRIV-001 | Local workflow network deny | WN | No outbound request from shell, image, viewer, Blender, or local generator path. | M12 |
| PRIV-002 | Diagnostic bundle preview | W11-C | Images/secrets excluded by default; preview matches saved bundle. | M12 |
| DEL-001 | Delete originals semantics | W11-C | Managed originals removed; remaining masks/models/derived likeness data listed. | M12 |
| DEL-002 | Enhanced cleanup wording | W11-C | UI/report says best-effort and never guarantees device sanitization. | M12 |

## 5. UI and Localization Tests

| ID | Test | Env | Pass criterion | Gate |
|---|---|---|---|---|
| UI-001 | Startup and exception boundary | W11-C | Shell opens; seeded startup failure shows safe UI without raw crash. | M3 |
| UI-002 | Navigation state | W11-C | Five phases/fifteen steps show current/completed/warning/blocked states correctly. | M3 |
| UI-003 | Project create/open/recent | W11-C | Project persists/reopens; missing recent path offers Locate/Remove. | M3 |
| UI-004 | Accurate Scan deferred state | W11-C | Mode unavailable with Stage 3 explanation; no fake success path. | M3 |
| UI-005 | RTL shell direction | W11-C | Arabic mirrors layout/navigation where appropriate and preserves model-axis semantics. | M3/M12 |
| UI-006 | Mixed Arabic/English identifiers | W11-C | Paths, extensions, IDs, and numbers display without destructive bidi reordering. | M3/M12 |
| UI-007 | Display scaling | W11-C | Critical shell/import/mask/viewer/export remains usable at 100/125/150/200%. | M3/M12 |
| UI-008 | Keyboard/accessibility | W11-C | Critical flow is keyboard reachable with logical focus and accessible names. | M3/M12 |
| UI-009 | GUI heartbeat during fake long job | W11-C | Heartbeat remains responsive within the defined threshold. | M4 |
| UI-010 | Indeterminate progress honesty | W11-C | Stage without numeric progress shows named indeterminate state, not a fake percentage. | M4 |
| UI-011 | Pause capability gating | W11-C | Pause absent/disabled for non-resumable adapter and enabled only for tested capability. | M4 |
| UI-012 | Error layers and copy | W11-C | Summary, action, technical details, and redacted copy match the error. | M4 |
| UI-013 | Translation key parity | U | Required English/Arabic critical keys match; missing translation is reported. | M3/M12 |

## 6. Process Supervisor and Protocol Tests

| ID | Test | Env | Pass criterion | Gate |
|---|---|---|---|---|
| PROC-001 | Argument-vector path safety | W11-C | Spaces, quotes, metacharacters, and Arabic path reach fake worker unchanged without a shell. | M4 |
| PROC-002 | Minimal child environment | W11-C | Seeded unrelated secret/environment value is absent from child. | M4 |
| PROC-003 | Structured numeric progress | W11-C | Events update the correct run/stage and finish at a terminal state. | M4 |
| PROC-004 | Malformed event isolation | W11-C | Malformed event is reported/ignored by policy without corrupting state. | M4 |
| PROC-005 | Cooperative cancellation | W11-C | Worker acknowledges; task becomes Cancelled; output not promoted. | M4 |
| PROC-006 | Forced parent/child termination | WF | Hung worker and child end after grace period; locks release. | M4 |
| PROC-007 | Zero exit plus missing result | W11-C | Task is Failure, never Success. | M4 |
| PROC-008 | Zero exit plus malformed result | W11-C | Task is Failure with protocol error. | M4 |
| PROC-009 | Stale run/stage result | W11-C | Output rejected; prior artifact unchanged. | M4 |
| PROC-010 | Empty artifact | W11-C | Result rejected despite claimed success. | M4 |
| PROC-011 | Retry from restart | W11-C | New IDs/staging and explicit restarted label. | M4 |
| PROC-012 | Checkpoint resume capability | W11-C | Resume offered only for declared, validated checkpoints. | M4/M10 |
| PROC-013 | Restart during worker | WF | Orphan handled by policy; project detects interrupted stage. | M4 |

## 7. Image Import and Quality Tests

| ID | Test | Env | Fixture | Pass criterion | Gate |
|---|---|---|---|---|---|
| IMG-001 | Decode/orientation | U/W11-C | Synthetic JPEG/PNG/WebP orientation cases | Working copy orientation/dimensions expected. | M5 |
| IMG-002 | Corrupt input | U/W11-C | Truncated/malformed files | Stable invalid-image error; UI responsive. | M5 |
| IMG-003 | Oversized/resource-limit input | W11-C | Header/pixel-bomb fixture | Rejected before excessive allocation. | M5 |
| IMG-004 | Original immutability | W11-C | Synthetic image | Source hash/timestamps unchanged. | M5 |
| IMG-005 | Drag/drop mixed selection | W11-C | Supported/unsupported files | Supported import; skipped list contains reasons. | M5 |
| IMG-006 | Exact duplicate | U | Byte-identical files | Grouped as exact duplicate. | M5 |
| IMG-007 | Perceptual near duplicate | U | Resize/compression/crop variants | Expected grouping within documented threshold. | M5 |
| IMG-008 | Similar non-duplicate | U | Different patterns/subjects | Not incorrectly grouped at approved threshold. | M5 |
| IMG-009 | Blur detection | U | Synthetic blur ladder | Metric/classification expected. | M5 |
| IMG-010 | Exposure detection | U | Under/normal/over fixtures | Shadow/highlight metrics/status expected. | M5 |
| IMG-011 | Low resolution | U | Dimension/subject-scale fixtures | Finding includes measurement/threshold. | M5 |
| IMG-012 | Fast AI photo count | U/W11-C | 0, 1, 6, 7 inputs | Only 1–6 permitted. | M5 |
| IMG-013 | View assignment persistence | W11-C | Six synthetic thumbnails | Assignments/source survive restart. | M5 |
| IMG-014 | Primary-image selection | U | Front/45/side/blur/exposure fixtures | Best eligible candidate chosen and explained. | M5 |
| IMG-015 | Manual primary override | W11-C | Imported set | User choice persists; downstream invalidation recorded. | M5 |
| IMG-016 | Image/EXIF log exclusion | W11-C | Seeded EXIF/pixel marker | Logs contain no image bytes, GPS, thumbnail, or sensitive metadata. | M5 |

## 8. Background Removal and Mask Tests

| ID | Test | Env | Pass criterion | Gate |
|---|---|---|---|---|
| MASK-001 | Adapter contract | U | Fake adapter capabilities/results are consistent. | M6 |
| MASK-002 | Model license/hash gate | U/W11-C | Missing license/hash/source/revision blocks installation. | M6 |
| MASK-003 | No silent download | WN | Selecting automatic removal without model causes no network request. | M6 |
| MASK-004 | Model self-test | W11-C | Approved model passes synthetic inference/output constraints. | M6 |
| MASK-005 | CPU inference | W11-C | Mask dimensions/range/lineage match input. | M6 |
| MASK-006 | Inference cancellation | W11-C/WF | No mask promoted; process releases handles. | M6 |
| MASK-007 | Failure fallback | W11-C | Retry/alternate/manual path offered; no blank success. | M6 |
| MASK-008 | Brush determinism | U/W11-C | Same revision/strokes produce same mask hash. | M6 |
| MASK-009 | Undo/redo | W11-C | Pixel/revision state matches history. | M6 |
| MASK-010 | Autosave/restart | WF | Last committed revision reopens after forced close. | M6 |
| MASK-011 | Source integrity | W11-C | Source hash unchanged. | M6 |
| MASK-012 | Arabic path | W11-C | Worker/editor read/write correctly under Arabic path. | M6 |

## 9. Viewer Tests

| ID | Test | Env | Pass criterion | Gate |
|---|---|---|---|---|
| VIEW-001 | Deterministic local bundle | U | Clean build has expected manifest/hash policy and no CDN reference. | M7 |
| VIEW-002 | Network denial | VW/WN | HTTP/HTTPS requests blocked; viewer still functions. | M7 |
| VIEW-003 | Navigation/popup denial | VW | Untrusted links, popups, and downloads are blocked. | M7 |
| VIEW-004 | Bridge schema rejection | VW | Unknown method, field, type, path, or protocol version rejected. | M7 |
| VIEW-005 | Arbitrary local path denial | VW | JavaScript cannot read files outside viewer cache. | M7 |
| VIEW-006 | Synthetic GLB load | VW | Mesh/part/material inventory matches fixture. | M7 |
| VIEW-007 | Arabic source path through cache | VW/W11-C | Model loads while JavaScript sees only generated cache identity. | M7 |
| VIEW-008 | Rotate/zoom/pan/standard views | VW | Camera state changes predictably and reset/fit works. | M7 |
| VIEW-009 | Material/solid/wireframe | VW | Mode state applies without corrupting model. | M7 |
| VIEW-010 | Part visibility/isolation | VW | Scene visibility matches part-tree selection. | M7 |
| VIEW-011 | Screenshot | VW/W11-C | User-triggered image is non-empty and follows background option. | M7 |
| VIEW-012 | Malformed model | VW | Safe load error; renderer remains or becomes usable after recreation. | M7 |
| VIEW-013 | Renderer crash recovery | VW/WF | Viewer recreates without project/artifact loss. | M7 |

## 10. Blender Tests

| ID | Test | Env | Fixture | Pass criterion | Gate |
|---|---|---|---|---|---|
| BLN-001 | Missing Blender | W11-C | No executable | Stable Missing Blender error and Settings action. | M8 |
| BLN-002 | Unsupported Blender | W11-C/BL | Fake/alternate version | Refused before processing with supported-range message. | M8 |
| BLN-003 | Background self-test/protocol | BL | Synthetic request | Valid versioned result and no interactive window. | M8 |
| BLN-004 | Raw backup immutability | BL | Known mesh | Raw hash unchanged; backup reopens. | M8 |
| BLN-005 | Remove disconnected artifacts | BL | Main body plus islands | Main retained; expected islands removed. | M8 |
| BLN-006 | Merge by Distance | BL | Duplicate vertices | Count reduction within tolerance without destructive collapse. | M8 |
| BLN-007 | Recalculate normals | BL | Inverted normals | Expected orientation/metrics. | M8 |
| BLN-008 | Hole analysis/repair | BL | Open boundaries | Eligible holes close; unsafe case reports warning/failure. | M8 |
| BLN-009 | Non-manifold repair | BL | Non-manifold fixture | Count improves or actual failure is reported. | M8 |
| BLN-010 | Conditional voxel remesh | BL | Trigger/non-trigger | Runs only when policy triggers; metrics recorded. | M8 |
| BLN-011 | Conservative decimation | BL | Dense synthetic shape | Target approached; surface-deviation limit respected. | M8 |
| BLN-012 | Base union success | BL | Valid body/base | One expected connected object and build-plate contact. | M8 |
| BLN-013 | Base union failure | BL | Coplanar/self-intersecting | Pre-Boolean checkpoint preserved and useful error/fallback returned. | M8 |
| BLN-014 | Millimeter height | BL | Known box/figure | 40, 100, 250 mm outputs within approved tolerance. | M8 |
| BLN-015 | Z=0 placement | BL | Offset mesh | Minimum Z within tolerance; dimensions preserved except translation. | M8 |
| BLN-016 | Four previews | BL | Processed fixture | Front/back/left/right images non-empty and tied to artifact hash. | M8 |
| BLN-017 | Cancellation | BL/WF | Delayed script | Process ends; staged output not promoted; checkpoint preserved. | M8 |
| BLN-018 | Zero exit invalid artifact | BL | Invalid-output script | Application reports Failure. | M8 |

## 11. Generator and Optional External-API Tests

| ID | Test | Env | Pass criterion | Gate |
|---|---|---|---|---|
| GEN-001 | Capability contract | U | Input, device, texture, progress, cancel, resume, and local/remote flags validate. | M9 |
| GEN-002 | Territory/license block before staging | W11-C/W11-G | Ineligible policy creates no image in engine stage. | M9 |
| GEN-003 | Missing engine | W11-C | Useful installation action; no fake result. | M9 |
| GEN-004 | Integrity mismatch | W11-C/W11-G | Engine quarantined and not executed. | M9 |
| GEN-005 | Protocol mismatch | W11-C/W11-G | Compatible version required; no request sent. | M9 |
| GEN-006 | Insufficient resources | W11-G | Stable error and only tested fallback offered. | M9 |
| GEN-007 | CPU/GPU/Auto semantics | W11-C/W11-G | Unsupported mode disabled; Auto records actual choice. | M9 |
| GEN-008 | Single-primary staging | W11-C/W11-G | Stage contains primary image/mask only; supplementary photos absent. | M9 |
| GEN-009 | Real success | Selected real environment | Current-run non-empty reopenable mesh with plausible bounds/provenance. | M9 |
| GEN-010 | Real failure | Same | Actual Failure; no prior/placeholder mesh promoted. | M9 |
| GEN-011 | Real cancellation | Same | No promoted artifact; actual local/remote cancellation state recorded. | M9 |
| GEN-012 | Stale output | Same | Run/stage mismatch rejected. | M9 |
| GEN-013 | Optional PBR resources | Same | Declared texture/material resources exist, are bounded, and reopen. | M9 |
| GEN-014 | Supplementary reference separation | U/W11-C | Reference report is separate; generator request unchanged. | M9 |
| API-001 | Credential non-disclosure | W11-C | Key absent from project, command line, logs, bundles, and child environment. | If external |
| API-002 | Consent required | W11-C | No network call before matching current consent. | If external |
| API-003 | Failed external API | W11-C | Timeout/HTTP/schema/download failures map to stable errors; no fake success. | If external |
| API-004 | Duplicate-submission safety | W11-C | Retry does not silently duplicate a paid job where provider identity/idempotency exists. | If external |

## 12. Orchestration, Validation, and Export Tests

| ID | Test | Env | Pass criterion | Gate |
|---|---|---|---|---|
| PIPE-001 | Stage invalidation graph | U | Primary/mask/style/dimension changes invalidate only declared descendants. | M10 |
| PIPE-002 | Current-run artifact selection | U/W11-C | UI/pipeline never selects stale prior-run artifact. | M10 |
| PIPE-003 | End-to-end Fast AI success | W11-G/BL/VW or chosen engine environment | Import→quality→mask→generate→raw preview→Blender→processed preview succeeds with lineage. | M10 |
| PIPE-004 | Failure at each process boundary | WF | Image worker, generator, viewer, and Blender failures remain truthful/recoverable. | M10 |
| PIPE-005 | End-to-end cancellation | WF | Cancel at generation/Blender leaves last committed stage and no false success. | M10 |
| PIPE-006 | Restart/recovery | WF | Restart offers correct retry/resume/review action. | M10 |
| VAL-001 | Watertight/topology finding | U/W11-C | Known fixtures yield expected counts/status. | M11 |
| VAL-002 | Disconnected-object count | U/W11-C | Expected object/component count. | M11 |
| VAL-003 | Dimensions/polygons | U/W11-C | Values match fixture within tolerance. | M11 |
| VAL-004 | Build-plate contact | U/W11-C | Contact/offset fixtures classified correctly. | M11 |
| VAL-005 | Three-state derivation | U | Blocking, warning-only, and clean combinations derive Repair/Warning/Ready. | M11 |
| VAL-006 | Qualified readiness wording | W11-C | UI/report says implemented checks passed, not guaranteed physical print. | M11 |
| EXP-001 | STL transactional success | W11-C/BL | Final reopens, is non-empty, has correct dimensions/report/hash. | M11 |
| EXP-002 | GLB transactional success | W11-C/BL | Scene/mesh/material inventory reopens and matches expectations. | M11 |
| EXP-003 | Empty/malformed output | WF | No final success file; staged invalid result and error recorded. | M11 |
| EXP-004 | Permission denied | WF | Clear failure; existing destination preserved. | M11 |
| EXP-005 | Disk full during export | WF | No corrupt final file; cleanup/remaining item reported. | M11 |
| EXP-006 | Existing-file policy | W11-C | Explicit replace/rename required; no silent overwrite. | M11 |
| EXP-007 | Arabic destination | W11-C | STL/GLB export and reopen succeed. | M11 |

## 13. Packaging and Closeout Tests

| ID | Test | Env | Pass criterion | Gate |
|---|---|---|---|---|
| PKG-001 | PyInstaller directory build | W11-C | Build completes from lock; inventory matches plan. | M12 |
| PKG-002 | Clean Windows 11 startup | PKG | Starts without development Python; theme/translations/resources present. | M12 |
| PKG-003 | Clean Windows 10 startup | PKG/W10-C | Declared smoke flow passes or Windows 10 support remains blocked. | M12 |
| PKG-004 | Qt plugin/WebEngine resources | PKG | Viewer loads; required resources present; unneeded modules inventoried. | M12 |
| PKG-005 | Offline package smoke | PKG/WN | Local shell, project, import, viewer, Blender discovery, and export fixtures work. | M12 |
| PKG-006 | Notice/SBOM completeness | U/W11-C | Shipped files map to SBOM and required notice/source material. | M12 |
| PKG-007 | Setup/run reproduction | Clean W11 | Clean tester follows docs successfully; discrepancies fixed. | M12 |
| PKG-008 | Changed-file inventory | U | Report matches version-control diff and generated-file policy. | M12 |
| PKG-009 | No real photos/secrets in package | PKG | Binary/content scan passes. | M12 |

## 14. Original-Specification Tests Deferred to Stage 3

The original specification also requests missing COLMAP, keychain loop, printable color separation, 3MF round trip, complete wall/internal/overhang/support validation, and Accurate Scan tests. They remain tracked but do not satisfy or block the Stage 2 Fast AI MVP unless pulled forward by an approved change.

| ID | Deferred test | Reason |
|---|---|---|
| S3-COL-001 | Missing COLMAP executable | Accurate Scan is Stage 3. |
| S3-COL-002 | Sparse/dense failures and camera coverage | Accurate Scan is Stage 3. |
| S3-BLN-001 | Keychain loop geometry | Advanced printable styles are Stage 3. |
| S3-COLR-001 | Filament color separation and tiny regions | Printable palette is Stage 3. |
| S3-3MF-001 | 3MF write/read/material assignment | 3MF/slicer interoperability is Stage 3. |
| S3-VAL-001 | Minimum wall thickness | Complete printability analysis is Stage 3. |
| S3-VAL-002 | Internal geometry/floating parts | Complete printability analysis is Stage 3. |
| S3-VAL-003 | Overhang/orientation/support estimate | Complete printability analysis is Stage 3. |
| S3-LOC-001 | Complete Arabic translation of advanced screens/help/installer | Full localization is Stage 3. |

## 15. Stage 2 Test Summary Template

| Field | Required value |
|---|---|
| Source revision | Commit hash and dirty/clean state. |
| Core environment | OS, Python, dependency lock hash, Qt/PySide version. |
| Engine environments | Blender, generator, model/runtime/hardware manifests and hashes. |
| Results | Total/Passed/Failed/Skipped/Not Run/Blocked by category. |
| Mandatory failures | Full list with stable error IDs and issue links. |
| Artifacts | Reports, redacted logs, screenshots, previews, validated STL/GLB hashes. |
| Support claims | Windows/GPU/engine combinations supported only by passed evidence. |
| Known limitations | Deferred features, uncertain paths, performance, and translation coverage. |

Stage 2 cannot be approved while a mandatory gate test is Failed, Skipped, Not Run, or Blocked unless the owner explicitly narrows the claimed supported environment and the remaining MVP still includes one real legally usable generator.
