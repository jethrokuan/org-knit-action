#!/usr/bin/env python3

from subprocess import run
from os import environ
from pathlib import Path

from inputs import Inputs
from colour import *


def git_result(work_dir, *args):
    r = run(["git", *args], cwd=work_dir, capture_output=True)
    return r.stdout.decode().strip()


def remote_from_token(I: Inputs):
    # TODO add checks, i.e. is branch prohibited? is repo external?
    return f"https://x-access-token:{I.github_token}@github.com/{environ['GITHUB_REPOSITORY']}.git"


def push(work_dir: Path, I: Inputs):
    def git(*args):
        return run(["git", *args], cwd=work_dir)

    print(blue | f"Configuring repository to push to {I.branch}")

    run(["rm", "-rf", work_dir.absolute() / ".git"])
    git("init")
    git("checkout", "--orphan", I.branch)
    git("remote", "add", "origin", remote_from_token(I))

    git("add", "--all")

    git("config", "user.name", I.name)
    git("config", "user.email", I.email)

    message = I.commit_message.replace("!#!", environ["GITHUB_SHA"])

    git("commit", "-m", message)

    print(f'Commited: "{message}"')

    print(blue | "Add remote, and stage files")

    git("push", "origin", "--force", I.branch)
    print(green | f"Pushed.")
