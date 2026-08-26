# MiniFigure 3D Studio — Stage 1 User-Interface Design

**Author:** Manus AI  
**Status:** Proposed for approval  
**Platforms:** Windows 10 and Windows 11 desktop

## 1. Experience Strategy

The interface should feel like a guided professional studio rather than a collection of technical utilities. The application reveals advanced controls when they are relevant, but it never hides failures or replaces technical truth with an ambiguous success screen. Every major action answers four questions: **what is happening, what is being processed, what can the user safely do now, and what happens if the operation fails or is cancelled?**

The visual language uses dark navy surfaces, white or near-white text, and restrained gold accents. Gold identifies current navigation, primary actions, and selected objects; it is not used as the only status signal. Success, warning, error, and information states combine text, iconography, and color.

## 2. Visual Design Tokens

| Token | Proposed value | Use |
|---|---|---|
| Deep navy | `#071522` | Main application background. |
| Navy surface | `#0D2136` | Panels, cards, sidebars, and toolbars. |
| Raised surface | `#14304B` | Selected or elevated content. |
| Primary gold | `#D7AE55` | Current step, primary button, selection outline. |
| Gold hover | `#E5C779` | Hover and keyboard focus emphasis. |
| Main text | `#F6F8FB` | Primary copy. |
| Secondary text | `#B8C4D1` | Descriptions, metadata, and inactive text. |
| Success | `#48B786` | Ready state, always paired with icon/text. |
| Warning | `#E3A63B` | Review required, always paired with icon/text. |
| Error | `#E35D68` | Blocking error and geometry overlay. |
| Information | `#5BA8E6` | Guidance and neutral notices. |

The typography should use a bundled family with high-quality Arabic and Latin coverage, such as verified Noto Sans and Noto Sans Arabic assets. Text sizes should be defined in scalable points rather than fixed pixels, with a minimum comfortable body size and support for Windows display scaling. Exact contrast ratios, keyboard focus visibility, and screen-reader behavior are implementation acceptance tests rather than assumptions.

## 3. Application Shell

The shell uses a persistent title bar and global toolbar, a step navigation rail, a large central workspace, an optional contextual inspector, and a collapsible activity drawer. The central workspace should occupy most of the window because image inspection, mask correction, and 3D review are the product's core tasks.

| Region | Content | Behavior |
|---|---|---|
| Title bar | Product name, current project/model, save state, window controls | Shows “Saving,” “Saved,” or “Recovery needed” without interrupting work. |
| Global toolbar | New/Open Project, Undo/Redo when applicable, language, Help, Settings | Language switch updates layout direction immediately after confirmation if needed. |
| Navigation rail | Grouped workflow steps with completion, warning, and blocked states | Users may revisit completed steps; downstream invalidation is explained before settings are changed. |
| Main workspace | Screen-specific editor or preview | Supports empty, loading, ready, warning, error, and read-only recovery modes. |
| Context inspector | Selected image, part, issue, or setting details | Can collapse to maximize preview area. |
| Activity drawer | Overall progress, stage progress, safe log, controls, technical details | Remains reachable throughout long operations. |
| Status bar | Engine/device, offline/online state, units, cursor/selection context | Never displays secrets or full sensitive paths by default. |

The application supports a practical minimum window size, remembers geometry per user, and degrades by collapsing the inspector and navigation labels rather than shrinking critical controls below usable sizes.

## 4. Navigation Information Architecture

The specified fifteen-step workflow remains visible, but it is grouped into five comprehensible phases. The stepper shows the current step, completed steps, warnings, blocking errors, and steps unavailable for the selected mode.

| Phase | Steps | Purpose |
|---|---|---|
| Project | 1. New Project; 2. Project and Model Name | Establish storage, permission acknowledgment, language, and model identity. |
| Photos | 3. Import; 4. Assign Views; 5. Check Quality; 6. Remove Background; 7. Correct Mask | Produce validated and approved image inputs. |
| Design | 8. Select Style; 9. Dimensions and Printing | Configure appearance and manufacturing intent. |
| Build | 10. Generate; 11. Preview; 12. Repair and Optimize; 13. Separate Printable Colors | Create and refine artifacts. |
| Verify and Deliver | 14. Validate Printability; 15. Export | Review objective findings and write verified output files. |

