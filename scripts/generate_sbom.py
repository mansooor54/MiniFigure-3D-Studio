from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path


def _direct_dependency_names(pyproject_path: Path) -> set[str]:
    with pyproject_path.open("rb") as handle:
        data = tomllib.load(handle)
    raw_dependencies = data["project"]["dependencies"]
    names: set[str] = set()
    for dependency in raw_dependencies:
        name = dependency.split("[", maxsplit=1)[0]
        for separator in ("<", ">", "=", "!", "~", ";"):
            name = name.split(separator, maxsplit=1)[0]
        names.add(name.strip().lower().replace("_", "-"))
    return names


def _cyclonedx_cli() -> str:
    candidate = Path(sys.executable).with_name("cyclonedx-py")
    if candidate.is_file():
        return str(candidate)
    discovered = shutil.which("cyclonedx-py")
    if discovered is None:
        raise RuntimeError("cyclonedx-py is not installed in the active environment")
    return discovered


def _validate_output(output_path: Path, pyproject_path: Path) -> None:
    data = json.loads(output_path.read_text(encoding="utf-8"))
    components = data.get("components")
    if not isinstance(components, list) or not components:
        raise RuntimeError("Generated SBOM has no components")
    component_names = {
        str(component.get("name", "")).lower().replace("_", "-")
        for component in components
        if isinstance(component, dict)
    }
    missing = sorted(_direct_dependency_names(pyproject_path) - component_names)
    if missing:
        raise RuntimeError(f"SBOM is missing direct dependencies: {', '.join(missing)}")
    metadata = data.get("metadata")
    if not isinstance(metadata, dict) or not isinstance(metadata.get("component"), dict):
        raise RuntimeError("Generated SBOM is missing root component metadata")


def generate_sbom(project_root: Path, environment: Path, output_path: Path) -> None:
    pyproject_path = project_root / "pyproject.toml"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        _cyclonedx_cli(),
        "environment",
        "--pyproject",
        str(pyproject_path),
        "--mc-type",
        "application",
        "--output-reproducible",
        "--of",
        "JSON",
        "-o",
        str(output_path),
        "--validate",
        str(environment),
    ]
    subprocess.run(command, check=True, cwd=project_root)
    _validate_output(output_path, pyproject_path)


def _parse_args() -> argparse.Namespace:
    project_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=project_root)
    parser.add_argument("--environment", type=Path, default=Path(sys.prefix))
    parser.add_argument(
        "--output",
        type=Path,
        default=project_root / "reports" / "generated" / "development-sbom.json",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    generate_sbom(
        args.project_root.resolve(),
        args.environment.resolve(),
        args.output.resolve(),
    )
    print(args.output.resolve())


if __name__ == "__main__":
    main()
