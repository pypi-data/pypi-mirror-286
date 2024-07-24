import json
import os
import shutil
from typing import List, Literal

import click

from morph.cli.flags import Flags
from morph.task.base import BaseTask
from morph.task.constant.project_config import ProjectConfig
from morph.task.utils.morph import MorphYaml
from morph.task.utils.os import OsUtils
from morph.task.utils.sqlite import SqliteDBManager


class PrintResourceTask(BaseTask):
    def __init__(self, args: Flags):
        super().__init__(args)
        self.args = args

        self.alias = args.ALIAS
        self.file = args.FILE

        # Initialize project root
        try:
            self.project_root = MorphYaml.find_abs_project_root_dir()
        except FileNotFoundError as e:
            click.echo(click.style(str(e), fg="red"))
            raise e

        # Initialize SQLite database
        self.db_manager = SqliteDBManager(self.project_root)
        self.db_manager.initialize_database()

    def run(self):
        if self.alias:
            resource = MorphYaml.find_resource_by_alias(
                self.alias, self.project_root, self.db_manager
            )
            if resource:
                click.echo(json.dumps(resource.to_dict(), indent=2))
            else:
                click.echo(f"Alias {self.alias} not found.")
        elif self.file:
            resource = MorphYaml.find_resource_by_path(
                self.file, self.project_root, self.db_manager
            )
            if resource:
                click.echo(json.dumps(resource.to_dict(), indent=2))
            else:
                click.echo(f"File {self.file} not found.")
        else:
            click.echo("Either --alias or --file must be provided.")


class CreateResourceTask(BaseTask):
    def __init__(self, args: Flags):
        super().__init__(args)

        # Validate required arguments
        self.file = args.FILE
        if not self.file:
            raise click.BadParameter("--file [-f] parameter is required.")
        ext = os.path.splitext(self.file)[1]
        if ext not in ProjectConfig.EXECUTABLE_EXTENSIONS:
            raise click.BadParameter(
                f"Unsupported file extension {ext}. Supported extensions are {ProjectConfig.EXECUTABLE_EXTENSIONS}."
            )

        # Initialize project root
        try:
            self.project_root = MorphYaml.find_abs_project_root_dir()
        except FileNotFoundError as e:
            click.echo(click.style(str(e), fg="red"))
            raise e

        # Initialize SQLite database
        self.db_manager = SqliteDBManager(self.project_root)
        self.db_manager.initialize_database()

        # Validate optional arguments
        self.alias = args.ALIAS
        resource = MorphYaml.find_resource_by_alias(
            self.alias, self.project_root, self.db_manager
        )
        if resource:
            raise click.BadParameter(f"Alias {self.alias} already exists.")

        # TODO: validate connection
        self.connection = args.CONNECTION

        # TODO: validate output_paths
        self.output_paths = list(args.OUTPUT_PATHS)

    def run(self):
        resource = MorphYaml.generate_new_alias(
            self.file,
            self.project_root,
            self.db_manager,
            self.alias,
            self.connection,
            self.output_paths,
        )
        click.echo(json.dumps(resource.to_dict(), indent=2))


