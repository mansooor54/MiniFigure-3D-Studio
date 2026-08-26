# MiniFigure 3D Studio — Proposed Project Structure

**Author:** Manus AI  
**Status:** Stage 1 proposal; directories and files are planning artifacts, not implemented source code.

## 1. Structural Principles

The repository separates the Python 3.11 desktop shell from Blender API scripts, Hunyuan/COLMAP engine integrations, the offline Three.js viewer, test fixtures, and packaging material. The application layer depends on typed ports, while adapters depend on third-party libraries and external executables. User data, downloaded weights, Blender, and COLMAP binaries do not live in the source tree.

The structure intentionally creates more focused files than the example specification. It preserves the requested top-level areas—`app`, `blender_scripts`, `generators`, `tests`, `assets`, and `docs`—while adding explicit protocol, privacy, packaging, viewer, and compliance boundaries.

## 2. Proposed Repository Tree

```text
mini_figure_studio/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── bootstrap.py
│   ├── application_info.py
│   ├── composition_root.py
│   ├── ui/
│   │   ├── main_window.py
│   │   ├── navigation_model.py
│   │   ├── theme.py
│   │   ├── resources.qrc
│   │   ├── pages/
│   │   │   ├── home_page.py
│   │   │   ├── new_project_page.py
│   │   │   ├── mode_selection_page.py
│   │   │   ├── image_import_page.py
│   │   │   ├── view_assignment_page.py
│   │   │   ├── quality_report_page.py
│   │   │   ├── background_removal_page.py
│   │   │   ├── mask_editor_page.py
│   │   │   ├── style_selection_page.py
│   │   │   ├── print_settings_page.py
│   │   │   ├── generation_page.py
│   │   │   ├── model_preview_page.py
│   │   │   ├── repair_page.py
│   │   │   ├── color_separation_page.py
│   │   │   ├── printability_page.py
│   │   │   └── export_page.py
│   │   ├── dialogs/
│   │   │   ├── external_consent_dialog.py
│   │   │   ├── dependency_settings_dialog.py
│   │   │   ├── error_details_dialog.py
│   │   │   ├── delete_project_dialog.py
│   │   │   ├── diagnostic_bundle_dialog.py
│   │   │   └── about_licenses_dialog.py
│   │   └── widgets/
│   │       ├── activity_drawer.py
│   │       ├── progress_stage_row.py
│   │       ├── image_thumbnail_card.py
│   │       ├── image_drop_zone.py
│   │       ├── view_slot.py
│   │       ├── mask_canvas.py
│   │       ├── style_card.py
│   │       ├── dimension_summary.py
│   │       ├── finding_card.py
│   │       ├── palette_editor.py
│   │       ├── part_tree.py
│   │       └── collapsible_error_panel.py
│   ├── controllers/
│   │   ├── application_controller.py
│   │   ├── project_controller.py
│   │   ├── image_controller.py
│   │   ├── mask_controller.py
│   │   ├── generation_controller.py
│   │   ├── processing_controller.py
│   │   ├── color_controller.py
│   │   ├── validation_controller.py
│   │   ├── export_controller.py
│   │   ├── viewer_controller.py
│   │   └── settings_controller.py
│   ├── application/
│   │   ├── commands/
│   │   │   ├── create_project.py
│   │   │   ├── import_images.py
│   │   │   ├── analyze_images.py
│   │   │   ├── generate_mask.py
│   │   │   ├── save_mask_revision.py
│   │   │   ├── start_generation.py
│   │   │   ├── run_mesh_pipeline.py
│   │   │   ├── validate_model.py
│   │   │   ├── export_model.py
│   │   │   └── delete_project.py
│   │   ├── queries/
│   │   │   ├── load_project_summary.py
│   │   │   ├── list_engine_capabilities.py
│   │   │   ├── build_quality_report.py
│   │   │   ├── build_printability_report.py
│   │   │   └── list_export_options.py
│   │   └── orchestration/
│   │       ├── pipeline_orchestrator.py
│   │       ├── fast_ai_pipeline.py
│   │       ├── accurate_scan_pipeline.py
│   │       ├── blender_pipeline.py
│   │       ├── export_pipeline.py
│   │       ├── stage_definition.py
│   │       ├── stage_cache.py
│   │       └── recovery_coordinator.py
│   ├── models/
│   │   ├── project.py
│   │   ├── source_image.py
│   │   ├── view_assignment.py
│   │   ├── quality_finding.py
│   │   ├── mask_revision.py
│   │   ├── generation_request.py
│   │   ├── generator_capabilities.py
│   │   ├── print_profile.py
│   │   ├── figure_style.py
│   │   ├── mesh_artifact.py
│   │   ├── surface_appearance.py
│   │   ├── printable_palette.py
│   │   ├── validation_finding.py
│   │   ├── validation_report.py
│   │   ├── pipeline_run.py
│   │   ├── stage_result.py
│   │   ├── consent_record.py
│   │   ├── engine_manifest.py
│   │   └── error_info.py
│   ├── ports/
│   │   ├── generator.py
│   │   ├── background_remover.py
│   │   ├── image_quality_analyzer.py
│   │   ├── view_estimator.py
│   │   ├── mesh_processor.py
│   │   ├── printability_validator.py
│   │   ├── color_separator.py
│   │   ├── model_exporter.py
│   │   ├── project_repository.py
│   │   ├── secret_store.py
│   │   ├── process_runner.py
│   │   ├── viewer_bridge.py
│   │   └── clock.py
│   ├── services/
│   │   ├── project_service.py
│   │   ├── artifact_service.py
│   │   ├── image_import_service.py
│   │   ├── image_quality_service.py
│   │   ├── primary_image_selector.py
│   │   ├── reference_color_service.py
│   │   ├── mask_service.py
│   │   ├── device_capability_service.py
│   │   ├── engine_registry.py
│   │   ├── engine_installation_service.py
│   │   ├── print_profile_service.py
│   │   ├── style_service.py
│   │   ├── dimension_service.py
│   │   ├── consent_service.py
│   │   ├── secure_deletion_service.py
│   │   ├── diagnostic_bundle_service.py
│   │   └── localization_service.py
│   ├── workers/
│   │   ├── process_supervisor.py
│   │   ├── process_tree.py
│   │   ├── image_worker.py
│   │   ├── task_state_machine.py
│   │   ├── progress_event.py
│   │   ├── cancellation_token.py
│   │   ├── checkpoint_manager.py
│   │   └── worker_protocol.py
│   ├── adapters/
│   │   ├── filesystem/
│   │   │   ├── local_project_repository.py
│   │   │   ├── atomic_file_writer.py
│   │   │   ├── artifact_hasher.py
│   │   │   ├── safe_paths.py
│   │   │   └── reparse_point_guard.py
│   │   ├── imaging/
│   │   │   ├── pillow_decoder.py
│   │   │   ├── opencv_quality_analyzer.py
│   │   │   ├── perceptual_duplicate_detector.py
│   │   │   ├── onnx_background_remover.py
│   │   │   └── manual_mask_renderer.py
│   │   ├── processes/
│   │   │   ├── qt_process_runner.py
│   │   │   ├── blender_cli_adapter.py
│   │   │   ├── colmap_cli_adapter.py
│   │   │   └── engine_result_reader.py
│   │   ├── security/
│   │   │   ├── windows_credential_store.py
│   │   │   ├── dpapi_secret_store.py
│   │   │   ├── dotenv_secret_source.py
│   │   │   ├── log_redactor.py
│   │   │   └── consent_repository.py
│   │   └── viewer/
│   │       ├── webengine_viewer.py
│   │       ├── viewer_request_interceptor.py
│   │       ├── webchannel_gateway.py
│   │       └── viewer_cache.py
│   ├── validators/
│   │   ├── image_input_validator.py
│   │   ├── project_validator.py
│   │   ├── engine_manifest_validator.py
│   │   ├── artifact_validator.py
│   │   ├── mesh_topology_validator.py
│   │   ├── dimension_validator.py
│   │   ├── wall_thickness_validator.py
│   │   ├── floating_part_validator.py
│   │   ├── internal_geometry_validator.py
│   │   ├── overhang_validator.py
│   │   ├── build_plate_validator.py
│   │   ├── palette_validator.py
│   │   └── export_result_validator.py
│   ├── exporters/
│   │   ├── export_manager.py
│   │   ├── transactional_exporter.py
│   │   ├── stl_exporter.py
│   │   ├── glb_exporter.py
│   │   ├── obj_exporter.py
│   │   ├── blend_exporter.py
│   │   ├── three_mf_exporter.py
│   │   └── export_report_writer.py
│   ├── logging/
│   │   ├── configure_logging.py
│   │   ├── event_ids.py
│   │   ├── redaction_policy.py
│   │   └── bounded_log_store.py
│   ├── localization/
│   │   ├── translator.py
│   │   ├── locale_format.py
│   │   ├── bidi_helpers.py
│   │   ├── en_US.ts
│   │   ├── ar.ts
│   │   ├── en_US.qm
│   │   └── ar.qm
│   ├── config/
│   │   ├── settings.py
│   │   ├── paths.py
│   │   ├── constants.py
│   │   ├── schemas/
│   │   │   ├── project.schema.json
│   │   │   ├── engine_manifest.schema.json
│   │   │   ├── worker_request.schema.json
│   │   │   ├── worker_result.schema.json
│   │   │   └── validation_report.schema.json
│   │   └── presets/
│   │       ├── creality_k2_cfs.yaml
│   │       ├── orca_slicer.yaml
│   │       ├── creality_print.yaml
│   │       ├── generic_fdm.yaml
│   │       └── resin_printer.yaml
│   └── migrations/
│       ├── project_v1_to_v2.py
│       └── migration_registry.py
├── generators/
│   ├── __init__.py
│   ├── base_generator.py
│   ├── hunyuan_generator.py
│   ├── external_api_generator.py
│   ├── tripo_generator.py
│   ├── meshy_generator.py
│   ├── photogrammetry_generator.py
│   ├── hunyuan_worker_entry.py
│   ├── provider_http_client.py
│   └── provider_response_validator.py
├── blender_scripts/
│   ├── README.md
│   ├── LICENSE
│   ├── pipeline_runner.py
│   ├── protocol.py
│   ├── scene_io.py
│   ├── geometry_metrics.py
│   ├── cleanup_mesh.py
│   ├── repair_non_manifold.py
│   ├── voxel_remesh.py
│   ├── decimate_mesh.py
│   ├── protect_face_region.py
│   ├── strengthen_fragile_parts.py
│   ├── add_base.py
│   ├── add_name.py
│   ├── add_keychain_loop.py
│   ├── hollow_model.py
│   ├── add_drain_holes.py
│   ├── split_colors.py
│   ├── validate_printability.py
│   ├── render_previews.py
│   ├── export_models.py
│   └── operations/
│       ├── connected_components.py
│       ├── merge_by_distance.py
│       ├── normals.py
│       ├── holes.py
│       ├── boolean_union.py
│       ├── internal_geometry.py
│       ├── unit_scale.py
│       └── build_plate.py
├── viewer/
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── src/
│   │   ├── main.ts
│   │   ├── scene_controller.ts
│   │   ├── model_loader.ts
│   │   ├── camera_controller.ts
│   │   ├── view_modes.ts
│   │   ├── part_tree.ts
│   │   ├── issue_overlay.ts
│   │   ├── comparison_view.ts
│   │   ├── screenshot.ts
│   │   ├── webchannel.ts
│   │   └── styles.css
│   └── tests/
│       ├── protocol.test.ts
│       ├── issue_overlay.test.ts
│       └── network_denial.test.ts
├── assets/
│   ├── icons/
│   ├── fonts/
│   ├── style_previews/
│   ├── capture_guides/
│   ├── viewer/
│   │   └── dist/
│   ├── licenses/
│   └── asset_manifest.yaml
├── tests/
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_blur_detection.py
│   │   ├── test_exposure_detection.py
│   │   ├── test_duplicate_detection.py
│   │   ├── test_dimension_calculations.py
│   │   ├── test_millimeter_conversion.py
│   │   ├── test_primary_image_selector.py
│   │   ├── test_task_state_machine.py
│   │   ├── test_log_redaction.py
│   │   ├── test_palette_rules.py
│   │   └── test_project_migrations.py
│   ├── contract/
│   │   ├── test_generator_contract.py
│   │   ├── test_background_remover_contract.py
│   │   ├── test_worker_protocol.py
│   │   ├── test_blender_result_contract.py
│   │   ├── test_colmap_result_contract.py
│   │   └── test_exporter_contract.py
│   ├── integration/
│   │   ├── test_arabic_paths.py
│   │   ├── test_task_cancellation.py
│   │   ├── test_interrupted_recovery.py
│   │   ├── test_missing_blender.py
│   │   ├── test_missing_colmap.py
│   │   ├── test_failed_external_api.py
│   │   ├── test_blender_cleanup.py
│   │   ├── test_base_creation.py
│   │   ├── test_keychain_loop.py
│   │   ├── test_color_separation.py
│   │   ├── test_export_validation.py
│   │   └── test_three_mf_round_trip.py
│   ├── ui/
│   │   ├── test_navigation.py
│   │   ├── test_drag_drop.py
│   │   ├── test_progress_controls.py
│   │   ├── test_error_details.py
│   │   ├── test_mask_editor.py
│   │   └── test_rtl_layout.py
│   ├── e2e/
│   │   ├── test_fast_ai_workflow.py
│   │   ├── test_accurate_scan_workflow.py
│   │   └── test_windows_packaged_app.py
│   ├── blender/
│   │   ├── test_remove_disconnected.py
│   │   ├── test_manifold_validation.py
│   │   ├── test_face_preservation.py
│   │   └── test_preview_rendering.py
│   └── fixtures/
│       ├── images/
│       ├── meshes/
│       ├── colmap/
│       ├── exports/
│       ├── fake_engines/
│       └── asset_manifest.yaml
├── packaging/
│   ├── pyinstaller/
│   │   ├── MiniFigure3DStudio.spec
│   │   ├── runtime_hook.py
│   │   └── hooks/
│   ├── installer/
│   │   ├── installer_definition.iss
│   │   ├── installer_strings_en.isl
│   │   └── installer_strings_ar.isl
│   ├── engine_manifests/
│   │   ├── background_model.template.json
│   │   ├── hunyuan.template.json
│   │   ├── blender.template.json
│   │   └── colmap.template.json
│   ├── licenses/
│   ├── source_offer/
│   └── windows/
│       ├── build.ps1
│       ├── sign.ps1
│       ├── smoke_test.ps1
│       └── clean_vm_test.md
├── scripts/
│   ├── build_viewer.py
│   ├── compile_translations.py
│   ├── generate_sbom.py
│   ├── collect_licenses.py
│   ├── validate_assets.py
│   ├── validate_engine_manifest.py
│   └── create_synthetic_fixtures.py
├── docs/
│   ├── architecture.md
│   ├── data_flow.md
│   ├── ui_design.md
│   ├── security_privacy.md
│   ├── dependency_licenses.md
│   ├── implementation_roadmap.md
│   ├── risk_register.md
│   ├── testing_strategy.md
│   ├── engine_protocol.md
│   ├── project_format.md
│   ├── export_compatibility.md
│   ├── troubleshooting_en.md
│   └── troubleshooting_ar.md
├── licenses/
│   ├── THIRD_PARTY_NOTICES.md
│   ├── qt/
│   ├── chromium/
│   ├── blender/
│   ├── colmap/
│   ├── models/
│   ├── fonts/
│   └── python/
├── .github/
│   └── workflows/
│       ├── quality.yml
│       ├── windows-build.yml
│       ├── blender-integration.yml
│       ├── security.yml
│       └── release.yml
├── .env.example
├── .gitignore
├── .gitattributes
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── requirements-lock.txt
├── README_EN.md
├── README_AR.md
├── SECURITY.md
├── PRIVACY.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── LICENSE
└── THIRD_PARTY_NOTICES.md
```

