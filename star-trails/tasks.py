from invoke import task


@task
def setup_dev(c):
    """Install requirements for development."""
    c.run(f"pip install --upgrade pip")
    c.run(f"pip install -r requirements-dev.txt")


@task
def lint(c):
    """Run lint - only checks"""
    c.run("isort --check-only . --skip .venv;")
    c.run('black --check . --exclude ".venv";')


@task
def lint_apply(c):
    """Run lint - only checks"""
    c.run("isort . --skip .venv;")
    c.run('black . --exclude ".venv";')