class MoveResourceTask(BaseTask):
    def __init__(self, args: Flags):
        super().__init__(args)

        # Initialize project root
        try:
            self.project_root = MorphYaml.find_abs_project_root_dir()
        except FileNotFoundError as e:
            click.echo(click.style(str(e), fg="red"))
            raise e

        base_path = (
            self.project_root if OsUtils.is_at(self.project_root) else os.getcwd()
        )
        self.source = OsUtils.get_abs_path(args.SOURCE, base_path)
        self.target = OsUtils.get_abs_path(args.TARGET, base_path)

        # Validate required arguments
        if not os.path.exists(self.source):
            raise click.BadArgumentUsage(f"SOURCE path {self.source} does not exist.")
        if os.path.isdir(self.target) and not os.path.exists(self.target):
            raise click.BadArgumentUsage(f"TARGET path {self.target} does not exist.")

        # Source must be a valid file or directory
        self.source_type: Literal["file", "directory"]
        if os.path.isfile(self.source):
            self.source_type = "file"
        elif os.path.isdir(self.source):
            self.source_type = "directory"
        else:
            raise click.BadArgumentUsage(f"Unsupported SOURCE type {self.source}.")

        # Treat target as a file if it does not exist
        self.target_type: Literal["file", "directory"]
        if self.source_type == "directory":
            self.target_type = "directory"
        elif os.path.isdir(self.target):
            self.target_type = "directory"
        elif os.path.isfile(self.target):
            self.target_type = "file"
        else:
            raise click.BadArgumentUsage(f"Unsupported TARGET type {self.target}.")

        # Initialize SQLite database
        self.db_manager = SqliteDBManager(self.project_root)
        self.db_manager.initialize_database()

        # Load morph.yaml
        self.morph_yaml = MorphYaml.load_yaml(self.project_root)

    def run(self):
        if self.source_type == "file":
            # Determine the target file path
            target_file_path: str
            if self.target_type == "file":
                target_file_path = self.target
            if self.target_type == "directory":
                target_file_path = os.path.abspath(
                    os.path.normpath(
                        (os.path.join(self.target, os.path.basename(self.source)))
                    )
                )

            # Update morph.yaml
            for alias, res_dict in self.morph_yaml.resources.items():
                resource_path = OsUtils.get_abs_path(
                    res_dict["path"], self.project_root
                )
                if resource_path == self.source:
                    res_dict["path"] = target_file_path
            self.morph_yaml.save_yaml(self.project_root)

            # Move the file
            os.rename(self.source, target_file_path)
        elif self.source_type == "directory" and self.target_type == "directory":
            # Update morph.yaml
            for alias, res_dict in self.morph_yaml.resources.items():
                resource_path = OsUtils.get_abs_path(
                    res_dict["path"], self.project_root
                )
                if resource_path.startswith(self.source):
                    res_dict["path"] = os.path.abspath(
                        os.path.normpath(
                            os.path.join(
                                self.target,
                                os.path.relpath(resource_path, self.source),
                            )
                        )
                    )
            self.morph_yaml.save_yaml(self.project_root)

            # Move the directory
            os.rename(self.source, self.target)
        else:
            raise click.BadArgumentUsage("Unsupported move operation.")

        # Sync morph.yaml to SQLite
        self.db_manager.sync_resources_from_yaml()
        click.echo(click.style("Synced morph.yaml to SQLite database.", fg="green"))


class RemoveResourceTask(BaseTask):
    def __init__(self, args: Flags):
        super().__init__(args)

        # Initialize project root
        try:
            self.project_root = MorphYaml.find_abs_project_root_dir()
        except FileNotFoundError as e:
            click.echo(click.style(str(e), fg="red"))
            raise e

        base_path = (
            self.project_root if OsUtils.is_at(self.project_root) else os.getcwd()
        )
        self.target = OsUtils.get_abs_path(args.TARGET, base_path)

        # Validate required arguments
        if not os.path.exists(self.target):
            raise click.BadArgumentUsage(f"TARGET path {self.target} does not exist.")

        # Target must be a valid file or directory
        self.target_type: Literal["file", "directory"]
        if os.path.isfile(self.target):
            self.target_type = "file"
        elif os.path.isdir(self.target):
            self.target_type = "directory"
        else:
            raise click.BadArgumentUsage(f"Unsupported TARGET type {self.target}.")

        # Initialize SQLite database
        self.db_manager = SqliteDBManager(self.project_root)
        self.db_manager.initialize_database()

        # Load morph.yaml
        self.morph_yaml = MorphYaml.load_yaml(self.project_root)

    def run(self):
        # Collect aliases to be deleted
        aliases_to_delete: List[str] = []

        if self.target_type == "file":
            # Collect aliases for file
            for alias, res_dict in self.morph_yaml.resources.items():
                resource_path = OsUtils.get_abs_path(
                    res_dict["path"], self.project_root
                )
                if resource_path == self.target:
                    aliases_to_delete.append(alias)

            # Update morph.yaml
            for alias in aliases_to_delete:
                del self.morph_yaml.resources[alias]
            self.morph_yaml.save_yaml(self.project_root)

            # Remove the file
            os.remove(self.target)
        elif self.target_type == "directory":
            # Collect aliases for directory
            for alias, res_dict in self.morph_yaml.resources.items():
                resource_path = OsUtils.get_abs_path(
                    res_dict["path"], self.project_root
                )
                if resource_path.startswith(self.target):
                    aliases_to_delete.append(alias)

            # Update morph.yaml
            for alias in aliases_to_delete:
                del self.morph_yaml.resources[alias]
            self.morph_yaml.save_yaml(self.project_root)

            # Remove the directory
            shutil.rmtree(self.target)
        else:
            raise click.BadArgumentUsage("Unsupported remove operation.")

        # Sync morph.yaml to SQLite
        self.db_manager.sync_resources_from_yaml()
        click.echo(click.style("Synced morph.yaml to SQLite database.", fg="green"))
