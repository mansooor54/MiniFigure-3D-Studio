# MiniFigure-3D-Studio
You are an expert software engineer specializing in Python, artificial intelligence, image processing, 3D modeling, Blender automation, and 3D printing.

Create a complete professional desktop application named:

# MiniFigure 3D Studio

## Project Objective

The application converts photographs of a real person into a small 3D miniature figure that can be edited in Blender or printed using a 3D printer.

The application must support realistic figures, cartoon figures, Chibi miniatures, busts, bobbleheads, bas-reliefs, and keychains. It must also prepare, repair, scale, color-separate, validate, and export the generated model for 3D printing.

## 1. Target Platform and Technology

* Target operating systems: Windows 10 and Windows 11.
* Main programming language: Python 3.11.
* Desktop user interface: PySide6.
* Use Blender as a background 3D-processing engine through its Command Line and Python API.
* Use a modular architecture that allows additional AI engines to be added later.
* Create a Windows EXE installer using PyInstaller.
* The user must not need to open Blender manually.
* The interface must support Arabic RTL and English LTR.
* The application must work without requiring a permanent internet connection, except when the user selects an external AI API.

## 2. Model Generation Modes

Create two separate generation modes.

### Mode A: Fast AI Mode

This mode is intended for users who have between one and six photographs.

Requirements:

* Use Hunyuan3D 2.1 as the default local image-to-3D engine.
* Select the best front-facing or 45-degree photograph as the primary input.
* Use the remaining photographs as visual references for clothing, skin, hair, and accessory colors.
* Do not claim that multiple images were submitted directly to the AI model if the selected engine does not support multi-image input.
* Create a separate Generator Adapter interface so that Tripo, Meshy, or other APIs can be added later.
* Do not hard-code API keys.
* Read API keys from a secure local `.env` file.
* Clearly inform the user if an image will be sent to an external service.
* Allow the user to select CPU, GPU, or automatic processing mode.
* Detect insufficient GPU memory and provide a useful error message or fallback option.

### Mode B: Accurate Scan Mode

This mode is intended for users who have between 24 and 80 overlapping photographs taken around the person.

Requirements:

* Use COLMAP for Structure-from-Motion and Multi-View Stereo processing.
* Extract camera positions, a sparse point cloud, a dense point cloud, and a reconstructed mesh.
* Display clear photography instructions before the user begins.
* Ask the person to remain completely still.
* Recommend even lighting and a non-reflective background.
* Detect blurry, duplicated, underexposed, or low-resolution images before reconstruction begins.
* Display which camera angles are missing.
* If reconstruction fails, display the actual failure reason and useful corrective steps.
* Never generate a fake successful result when reconstruction fails.

## 3. User Interface

Create a clean and modern user interface using:

* Dark navy blue.
* White.
* Gold.
* Clear icons.
* Large preview areas.
* Step-by-step navigation.
* Arabic RTL and English LTR support.

The workflow must include:

1. Create a new project.
2. Enter a project and model name.
3. Import images using drag and drop.
4. Assign a view to each image:

   * Front
   * Back
   * Left
   * Right
   * Front Left
   * Front Right
5. Check image quality.
6. Remove the background automatically.
7. Allow manual background-mask correction.
8. Select the model style.
9. Configure dimensions and printing options.
10. Generate the model.
11. Preview the model in 3D.
12. Repair and optimize the mesh.
13. Separate printable colors.
14. Validate printability.
15. Export the final files.

Display a real progress indicator for every stage.

Include:

* Cancel button.
* Pause button where technically supported.
* Retry button.
* Simplified log window.
* Expandable technical error details.
* Button to copy error information.

Do not freeze the interface during long operations. Use `QProcess`, `QThread`, or another safe asynchronous system.

## 4. Supported Figure Styles

Add the following styles:

* Realistic Full Body
* Cartoon
* Chibi Miniature
* Bobblehead
* Bust
* Keychain
* Bas-Relief
* Custom Style

