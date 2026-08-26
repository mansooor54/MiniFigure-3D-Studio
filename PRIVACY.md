# Privacy Policy for Development

## Local-First Default

MiniFigure 3D Studio is designed to process photographs, masks, textures, and 3D models locally by default. No image, model, project, diagnostic bundle, or usage event may leave the computer unless the user selects a named external operation and explicitly confirms the transfer.

## Sensitive Data

| Data | Default treatment |
|---|---|
| Source photographs and likeness | Restricted project data stored in the selected project workspace. |
| Masks, textures, point/mesh artifacts, and previews | Derived sensitive data; remain local and retain provenance. |
| Person/model name | Sensitive project metadata; excluded from telemetry and ordinary log routing. |
| EXIF and local paths | Minimized; unneeded metadata stripped before any approved external transfer. |
| API credentials | Stored by reference in Windows-protected storage where possible; never stored in projects or logs. |
| Operational metrics | Local bounded logs may store stage IDs, durations, versions, counts, and stable errors after redaction. |

## External Services

Before any external request, the application must show the provider name, purpose, selected image count, data categories, metadata handling, and actual cancellation limitation. Consent is tied to the provider, purpose, data categories, endpoint/policy version, and time. Declining consent leaves local and unrelated functions available.

No external provider is configured or enabled in the Stage 2 foundation.

## Retention and Deletion

Projects retain imported and derived artifacts locally until the user deletes them. Deleting originals must explain that masks, textures, meshes, and other derived likeness data may remain. Deleting a project stops jobs, closes handles, inventories managed files, prevents traversal outside the project root, and reports any remaining items.

Application-level overwrite and deletion cannot guarantee storage-device sanitization on SSDs, snapshots, synchronized folders, or backups. Any enhanced cleanup option must be described as best effort, not guaranteed secure erasure.

## Logs and Diagnostics

Logs and copied errors must exclude image pixels, thumbnails, masks, textures, credentials, authorization headers, unconsented personal data, and unsafe full paths. Diagnostic bundles are local, previewable, and user-saved; they are never uploaded automatically.

## Development and Test Data

The repository and CI use synthetic or explicitly licensed fixtures. Real-person photographs and generated likenesses must not be committed, attached to issues, included in screenshots, or retained in CI artifacts.

## Analytics and Crash Reporting

Analytics and remote crash reporting are not implemented or enabled by default. Adding either requires a separate data inventory, explicit opt-in design, redaction tests, and owner approval.
