from invoke import task


@task
def setup_dev(c):
    """Install requirements for development."""
    c.run("pip install -r requirements-dev.txt")


@task
def lint(c):
    """Run lint, only check"""
    isort_lint = c.run("isort --check-only . --skip .venv", warn=True)
    black_lint = c.run('black --check . --exclude ".venv";', warn=True)

    if isort_lint.failed or black_lint.failed:
        raise SystemExit("Lint failed, you must run invoke lint-apply")


@task
def lint_apply(c):
    """Run lint, apply"""
    c.run("isort . --skip .venv")
    c.run('black . --exclude ".venv";')
