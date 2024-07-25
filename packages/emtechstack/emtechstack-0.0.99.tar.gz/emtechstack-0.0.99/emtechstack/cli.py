import click
from emtechstack.commands import (
    init_profile,
    start_infra as start_infra_function,
    stop_infra as stop_infra_function,
    start_api as start_api_function,
    stop_api as stop_api_function,
    build_env,
    clean_code,
    find_and_kill_processes,
    update_emtechstack,
    update_requirements as update_requirements_function,
    show_version,
    graceful_shutdown as graceful_shutdown_function,
    push_to_new_repo
)


@click.group()
def cli():
    """Emtechstack CLI Tool"""
    pass


@cli.command()
@click.option("--profile", required=True, help="Profile path to initialize")
@click.option("--name", help="Custom directory name for the cloned profile")
def init(profile, name):
    """Initialize the profile by cloning the repo"""
    init_profile(profile, name)


@cli.command()
def start_infra():
    """Start the infrastructure using docker-compose"""
    start_infra_function()


@cli.command()
def stop_infra():
    """Stop the infrastructure using docker-compose"""
    stop_infra_function()


@cli.command()
@click.option("--port", default="8000", help="Port to run the API on")
def start_api(port):
    """Start the FastAPI application"""
    start_api_function(port)


@cli.command()
def stop_api():
    """Stop the FastAPI application"""
    stop_api_function()


@cli.command()
@click.option("--name", help="Name of the Conda environment to create and activate")
@click.option("--python", default="3.11", help="Python version. By default is 3.11")
def build(name, python):
    """Build and activate the Conda environment, and install dependencies from requirements.txt"""
    build_env(name,python)


@cli.command()
def clean():
    """Clean the code using black"""
    clean_code()


@cli.command()
@click.option("--port", required=True, help="Port to clean")
def clean_port(port):
    """Clean the port"""
    find_and_kill_processes(port)


@cli.command()
def update():
    """Update the emtechstack package"""
    update_emtechstack()


@cli.command()
def upgrade():
    """Update the emtechstack package"""
    update_emtechstack()

@cli.command()
def update_requirements():
    """Update the requirements.txt file with installed package versions"""
    update_requirements_function()
    

@cli.command()
def version():
    """Show the current version of EmTechStack"""
    show_version()
    

@cli.command()
def graceful_shutdown():
    """Gracefully shutdown the API and Infra application"""
    graceful_shutdown_function()
    
    
@cli.command()
def goodnight():
    """Gracefully shutdown the API and Infra application"""
    graceful_shutdown_function()
    graceful_shutdown_function()
    
    
@cli.command()
@click.option("--repository", required=True, help="The repository URL that you want to push for the first time (initial commit)")
@click.option("--branch", required=True, help="The branch name to push to (main or master or ...)")
@click.option("--message", default="feat: Initial Commit From EmTechStack", help="The commit message for the initial commit")
def init_push(repository, branch, message):
    """Gracefully shutdown the API and Infra application"""
    push_to_new_repo(
        repo_url=repository,
        branch_name=branch,
        first_commit=message,
    )
    
if __name__ == "__main__":
    cli()