Mode selection occurs immediately after project creation. **Fast AI Mode** and **Accurate Scan Mode** keep mode-specific photo guidance and processing screens, while later review, repair, color, validation, and export screens reuse shared components.

## 5. Screen 1 — Home and Project Dashboard

The home screen provides **Create New Project**, **Open Existing Project**, and a recent-project grid. Each recent item shows project/model name, last updated time, mode, latest valid artifact status, and a thumbnail generated from the model rather than a person's source photograph unless the user explicitly enables photo thumbnails.

| State | Presentation |
|---|---|
| First launch | Short privacy statement, language choice, dependency check entry point, and one primary Create Project action. |
| Recent project missing | Mark as unavailable; offer Locate or Remove from list, never silently recreate it. |
| Interrupted project | Show Recovery Available with last committed stage and safe recovery options. |
| Engine update required | Non-blocking banner unless the selected workflow depends on the engine. |

## 6. Screens 2–3 — New Project and Mode Selection

New Project requests a project name, model name, storage location, interface language, and acknowledgment that the user has permission to process the photographed person. The storage chooser displays available space and warns about cloud-synced or removable locations without prohibiting them.

The next screen compares the two modes in a table rather than using marketing labels alone.

| Attribute | Fast AI Mode | Accurate Scan Mode |
|---|---|---|
| Photos | 1–6 | 24–80 overlapping images |
| Best for | Rapid miniature creation from limited photos | Detailed reconstruction from a controlled capture set |
| Subject requirement | Clear front or 45-degree primary image | Person must remain still for the full sequence |
| Processing | Local AI where installed/licensed or optional external adapter | Local COLMAP reconstruction followed by Blender |
| Hardware | Selected engine dependent; GPU often required | CPU/GPU and substantial disk/time depending on dense reconstruction |
| Main risk | Unseen geometry may be inferred incorrectly | Motion, blur, weak overlap, reflective backgrounds, and missing angles can cause failure |

Accurate Scan Mode displays capture instructions before import: even diffuse lighting, non-reflective background, consistent camera settings when practical, overlap, complete circular coverage at more than one height, no subject movement, and visible feet/base area when a full-body model is intended. The user can export or print these instructions.

## 7. Screen 4 — Image Import and View Assignment

The import workspace combines a large drag-and-drop area with a thumbnail grid and view slots. Imported images enter an analysis queue immediately, but no generation begins. Each card shows a thumbnail, filename or safe display alias, dimensions, assigned view, quality badge, and selection checkbox.

| Interaction | Behavior |
|---|---|
| Drag and drop | Accept supported image files and folders; show skipped files and reasons. |
| Duplicate detection | Group exact and near duplicates; user chooses which to keep. |
| Assign view | Drag a thumbnail to Front, Back, Left, Right, Front Left, or Front Right; keyboard alternative provided. |
| Automatic suggestion | Show suggested view plus confidence; visually distinguish it from user confirmation. |
| Multi-select | Apply a view label only when semantically valid; Accurate Scan images can enter ordered/unassigned coverage bins. |
| Remove | Remove from project after confirmation when derived work exists; never delete the external original unless explicitly requested. |

Fast AI Mode visually identifies the proposed primary image and explains why it ranks highest. The user can set another primary image. The UI states that the selected engine receives only the inputs declared in its capability panel.

## 8. Screen 5 — Image Quality Report

The quality screen uses a comparison table, filter chips, and a large selected-image preview. It avoids one unexplained score. Each check reports the measurement, status, impact, and recommended correction.

