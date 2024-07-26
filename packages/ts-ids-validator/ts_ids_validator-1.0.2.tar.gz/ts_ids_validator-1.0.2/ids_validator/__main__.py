import argparse
import json
import sys
from pathlib import Path

from rich.console import Console

from ids_validator import tdp_api
from ids_validator.ids_validator import validate_ids, validate_ids_using_tdp_artifact


def main():
    parser = argparse.ArgumentParser(description="Validate IDS Artifacts")

    parser.add_argument(
        "-i",
        "--ids_dir",
        "--ids-dir",
        type=Path,
        default=".",
        required=False,
        help="Path to the IDS folder",
    )

    # Add previous IDS artifact dir and TDP-download arguments as mutually exclusive
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-p",
        "--previous_ids_dir",
        "--previous-ids-dir",
        type=Path,
        default=None,
        required=False,
        help=(
            "Path to a folder containing another version of the IDS, used to "
            "validate whether two specific versions are compatible. "
            "For full versioning validation, the `--download` or `--git` flag must be "
            "used: this option is only for development purposes."
        ),
    )
    download_action = group.add_argument(
        "-d",
        "--download",
        help=(
            "(Boolean flag) Whether to download other IDS versions from TDP. "
            "This is used to validate that the new IDS is compatible with existing "
            "versions of the same IDS retrieved from TDP. "
            "To use this option, you must provide API configuration, either as "
            "environment variables 'TS_API_URL', 'TS_ORG' and 'TS_AUTH_TOKEN' (see the "
            "README for more), or as a JSON config file (see `--config`)."
        ),
        action="store_true",
        # If a config is passed, the download argument is required
        required=False,
    )
    group.add_argument(
        "-g",
        "--git",
        help=(
            "(Boolean flag) Whether to retrieve other IDS versions from git tags. "
            "This is used to validate that the new IDS is compatible with existing "
            "versions of the same IDS as an alternative to the --download flag which "
            "doesn't require configuring TDP credentials. "
            "Git tags must match `vM.m.p[.B]` where `M` (major), `m` (minor), "
            "`p` (patch) and the optional `B` (build) are integers. "
            "This assumes the version in the tag name matches the actual IDS version "
            "in schema.json at that tag - note that it is possible for these to be "
            "out of sync, and it is possible for the local tagged versions to be out "
            "of sync with the artifact available in TDP. "
            "It is recommended to use --download before uploading an IDS to TDP, but "
            "--git may be more convenient for iterative local development or CI/CD "
            "checks if tags are appropriately maintained."
        ),
        action="store_true",
        required=False,
    )
    parser.add_argument(
        "-c",
        "--config",
        help=(
            "Configuration for using the TDP API in a JSON file containing the keys "
            "'api_url', 'org' and 'auth_token'. Provide either this or the equivalent "
            "environment variables to use the `--download` flag."
        ),
        type=argparse.FileType("r"),
        required=False,
        default=None,
    )
    args = parser.parse_args()

    if args.config is not None and not args.download:
        # Validate `download` is required when `config` is used
        raise argparse.ArgumentError(
            argument=download_action,
            message=(
                "When the config argument is used, the download flag is required: "
                "Add `-d` to the command."
            ),
        )
    console = Console()
    try:
        if args.download:
            # Get existing IDSs via API download
            api_config = tdp_api.APIConfig.from_json_or_env(
                json.load(args.config) if args.config else None
            )
            result = validate_ids_using_tdp_artifact(
                ids_dir=args.ids_dir,
                api_config=api_config,
                console=console,
            )
        elif args.git:
            # Only import git-related modules where git is used, because it can fail
            # if a `git` executable is not installed
            from ids_validator.ids_validator_git import validate_ids_using_git_tags

            # Get existing IDSs from git tags
            result = validate_ids_using_git_tags(
                ids_dir=args.ids_dir,
                console=console,
            )
        else:
            # Note previous_ids_dir may be `None`
            result = validate_ids(
                ids_dir=args.ids_dir,
                previous_ids_dir=args.previous_ids_dir,
                console=console,
            )

        return_code = 0 if result else 1

    except Exception as exc:
        console.print(
            f"[b i red]\nValidation Failed with critical error.[/b i red]\n{exc}"
        )

        return_code = 1

    sys.exit(return_code)


if __name__ == "__main__":
    main()
