# MiniFigure 3D Studio — Stage 1 Risk Register

**Author:** Manus AI  
**Status:** Proposed for approval  
**Scoring:** Likelihood and impact use Low, Medium, High, or Critical. Priority reflects combined exposure and release consequences.

## 1. Risk Governance

A risk is closed only when evidence shows that the mitigation works in the intended Windows environment and distribution model. Documentation or a planned task does not by itself close a risk. Critical legal, privacy, or integrity risks block release rather than becoming generic warnings.

| Priority | Interpretation | Required response |
|---|---|---|
| Critical | Product cannot lawfully, safely, or truthfully ship as planned | Resolve before implementation dependence or public distribution. |
| High | Likely to break a principal workflow or create severe support burden | Run an early spike and define a tested fallback. |
| Medium | Material but containable with architecture and validation | Track to the relevant stage gate with acceptance evidence. |
| Low | Limited consequence or straightforward workaround | Monitor and include in regression coverage. |

## 2. Risk Register

| ID | Risk | Likelihood | Impact | Priority | Mitigation and contingency | Gate owner |
|---|---|---:|---:|---|---|---|
| R-01 | Hunyuan3D 2.1 community license excludes the EU, UK, and South Korea, preventing universal default distribution/use under the reviewed terms.[1] | High | Critical | **Critical** | Make Hunyuan an optional territory/license-gated package; obtain qualified legal review; secure separate rights or implement a compliant alternative local adapter before worldwide claims. Block before image staging when eligibility is absent. | Product owner and legal/compliance review before Stage 2 engine selection. |
| R-02 | Background-removal software license is mistaken for model-weight rights; the current rembg documentation warns its default BRIA model needs paid commercial terms.[2] | High | High | **Critical** | Approve software and weights separately; benchmark candidate portrait models; pin model/revision/hash/license; prohibit silent first-use downloads and library-default model selection. | Stage 2 WP2.4 entry gate. |
| R-03 | Hunyuan's documented resource demand exceeds many consumer GPUs: about 10 GB shape, 21 GB texture, and 29 GB combined in its stated setup.[3] | High | High | **High** | Preflight VRAM and CUDA stack; separate geometry and texture stages; expose supported low-memory mode; do not promise CPU fallback until benchmarked; offer other adapters. | Stage 2 WP2.6. |
| R-04 | Hunyuan upstream tested Python 3.10/PyTorch/CUDA stack conflicts with the required Python 3.11 desktop runtime.[3] | High | High | **High** | Isolate the engine in a separate environment and process with a versioned protocol; never import it into the GUI. Run clean Windows installation and self-test spikes. | Stage 2 WP2.6. |
| R-05 | One-view generation invents hidden geometry and may produce incorrect clothing, hair, or anatomy. | High | High | **High** | Honest primary-image wording; use other images only for separately implemented reference review unless the adapter supports multi-image; preserve raw result; require 3D review; allow alternative adapters or Accurate Scan. | Product and UX acceptance in Stage 2. |
| R-06 | Accurate Scan of a living person fails because the person moves between 24–80 photos. | High | High | **High** | Strong capture instructions, rapid capture recommendation, blur/duplicate/coverage preflight, actual COLMAP failure reporting, and no placeholder success. Consider future synchronized multi-camera support as a separate product. | Stage 3 WP3.1–WP3.3. |
| R-07 | COLMAP reconstruction fails from weak texture, reflective surfaces, repeated patterns, background changes, insufficient overlap, or missing angles. | High | High | **High** | Stage-by-stage CLI checkpoints; registration/match metrics; estimated then reconstructed coverage; corrective guidance; preserve sparse result; selectable matching strategy validated on synthetic/licensed sets. | Stage 3 WP3.2–WP3.3. |
| R-08 | A specific COLMAP Windows build carries third-party obligations or GPU capabilities different from the headline BSD license.[4] | Medium | High | **High** | Pin binary provenance; generate dependency and notice inventory; run CPU/GPU self-test; do not describe unsupported CUDA/HIP/CPU paths. | Pre-Stage 3 dependency gate. |
| R-09 | Blender automation scripts using Blender's Python API have GPL-compatible distribution obligations.[5] | High | High | **Critical** | Keep scripts in a separate GPL-compatible source component, ship source and notices, record modifications, and obtain release compliance review. | Pre-Stage 2 repository/license decision. |
| R-10 | Blender modifiers, booleans, remesh, and decimation damage facial details or create new defects. | High | High | **High** | Immutable backups; conservative defaults; conditional operations; face-region protection; surface-deviation metrics; before/after viewer; fallback strategies; block automatic acceptance above thresholds. | Stage 2 WP2.8 and Stage 3 advanced styles. |
| R-11 | Boolean union fails on self-intersections, coplanar surfaces, or invalid raw meshes. | High | Medium | **High** | Precondition validation, repair before union, bounded solver alternatives, preserve pre-Boolean artifact, report actual failure, permit review/manual Blender export. | Stage 2 WP2.8. |
| R-12 | Thin-feature strengthening incorrectly thickens face, hair, clothing, or accessories. | Medium | High | **High** | Use semantic/manual protected regions, profile-relative thresholds, localized preview, and accept/revert workflow. Do not claim automatic semantic certainty. | Stage 3 WP3.4. |
| R-13 | Printability validator produces false confidence; “Ready to Print” is interpreted as a physical-print guarantee. | High | High | **Critical** | Define state as passing declared checks only; disclose approximations; show metrics and profile thresholds; maintain blockers/warnings; validate against synthetic truth fixtures and sample prints. | Stage 3 WP3.5 and release UX review. |
| R-14 | Minimum wall thickness, internal geometry, and support estimates are computationally expensive or approximate. | High | Medium | **High** | Provide bounded-resolution analysis, progress/cancel, uncertainty labels, printer-profile thresholds, and qualitative support estimates rather than exact slicer predictions. | Stage 3 WP3.5. |
| R-15 | 3MF is standards-valid but parts/material assignments are not recognized as intended by Orca Slicer or Creality Print. | High | High | **High** | Use lib3mf and the Materials/Properties extension; write-read validation; fixture matrix for 1/4/8/16 colors; test exact slicer versions; record known differences.[6] [7] | Stage 3 WP3.7. |
| R-16 | Texture clustering creates tiny floating color objects or impractical color changes. | High | Medium | **High** | Domain-level printable parts and palette slots; minimum region area/volume; merge similar/tiny regions; manual review; block unassigned parts. | Stage 3 WP3.6. |
| R-17 | Qt/PySide6 open-source packaging fails LGPL obligations or Qt WebEngine/Chromium notices are incomplete.[8] [9] | Medium | Critical | **Critical** | Dynamic linking, replaceable Qt DLLs, notices and license texts, corresponding-source or offer path, module allowlist, Chromium notice bundle, legal review; use commercial Qt if obligations cannot be met. | Pre-release installer gate. |
| R-18 | Core installer becomes too large or fragile when AI weights, Blender, COLMAP, Qt WebEngine, and CUDA assets are combined. | High | High | **High** | Core installer plus optional signed engine/model packages; resumable downloads; disk preflight; rollback; discovery of separately installed tools; no one-file monolith. | Stage 3 WP3.10. |
| R-19 | PyInstaller succeeds on a developer machine but misses Qt plugins, WebEngine resources, native DLLs, or Windows runtime components. | High | High | **High** | Native Windows CI, deterministic spec, dependency inventory, clean VM tests on Windows 10/11, signed artifacts, upgrade/uninstall tests. | Stage 3 WP3.10. |
| R-20 | GUI freezes during native, GPU, image, or filesystem work. | Medium | High | **High** | Enforce no blocking work on GUI thread; process/worker boundaries; UI heartbeat test around every adapter; bounded file operations and preview generation. | Every Stage 2 vertical slice. |
| R-21 | Cancellation leaves child processes, GPU allocations, locked files, or half-committed artifacts. | High | High | **High** | Cooperative token, grace period, process-tree termination, staging-only writes, atomic commit, startup orphan cleanup, cancellation fault tests. | Stage 2 WP2.5. |
| R-22 | “Pause” is displayed for engines without a resumable state and misleads users. | Medium | Medium | **Medium** | Capability-gated control; show Pause only for verified checkpoints; otherwise explain that cancellation and later retry are available. | Stage 2 WP2.5 and UI tests. |
| R-23 | Arabic, spaces, long paths, quotes, or bidirectional text break command invocation and exports. | High | High | **High** | Generated internal filenames, Unicode argument vectors, no shell strings, UTF-8 JSON/logs, Arabic-path test matrix across all external processes. | Stage 2 and Stage 3 continuous gate. |
| R-24 | External API key leaks through `.env`, process environment, logs, crash dumps, or diagnostic bundles. | Medium | Critical | **Critical** | Credential Manager/DPAPI preferred; `.env` user-local and access-restricted; minimal child environment; no command-line key; redaction; seeded-secret scans; bundle preview.[10] [11] | Stage 2 provider/diagnostics gate. |
| R-25 | An external adapter sends photos without sufficiently specific consent or sends more metadata than needed. | Medium | Critical | **Critical** | Local default; named provider and purpose; exact transfer preview; EXIF stripping; consent record tied to adapter/policy version; network tests that fail without consent. | Before any external adapter is enabled. |
| R-26 | A dependency silently downloads weights or sends analytics, violating offline/privacy expectations. | Medium | High | **High** | Network-deny tests, explicit engine manager, request interception, disable automatic downloads, approved outbound domain allowlist only during confirmed operation. | Stage 2 model and release gates. |
| R-27 | Qt WebEngine viewer loads remote content or untrusted model metadata triggers script/content injection. | Medium | High | **High** | Bundle Three.js locally; restrictive CSP; deny navigation/remote requests; schema-validate WebChannel; escape metadata; disable popups/downloads/devtools in release. | Stage 2 WP2.7 security tests. |
| R-28 | Malformed or oversized images/models cause native crash, memory exhaustion, ZIP expansion, or parser abuse. | Medium | High | **High** | Worker isolation, file/mesh/texture limits, safe archive extraction, staging quotas, pinned libraries, independent reopen, resource monitoring. | Stage 2/3 input and export gates. |
| R-29 | Project deletion follows a junction/symlink outside the project or claims secure deletion that cannot be guaranteed on SSD/sync/backups. | Medium | Critical | **Critical** | Canonical root enforcement; do not follow unexpected reparse points; inventory and report failures; label enhanced cleanup best-effort; recommend encryption/device sanitization for stronger needs.[12] | Stage 2 project/deletion gate. |
| R-30 | Logs or recent-project thumbnails reveal sensitive images or personal paths. | Medium | High | **High** | Model-render thumbnails by default; project-relative IDs; no images/masks/textures in logs; bounded local retention; clear history action. | Stage 2 privacy tests. |
| R-31 | Export file is created but contains empty, invalid, wrong-unit, or stale geometry. | Medium | Critical | **Critical** | Run-ID provenance, write to staging, reopen independently, verify non-empty geometry/dimensions/parts/materials, hash, atomic finalize; zero exit alone never succeeds. | Stage 2 WP2.9 and Stage 3 exports. |
| R-32 | Model or engine update changes output or protocol and breaks old projects. | High | Medium | **High** | Pin exact versions, versioned protocol and project schema, capability negotiation, migration tests, preserve old engine manifest, explicit reprocess action. | Engine manager and release gates. |
| R-33 | Supply-chain package or asset is replaced or compromised. | Medium | Critical | **Critical** | Signed installer/manifests, hashes, pinned sources, SBOM, vulnerability scans, download staging, rollback, no execution before self-test. | Every release and engine-package publication. |
| R-34 | Real-person test images enter source control or CI artifacts. | Low | Critical | **High** | Synthetic/licensed-only repository policy, asset manifest, pre-commit/CI scans for unexpected binaries and EXIF, artifact retention controls. | Continuous integration gate. |
| R-35 | Bas-relief, bobblehead, keychain, hollowing, or drain-hole features are presented before physical and geometric validation. | Medium | High | **High** | Feature flags by maturity; synthetic geometry and physical-print acceptance criteria; clearly mark unsupported operations until validated. | Stage 3 WP3.4. |
| R-36 | The project scope expands across all advanced features before the MVP is stable. | High | High | **High** | Enforce Stage 2 definition of done and approval stop; defer Accurate Scan, full color, 3MF, complete report, localization completion, and installer to Stage 3. | Product owner at every stage boundary. |