| Finding | Example user message | Action |
|---|---|---|
| Low resolution | “The visible person is only 540 px tall; facial detail may be weak.” | Replace image or continue with warning when mode permits. |
| Blur | “Strong motion or focus blur was detected around the face.” | Choose another primary image or inspect at 100%. |
| Underexposure | “Shadow detail is clipped in clothing and hair.” | Replace image or adjust a working copy non-destructively. |
| Duplicate | “This image is an exact duplicate of Image 07.” | Keep one, keep both with reason, or remove duplicate. |
| Full body missing | “Feet are cut off at the lower frame edge.” | Use Bust style, add another image, or accept warning. |
| Missing angles | “Back-right coverage is missing.” | Add photos or continue with a stated reconstruction risk. |

Filters show All, Blocking, Warnings, Good, Duplicates, and Missing Angles. Accurate Scan Mode includes a circular coverage visualization with a legend distinguishing **estimated coverage before reconstruction** from **measured camera coverage after sparse reconstruction**.

## 9. Screens 6–7 — Background Removal and Mask Correction

Automatic background removal runs as a visible task with the selected model and device shown. Results appear in a checkerboard preview with side-by-side Original, Mask, and Cutout tabs. The user must review the primary mask before generation.

Manual correction presents a centered canvas, a compact left tool strip, and a right inspector. Tools include Add Foreground, Remove Foreground, Edge Refine, Brush Size, Hardness, Feather Preview, Undo, Redo, Fit, and 100% Zoom. A split-view handle supports before/after comparison.

| Safety behavior | Requirement |
|---|---|
| Non-destructive edits | Store revisions and strokes separately from source images. |
| Autosave | Save a mask checkpoint after a short idle period and on step exit. |
| Model replacement | Preserve manual edits where technically compatible or ask before resetting. |
| Failure | If automation fails, allow manual mask creation or a different adapter; do not show an empty transparent image as success. |

## 10. Screen 8 — Style Gallery

Styles appear as large cards with a synthetic or licensed illustration, a concise purpose, and printability implications. Selecting a card opens relevant controls in the inspector.

| Style | Key controls |
|---|---|
| Realistic Full Body | Detail preservation, pose/base connection review. |
| Cartoon | Simplification strength and proportion preset. |
| Chibi Miniature | Head-to-body ratio, hand/foot/accessory strengthening, foot-to-base preference. |
| Bobblehead | Head scale, neck/connector thickness, base style. |
| Bust | Crop height, shoulder width, plinth style. |
| Keychain | Loop placement, hole diameter, reinforcement. |
| Bas-Relief | Relief depth, backing thickness, border shape. |
| Custom Style | Approved parameter combination with reset and save-as-preset. |

The preview labels changes as **planned** until Blender produces a model. The UI must not show a generic concept image as if it were the user's generated result.

## 11. Screen 9 — Dimensions and Printing Options

Settings are organized into General, Shell, Base, Name, Keychain, Color, and Printer Profile sections. A dimension summary remains visible while settings change.

| Control | Default or range | Validation behavior |
|---|---|---|
| Final height | 100 mm; allowed 40–250 mm | Immediate range validation and predicted scale display. |
| Minimum wall thickness | Profile-derived, user editable | Warn when below profile recommendation. |
| Polygon target | Profile/performance-derived | Explain visual versus file-size tradeoff. |
| Solid/Hollow | Solid default unless profile changes it | Hollow requires wall thickness; resin can enable drain holes. |
| Drain holes | Resin-oriented, optional | Diameter, count, and placement review. |
| Base | Circular or square | Diameter/width and thickness preview. |
| Name | Off, raised, or engraved | Text, font, depth/height, placement, and minimum-feature warnings. |
| Keychain | Off/on | Loop placement and hole diameter. |
| Filament colors | 1, 4, 8, or 16 | Separate from texture mode; printer/profile compatibility warning. |

Printer presets populate settings but never lock them. If the user changes a preset value, the screen shows “Modified from Creality K2 with CFS” or equivalent. The profile version is recorded in the project.

## 12. Screen 10 — Generation and Activity Center