## 3. Responsibility Boundaries

| Area | Owns | Does not own |
|---|---|---|
| `app/ui` | Qt widgets, layouts, accessibility labels, translated presentation | Domain decisions, process creation, engine command construction. |
| `app/controllers` | UI event coordination and presentation state | Native library calls or filesystem persistence details. |
| `app/application` | Use cases, stage graphs, orchestration, recovery decisions | PySide6 widget implementation or Blender Python APIs. |
| `app/models` | Dataclasses/enums/value objects and invariants | File I/O, subprocesses, HTTP, Qt. |
| `app/ports` | Stable interfaces for replaceable dependencies | Concrete library types. |
| `app/adapters` | Filesystem, image libraries, Qt processes, Windows secrets, viewer bridge | Workflow policy. |
| `generators` | Generator adapters and worker entry points | UI and general Blender repair. |
| `blender_scripts` | GPL-compatible code executed inside Blender | Desktop UI, API credentials, project navigation. |
| `viewer` | Offline TypeScript/Three.js source and tests | Project filesystem access outside the controlled bridge. |
| `app/validators` | Independent application-level validation | Silent repair or mutation. |
| `app/exporters` | Transactional format writing and reopen checks | Generator behavior. |
| `packaging` | Native build, installer, notices, engine manifests, signing pipeline | Runtime product logic. |