For Chibi mode:

* Make the head proportionally larger than the body.
* Preserve the person’s primary facial characteristics.
* Make the hands, feet, fingers, and accessories thick enough for printing.
* Simplify fragile details that may break during printing.
* Allow adjustment of the head-to-body ratio.
* Keep both feet connected to the base when possible.

## 5. 3D Printing Settings

Allow the user to configure:

* Final model height in millimeters.
* Default height: 100 mm.
* Supported range: 40–250 mm.
* Minimum wall thickness.
* Polygon target.
* Hollow or solid model.
* Drain holes for resin printing.
* Circular or square base.
* Base diameter.
* Base thickness.
* Raised or engraved name on the base.
* Keychain loop.
* Keychain hole diameter.
* Number of filament colors: 1, 4, 8, or 16.

Add preset profiles for:

* Creality K2 with CFS.
* Orca Slicer.
* Creality Print.
* Generic FDM Printer.
* Resin Printer.

## 6. Blender Processing Pipeline

Run Blender in Background Mode and execute an automated processing pipeline.

The pipeline must:

1. Import the raw generated mesh.
2. Create a backup copy before modification.
3. Identify and remove small disconnected artifacts that do not belong to the main model.
4. Apply Merge by Distance.
5. recalculate and correct face normals.
6. Detect and close mesh holes.
7. Repair non-manifold geometry.
8. Apply Voxel Remesh when necessary.
9. Reduce polygon count with Decimate while preserving the face.
10. Strengthen thin fingers, clothing edges, accessories, and other fragile details.
11. Combine the body and base using Boolean Union.
12. Remove intersecting, floating, or internal geometry.
13. Place the bottom of the model at `Z = 0`.
14. Convert all measurements to millimeters.
15. Scale the model to the user’s selected final height.
16. Generate front, back, left, and right preview renders.

Avoid damaging important facial details during remeshing or decimation.

## 7. Printability Validation

Generate a printability report containing:

* Whether the model is watertight.
* Number of non-manifold edges.
* Number of disconnected objects.
* X, Y, and Z dimensions.
* Polygon count.
* Minimum wall thickness violations.
* Floating parts.
* Internal geometry.
* Difficult overhang areas.
* Whether the base touches the build plate.
* Whether any error prevents export.
* Recommended print orientation.
* Estimated support requirement.

Use three clear result states:

* Ready to Print.
* Ready with Warnings.
* Repair Required.

## 8. Color System

The application must clearly distinguish between texture colors and printable filament colors.

### Texture Mode

* Preserve PBR textures.
* Use this mode for GLB, OBJ, and Blender exports.
* Preserve image textures and material maps where supported.

### Filament Color Mode

* Convert the model colors into a limited printable palette.
* Support 4, 8, or 16 colors.
* Separate skin, hair, clothes, shoes, accessories, and the base into independent meshes or material regions.
* Prevent very small floating color objects.
* Allow the user to manually change each color.
* Display all parts and their assigned colors before export.
* Allow merging visually similar colors.
* Ensure that the resulting 3MF opens correctly in Orca Slicer and Creality Print with recognizable parts or material assignments.

Do not assume that a PBR image texture can be printed directly by a standard multi-filament printer.

## 9. Integrated 3D Viewer

Create an integrated 3D viewer with:

* Rotate.
* Zoom.
* Pan.
* Wireframe view.
* Material and color view.
* Display of separate model parts.
* Red highlighting for printability problems.
* Before-and-after comparison.
* Front, back, left, and right views.
* Screenshot export.

Use a locally bundled Three.js viewer inside Qt WebEngine or another suitable OpenGL solution.

Do not depend on loading JavaScript libraries from the internet while the application is running.

## 10. Export Formats

Support these formats:

* 3MF for multi-color 3D printing.
* STL for single-color printing.
* OBJ with MTL and textures.
* GLB for preserving materials.
* BLEND for manual editing in Blender.

Before exporting:

