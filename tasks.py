#!/usr/bin/python
import os
import platform

from invoke import task


def _project_name():
    return "epiblog"


def _aws_region():
    return "eu-west-1"


def _venv_dir():
    if platform.system() == "Windows":
        return "venv"
    return ".venv"


def _activate():
    if platform.system() == "Windows":
        return "call %s/Scripts/activate.bat" % _venv_dir()
    return "source %s/bin/activate" % _venv_dir()


def _pty():
    if platform.system() == "Windows":
        return False
    return True


@task
def stack_build(ctx):
    ctx.run(f"sam build --region {_aws_region()} --use-container")


@task(pre=[stack_build])
def stack_deploy(ctx, cicd_bucket):
    with ctx.prefix(_activate()):
        ctx.run(f"aws s3 cp spec/api-spec.yaml s3://{cicd_bucket}/spec/api-spec.yaml")
        ctx.run(f"sam package --s3-bucket {cicd_bucket} --output-template-file packaged.yaml")
        ctx.run(f"sam deploy packaged.yaml "
                f"--capabilities CAPABILITY_NAMED_IAM "
                f"--parameter-overrides "
                f" CicdBucket={cicd_bucket} "
                f"--s3-bucket {cicd_bucket} "
                f"--stack-name {_project_name()} "
                f"--region {_aws_region()} ")


@task
def stack_delete(ctx):
    ctx.run(f"aws cloudformation delete-stack --stack-name {_project_name()} --region {_aws_region()}")


@task
def test(ctx):
    with ctx.prefix(_activate()):
        os.environ["TABLE_NAME"] = f"{_project_name()}"
        ctx.run(f"python -m pytest")


@task
def venv(ctx):
    """Create virtualenv"""
    ctx.run("python -m venv %s" % _venv_dir(), pty=_pty())
    with ctx.prefix(_activate()):
        ctx.run("python -m pip install --upgrade pip setuptools wheel invoke wget", pty=_pty())


@task(pre=[venv])
def bootstrap(ctx):
    """Bootstrap"""
    with ctx.prefix(_activate()):
        ctx.run(" python -m pip install -e .", pty=_pty())
        if os.path.exists("dev-requirements.txt"):
            ctx.run(" python -m pip install -r dev-requirements.txt", pty=_pty())
        if os.path.exists("test-requirements.txt"):
            ctx.run(" python -m pip install -r test-requirements.txt", pty=_pty())
