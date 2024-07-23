import shutil
from pathlib import Path

from .base import PythonResolver
from nrp_devtools.commands.utils import run_cmdline


class UVResolver(PythonResolver):
    """
    Resolver for UV package manager from https://github.com/astral-sh/uv
    """
    def lock_python_repository(self, subdir=None):
        pyproject_toml = "pyproject.toml"
        requirements_txt = "requirements.txt"
        if subdir:
            pyproject_toml = Path(subdir)/"pyproject.toml"
            requirements_txt = Path(subdir)/"requirements.txt"

        self.run_uv_pip("compile", str(pyproject_toml), "-o", str(requirements_txt))

    def export_requirements(self, subdir=None):
        if subdir:
            return (Path(subdir) / "requirements.txt").read_text()
        return (self.config.repository_dir / "requirements.txt").read_text()

    def install_project_packages(self):
        # convert the partial requirements to the real ones
        self.run_uv_pip("compile", "requirements.txt", "-o", "requirements-resolved-local.txt")

        # install the real ones
        self.run_uv_pip("sync", "requirements-resolved-local.txt")
        self.run_uv_pip("install", "-e", ".")


    def run_uv_pip(self, *args, subdir=None, **kwargs):

        cwd = self.config.repository_dir
        if subdir:
            cwd = cwd / subdir

        environ = {
            **self.remove_virtualenv_from_env(),
        }

        venv_path = self.config.venv_dir
        if venv_path.exists():
            environ["VIRTUAL_ENV"] = str(venv_path)
            print(f"Using venv for uv: {environ['VIRTUAL_ENV']}")

        return run_cmdline(
            "uv",
            "pip",
            *args,
            cwd=cwd,
            environ=environ,
            no_environment=True,
            raise_exception=True,
            **kwargs,
        )