## 4. Required File Conventions

Python files use type hints, dataclasses or validated models for data, explicit `if`/`else` blocks, focused functions, and dependency injection at composition boundaries. User-facing strings do not appear directly in services or adapters; they use message keys. Paths use `pathlib.Path` internally and are converted to native argument values without shell concatenation.

Blender scripts share a small protocol and geometry-metrics module but keep individual operations separate. A pipeline runner composes operations from a validated request. No application API key or provider secret is imported into Blender.

The viewer is authored in TypeScript, built deterministically, and copied to `assets/viewer/dist`. The source and license remain in the repository. Runtime files do not load scripts, fonts, icons, or models from the internet.

## 5. Runtime Data Layout on Windows

The source tree must not be reused as application data. A proposed installed/runtime layout is:

```text
%LOCALAPPDATA%\MiniFigure3DStudio\
├── config\
│   ├── settings.json
│   └── .env                  # optional compatibility path; never shipped
├── credentials\             # DPAPI metadata only; preferred secrets use Credential Manager
├── engines\
│   ├── background\<version>\
│   ├── hunyuan\<version>\
│   ├── blender\<version>\
│   └── colmap\<version>\
├── cache\
│   ├── viewer\
│   ├── thumbnails\
│   └── downloads\
├── logs\
└── recovery\

%USERPROFILE%\Documents\MiniFigure 3D Studio\Projects\
└── <project-safe-name>-<short-id>\
    ├── project.json
    ├── inputs\
    ├── masks\
    ├── runs\
    ├── artifacts\
    ├── reports\
    ├── exports\
    ├── logs\
    └── .staging\
```