Generation begins only after a summary review. The review lists mode, primary image, supplementary-reference role, style, dimensions, engine, device, local versus external processing, and estimated resource requirements. External services add a dedicated consent dialog immediately before transfer.

The Activity Center shows one overall state and expandable stage rows. Each row displays stage name, real numeric progress when available, elapsed time, current safe message, and terminal result. Indeterminate stages show motion and operation name without a fake percentage.

| Control | Availability rule |
|---|---|
| Cancel | Available while queued, preflighting, or running; requests cooperative cancellation then terminates after a safe grace period. |
| Pause | Visible only if the current engine declares verified resumable checkpoints; otherwise disabled with explanation. |
| Retry | Available after a retryable failure and shows whether it resumes a checkpoint or restarts the stage. |
| Copy error | Copies a redacted summary. |
| Technical details | Expands native exit code, engine version, safe command summary, and causal chain. |
| Open log | Opens the simplified redacted log; full diagnostic export requires user review. |

The main application remains usable for safe navigation, but settings that would invalidate an active run are locked or queued until cancellation.

## 13. Screens 11–12 — 3D Preview, Repair, and Optimization

The 3D workspace uses the central viewer, a left scene/part tree, a right properties or issue inspector, and a bottom view toolbar. The viewer defaults to material view and a neutral studio environment bundled locally.

| Viewer control | Interaction |
|---|---|
| Rotate | Primary mouse drag; keyboard alternative. |
| Pan | Middle or modified drag; keyboard alternative. |
| Zoom | Wheel and buttons; reset view. |
| View mode | Material, printable colors, solid, wireframe, issue overlay. |
| Standard views | Front, Back, Left, Right, Perspective, Fit. |
| Parts | Show/hide, isolate, select, rename display label, inspect assigned color. |
| Compare | Synchronized before/after split or toggle. |
| Screenshot | Export current view with optional legend and transparent background. |

The Repair screen first shows objective before metrics, then proposed operations. Automatic repair produces a new artifact and before/after report. The user can accept the result, revert to the backup, or retry with conservative/standard/aggressive presets. Destructive operations never overwrite the only copy.

## 14. Screen 13 — Printable Color Separation

This screen opens with a prominent explanation that **texture colors are visual surface appearance, while filament colors require discrete printable assignments**. The left panel lists semantic parts and color regions; the center shows printable-color mode; the right panel displays palette slots and warnings.

| Action | Result |
|---|---|
| Change slot color | Updates preview and 3MF material color metadata. |
| Reassign part | Moves the selected part/region to another slot. |
| Merge similar colors | Shows a preview, color-distance rationale, and affected parts before applying. |
| Merge tiny regions | Prevents very small floating color objects; thresholds come from the print profile. |
| Split part | Creates a reviewable region operation only where the implementation supports stable geometry. |
| Isolate slot | Displays all meshes or regions assigned to one filament. |

A palette summary reports assigned and unassigned parts, smallest component volume, floating regions, and estimated change count. Export remains blocked when required assignments are missing or the target 3MF semantics are invalid.

## 15. Screen 14 — Printability Report

The report header shows one of three text states: **Ready to Print**, **Ready with Warnings**, or **Repair Required**. Beneath it, a metric grid shows watertight state, non-manifold edges, disconnected objects, dimensions, polygons, wall violations, floating parts, internal geometry, overhangs, build-plate contact, recommended orientation, and support estimate.

Selecting a finding centers the viewer on the associated geometry and highlights it in red. Each finding includes measured value, threshold source, why it matters, recommended correction, and an Auto Repair action only when the action is known and reversible.

The report includes this qualifier:

> “Ready to Print” means that the model passed the checks implemented by this version of MiniFigure 3D Studio for the selected profile. It does not guarantee a successful physical print, slicer settings, material behavior, or printer calibration.

## 16. Screen 15 — Export

The export screen presents Texture Exports and Printable Exports as separate groups. Users choose formats, destination, naming pattern, whether to include reports and previews, and whether to retain intermediate artifacts.

