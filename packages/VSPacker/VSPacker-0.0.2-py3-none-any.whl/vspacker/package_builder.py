import os

from vspacker.io import pack_example, zip_files
from vspacker.vs_project import construct_output_folder, get_info


class AssemblyBuilder:
    def __init__(self, project_file):
        self.project_file = project_file
        self.project_dir = os.path.dirname(project_file)
        self.project_name, self.version = get_info(self.project_file)
        self.output_folder = construct_output_folder(self.project_dir, self.version)
        self.validate_paths()

    def validate_paths(self):
        if not os.path.exists(self.project_dir):
            raise FileNotFoundError(f"Project directory not found: {self.project_dir}")
        if not os.path.exists(self.project_file):
            raise FileNotFoundError(f"Project file not found: {self.project_file}")
        if not self.project_file.endswith(".csproj"):
            raise ValueError(f"Invalid project file: {self.project_file}")

    def build_zip(self, zip_filename, exclude_patterns, include_files):
        zip_path = zip_files(
            zip_filename,
            self.project_dir,
            ["*.gha", "*.dll"],
            exclude_patterns,
            include_files,
            True,
            self.project_name,
            self.output_folder,
        )
        print(f"Plugin built and zipped successfully: {zip_path}")
        return zip_path

    def package_example(self, example_file):
        if not os.path.exists(example_file):
            raise FileNotFoundError(f"Example file not found: {example_file}")
        example_path = pack_example(
            example_file,
            self.version,
            self.output_folder,
        )
        print(f"Example file packaged successfully: {example_path}")
        return example_path