The user may select another project root. The application warns when the root is removable or cloud-synced because retention and secure-deletion behavior can differ.

## 6. Dependency Files

`pyproject.toml` is the authoritative project metadata and tool-configuration file. `requirements.txt` remains as a human-readable runtime input to satisfy the requested deliverable structure. `requirements-lock.txt` is the generated, hashed Windows release lock after compatibility testing. Separate engine manifests describe non-core environments instead of putting Hunyuan/PyTorch/CUDA into the desktop lock.

| File | Purpose |
|---|---|
| `requirements.txt` | Direct core runtime dependencies with constrained compatible ranges. |
| `requirements-dev.txt` | Test, lint, type, packaging, SBOM, and audit tooling. |
| `requirements-lock.txt` | Fully resolved and hashed core Windows environment produced only after tests. |
| `packaging/engine_manifests/*.json` | Exact engine/model assets, revisions, hashes, licenses, regions, and protocol range. |
| `.env.example` | Provider variable names only; no real values or endpoints requiring secrets. |

## 7. Test Fixture Policy

The repository contains no photographs of real people. Image fixtures are generated patterns, rendered synthetic characters, or assets with documented redistribution rights. Mesh fixtures intentionally represent disconnected islands, open boundaries, inverted normals, thin walls, self-intersections, internal shells, floating color parts, bases, and keychain loops.