* Verify model dimensions.
* Verify manifold geometry.
* Verify the number of disconnected objects.
* Display warnings when a problem exists.
* Do not treat successful file creation as proof that the model is printable.
* Validate that the exported file can be opened and contains valid geometry.

## 11. Privacy and Consent

Photographs of people are sensitive data.

The application must:

* Use local processing by default.
* Request explicit consent before sending images to an external API.
* Display the name of the external service.
* Allow the user to delete original images after model generation.
* Avoid collecting images or analytics without consent.
* Never write images or API keys into log files.
* Provide a Delete Project button.
* Require confirmation before deleting a project.
* Remove temporary files when the user chooses secure deletion.
* Display a reminder that the user must have permission to process the photographed person.

## 12. Error Handling

Handle at least these cases:

* Blender is not installed.
* Blender executable path is invalid.
* COLMAP is missing.
* No compatible GPU is available.
* Insufficient VRAM.
* Low-resolution input image.
* The full body is not visible.
* Background removal fails.
* AI generation fails.
* Photogrammetry reconstruction fails.
* Boolean operation fails.
* Mesh repair fails.
* 3MF export fails.
* The destination folder is not writable.
* The user cancels the operation.

Display understandable Arabic and English messages with expandable technical information.

Do not hide errors or create an empty file and report it as successful.

## 13. Project Structure

Use a clean project structure similar to:

```text
mini_figure_studio/
    app/
        main.py
        ui/
        controllers/
        services/
        models/
        workers/
        validators/
        exporters/
        localization/
    blender_scripts/
        cleanup_mesh.py
        add_base.py
        add_keychain_loop.py
        split_colors.py
        validate_printability.py
        export_models.py
    generators/
        base_generator.py
        hunyuan_generator.py
        photogrammetry_generator.py
    tests/
    assets/
    docs/
    requirements.txt
    pyproject.toml
    .env.example
    README_AR.md
    README_EN.md
    LICENSE
```

Use:

* Type hints.
* Dataclasses.
* Structured logging.
* Clear interfaces.
* Dependency injection where useful.
* Pytest.
* Small and focused functions.
* Meaningful class and variable names.

Do not use the ternary operator written as `?:`. Use explicit `if` and `else` statements.

## 14. Testing Requirements

Create automated tests for:

* Image validation.
* Blur detection.
* Dimension calculations.
* Millimeter unit conversion.
* Removal of disconnected artifacts.
* Manifold validation.
* Base creation.
* Keychain-loop creation.
* Color separation.
* Export validation.
* Arabic file and folder paths.
* Task cancellation.
* Missing Blender installation.
* Missing COLMAP installation.
* Failed external API calls.
* Recovery from interrupted processing.

Do not include photographs of real people in the repository. Use synthetic images or properly licensed test assets.

## 15. Required Deliverables

Deliver the project in stages.

### Stage 1: Planning and Architecture

Provide:

* Architecture document.
* Data-flow diagram.
* User-interface design.
* Dependency and license list.
* Security and privacy plan.
* Implementation roadmap.
* Proposed project structure.

### Stage 2: Working MVP

Implement:

* Image import.
* Image validation.
* Background removal.
* One working generation engine.
* Integrated 3D preview.
* Blender cleanup pipeline.
* STL and GLB export.

### Stage 3: Advanced Features

Implement:

* Accurate Scan Mode.
* Printable color separation.
* 3MF export.
* Printability report.
* Windows installer.
* Arabic and English localization.

Create the code file by file. Do not place the entire application in one source file.

After completing each stage:

1. Run the relevant tests.
2. Fix all discovered errors.
3. Explain how to install and run the project.
4. List every created or modified file.
5. Do not continue to the next stage until the current stage works.
6. Never claim that a test passed unless it was actually executed.
7. Clearly report any unfinished or unsupported feature.

Start with Stage 1 only.

Before writing the application code, present the proposed architecture, data flow, user-interface structure, dependencies, licensing considerations, risks, and implementation plan for approval.
