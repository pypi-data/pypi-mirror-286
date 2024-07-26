import os
import subprocess
from pathlib import Path

from dotenv import load_dotenv

from samgis_core import app_logger


load_dotenv()
root_folder = Path(globals().get("__file__", "./_")).absolute().parent.parent.parent
env_project_root_folder = os.getenv("PROJECT_ROOT_FOLDER", str(root_folder))
env_input_css_path = os.getenv("INPUT_CSS_PATH")


def assert_envs(envs_list):
    for current_env in envs_list:
        try:
            assert current_env is not None and current_env != ""
        except AssertionError as aex:
            app_logger.error(f"error on assertion for current_env: {current_env}.")
            raise aex


def read_std_out_err(std_out_err, output_type: str, command: list):
    output = std_out_err.split("\n")
    app_logger.info(f"output type:{output_type} for command:{' '.join(command)}.")
    for line in iter(output):
        app_logger.info(f"output_content_home stdout:{line.strip()}.")
    app_logger.info("########")


def run_command(commands_list: list, capture_output: bool = True, text: bool = True, check: bool = True) -> None:
    try:
        output_content_home = subprocess.run(
            commands_list,
            capture_output=capture_output,
            text=text,
            check=check
        )
        read_std_out_err(output_content_home.stdout, "stdout", commands_list)
        read_std_out_err(output_content_home.stderr, "stderr", commands_list)
    except Exception as ex:
        app_logger.error(f"ex:{ex}.")
        raise ex


def build_frontend(
        project_root_folder: str | Path,
        input_css_path: str | Path,
        output_dist_folder: Path = root_folder / "static" / "dist",
        index_page_filename: str = "index.html",
        output_css_filename: str = "output.css",
        force_build: bool = False,
    ) -> bool:
    assert_envs([
        str(project_root_folder),
        str(input_css_path)
    ])
    project_root_folder = Path(project_root_folder)
    index_html_pathfile = Path(output_dist_folder) / index_page_filename
    output_css_pathfile = Path(output_dist_folder) / output_css_filename
    if not force_build and output_css_pathfile.is_file() and index_html_pathfile.is_file():
        app_logger.info("frontend ok, build_frontend not necessary...")
        return False

    # install deps
    os.chdir(project_root_folder / "static")
    current_folder = os.getcwd()
    app_logger.info(f"current_folder:{current_folder}, install pnpm...")
    run_command(["which", "npm"])
    run_command(["npm", "install", "-g", "npm", "pnpm"])
    app_logger.info(f"install pnpm dependencies...")
    run_command(["pnpm", "install"])

    # build frontend dist and assert for its correct build
    output_css = str(output_dist_folder / output_css_filename)
    output_index_html = str(output_dist_folder / index_page_filename)
    output_dist_folder = str(output_dist_folder)
    app_logger.info(f"pnpm: build '{output_dist_folder}'...")
    run_command(["pnpm", "build"])
    app_logger.info(f"pnpm: ls -l {output_index_html}:")
    run_command(["ls", "-l", output_index_html])
    cmd = ["pnpm", "tailwindcss", "-i", str(input_css_path), "-o", output_css]
    app_logger.info(f"pnpm: {' '.join(cmd)}...")
    run_command(["pnpm", "tailwindcss", "-i", str(input_css_path), "-o", output_css])
    app_logger.info(f"pnpm: ls -l {output_css}:")
    run_command(["ls", "-l", output_css])
    app_logger.info(f"end!")
    return True


if __name__ == '__main__':
    build_frontend(
        project_root_folder=Path(env_project_root_folder),
        input_css_path=Path(env_input_css_path)
    )