Every fixture directory includes an asset manifest with origin, generator/script, license, checksum, purpose, and expected findings. Real-engine outputs used for regression are retained only when their model license permits redistribution and the input is synthetic or appropriately licensed.

## 8. Packaging and License Boundary

The core application, Blender scripts, optional engines, Qt/Chromium, COLMAP, models, viewer, and fonts have separate notice directories. The release build collects notices based on the exact artifacts included. Published Blender API scripts remain source-visible and GPL-compatible. Hunyuan assets never enter a universal installer under the reviewed community license.

## 9. Initial File-Creation Order for Stage 2

The project should be created in dependency order rather than alphabetically:

1. Repository metadata, licenses, quality tools, schemas, domain models, and ports.
2. Project repository, atomic storage, logging/redaction, state machine, and fake process runner.
3. Minimal PySide6 shell, navigation, new project, and recovery UI.
4. Image import/quality services and screens.
5. Background adapter and non-destructive mask editor.
6. Process supervisor and worker protocol.
7. One legally approved generator adapter.
8. Offline viewer and bridge.
9. Blender scripts and adapter.
10. Validators, STL/GLB transactional exporters, packaging smoke tests, and MVP documentation.

Each sequence item is implemented file by file, tested before the next vertical slice, and accompanied by a modified-file list.

## 10. Structure Approval Criteria

Approval confirms the separation of the desktop shell from engine runtimes, separate GPL-compatible Blender script component, adapter-driven generator architecture, non-destructive project/artifact model, local offline viewer source, transactional exporters, test hierarchy, engine manifests, compliance assets, and user-data layout outside the repository.