| Export group | Formats | Guardrails |
|---|---|---|
| Printable single color | STL | Warn that STL does not carry printable color assignments and record intended millimeter dimensions in the report. |
| Printable multi-color | 3MF | Require valid parts/material slots and compatibility validation. |
| Editable/visual | GLB, OBJ/MTL/textures, BLEND | Preserve materials where supported; verify referenced resources. |

The export progress panel distinguishes Writing, Reopening, Geometry Validation, Material/Part Validation, and Finalizing. The success screen lists exact output files, sizes, hashes when requested, and validation result. A file that was written but failed to reopen is shown as failed, not successful.

## 17. Settings and Dependency Center

Settings use sections for General, Language, Storage, Privacy, Engines, External Providers, Viewer, Diagnostics, and About/Third-Party Software.

| Section | Key behavior |
|---|---|
| Engines | Detect Blender and COLMAP, show supported range, run self-test, install optional package where approved, and display license/source. |
| AI engines | Show adapter capabilities, model revision, license status, territory availability, disk size, VRAM guidance, and uninstall action. |
| External providers | Configure endpoint/adapter, import `.env`, move a key to Windows secure storage, test without exposing the key, and remove credentials. |
| Privacy | Default local processing, metadata stripping, log retention, original-image retention, and network permission history. |
| Diagnostics | Redacted logs, engine manifests, system summary, and previewable diagnostic bundle. |
| Third-party software | Searchable notices and source/offer instructions for distributed dependencies. |

## 18. Error Presentation Pattern

Errors appear in three layers. The inline layer identifies the failing field or stage. A concise panel explains the problem and offers the next action. An expandable technical section provides details for advanced users and support without exposing secrets.

| Layer | Example |
|---|---|
| Human summary | “COLMAP could register only 9 of 42 images, so dense reconstruction cannot continue.” |
| Corrective guidance | “Retake blurred views, add overlapping photos around the back-right side, keep the person still, then retry from Feature Extraction.” |
| Technical details | Error code, COLMAP version, stage, exit code, registered-image count, sanitized stderr excerpt, checkpoint path alias. |

Retry is not shown for license blocks, missing consent, or settings that must change. For Boolean or mesh-repair failures, the error panel may offer an alternative strategy while retaining the pre-operation artifact.

## 19. RTL/LTR Behavior

Switching to Arabic changes window and text direction, navigation order, panel anchoring, alignment, and directional icons whose meaning is reading-order dependent. It does not invert model axes, orbit direction, front/back/left/right semantics, undo/redo history, media playback, file extensions, or signed numeric data.

Long Arabic translations must be tested at 100%, 125%, 150%, and 200% display scaling. Mixed Arabic/English strings should isolate technical identifiers and paths using appropriate bidirectional handling. Error-copy and report exports use UTF-8 and preserve Arabic project/model names.

## 20. Accessibility and Input

Every control requires a keyboard path and accessible name. Tooltips supplement but do not replace labels. Focus order follows the active layout direction where appropriate. Progress updates should be announced at meaningful stage boundaries rather than every numeric tick. Motion is restrained and respects reduced-motion preferences where accessible through Qt or application settings.

A high-contrast mode may be implemented after the base theme, but the initial theme must already avoid color-only meaning. Touch is not a primary target, yet hit targets should remain large enough for high-DPI desktop use.

## 21. UI Acceptance Criteria

The proposed UI is ready for implementation approval when the owner accepts the grouped fifteen-step workflow, large preview-first layouts, mode comparison and capture guidance, honest primary-image wording, non-destructive mask editor, style and print controls, real progress semantics, capability-gated Pause, redacted error copy, issue-linked 3D viewer, separated texture/filament workflows, transactional export feedback, Arabic/English direction rules, and dependency/privacy settings.

The first interactive prototype should validate four high-risk flows before visual polish: Fast AI image selection through generation summary; Accurate Scan capture/import through preflight; mask correction with Arabic paths; and repair/validation/export using synthetic meshes.