## 3. Critical Blockers for Approval

The architecture can be approved with open implementation risks, but the owner should explicitly acknowledge four blockers before Stage 2 begins: **Hunyuan territorial availability, the background model's commercial rights, the Qt/Blender licensing strategy, and the distinction between validator readiness and guaranteed print success**.

| Blocker | Approval question |
|---|---|
| Hunyuan | Is distribution limited to licensed territories, will separate rights be obtained, or must a different local default be selected? |
| Background removal | Which model weights are approved for local commercial redistribution and portrait use? |
| Qt/Blender | Will the release follow dynamic LGPL plus separate GPL-compatible Blender scripts, or use commercial/alternative terms where applicable? |
| Print claims | Is the owner willing to use the qualified “passes declared checks” wording and avoid a physical-print guarantee? |

## 4. Risk Review Cadence

The register should be reviewed at every milestone exit, after any dependency/model update, after a new provider is added, and before installer publication. Closed risks retain links to evidence. New risks receive an owner and testable mitigation before the related feature is merged.

## References

[1]: https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2.1/main/LICENSE "Tencent Hunyuan 3D 2.1 Community License"
[2]: https://github.com/danielgatis/rembg "rembg Repository and Model-License Warning"
[3]: https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1 "Tencent Hunyuan3D 2.1 Repository"
[4]: https://github.com/colmap/colmap "COLMAP Repository"
[5]: https://www.blender.org/about/license/ "Blender License"
[6]: https://3mf.io/spec/ "3MF Specification Suite"
[7]: https://github.com/3MFConsortium/lib3mf "lib3mf Repository"
[8]: https://www.qt.io/development/open-source-lgpl-obligations "Qt GPL and LGPL Obligations"
[9]: https://doc.qt.io/qt-6/qtwebengine-licensing.html "Qt WebEngine Licensing"
[10]: https://learn.microsoft.com/en-us/windows/win32/secbp/handling-passwords "Microsoft: Handling Passwords"
[11]: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html "OWASP Logging Cheat Sheet"
[12]: https://csrc.nist.gov/pubs/sp/800/88/r2/final "NIST SP 800-88 Rev. 2: Guidelines for Media Sanitization"
