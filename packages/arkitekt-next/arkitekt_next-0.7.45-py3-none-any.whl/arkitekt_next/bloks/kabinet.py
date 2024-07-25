from typing import Dict, Any
import secrets

from arkitekt_next.bloks.funcs import (
    create_default_service_yaml,
    create_default_service_dependencies,
    build_default_service_options,
)
from blok import blok, InitContext, ExecutionContext, Option
from blok.tree import Repo, YamlFile


@blok("live.arkitekt.kabinet")
class KabinetBlok:
    def __init__(self) -> None:
        self.dev = False
        self.host = "kabinet"
        self.command = "bash run-debug.sh"
        self.repo = "https://github.com/arkitektio/kabinet-server"
        self.scopes = {
            "kabinet_deploy": "Deploy containers",
            "kabinet_add_repo": "Add repositories to the database",
        }
        self.mount_repo = False
        self.build_repo = False
        self.buckets = ["media"]
        self.secret_key = secrets.token_hex(16)
        self.ensured_repos = ["jhnnsrs/ome:main", "jhnnsrs/renderer:main"]
        self.image = "jhnnsrs/kabinet:next"

    def get_builder(self):
        return "arkitekt.generic"

    def get_dependencies(self):
        return create_default_service_dependencies()

    def preflight(self, init: InitContext):
        for key, value in init.kwargs.items():
            setattr(self, key, value)

        self.service = create_default_service_yaml(
            init, self, {"ensured_repos": self.ensured_repos}
        )

        self.initialized = True

    def build(self, context: ExecutionContext):
        context.docker_compose.set_nested("services", self.host, self.service)

    def get_options(self):
        def_options = build_default_service_options(self)
        with_repos = Option(
            subcommand="repos",
            help="The default repos to enable for the service",
            default=self.secret_key,
        )

        return [
            *def_options,
            with_repos,
        ]
