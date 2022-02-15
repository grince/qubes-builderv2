import click

from qubesbuilder.config import STAGES, STAGES_ALIAS
from qubesbuilder.cli.cli_base import aliased_group, ContextObj
from qubesbuilder.plugins.helpers import (
    getSourcePlugin,
    getTemplatePlugin,
    getSignPlugin,
    getPublishPlugin,
)


@aliased_group("template", chain=True)
def template():
    """
    Template CLI
    """


# FIXME: Find a better design to register necessary plugins for each stage.
def _template_stage(obj: ContextObj, stage_name: str):
    """
    Generic function to trigger stage for a template component
    """
    click.echo(f"Running template stage: {stage_name}")
    executor = obj.config.get_stages()[stage_name]["executor"]

    # Qubes templates
    for component in obj.components:
        if not component.is_template():
            continue
        for tmpl in obj.templates:
            plugins = [
                getSourcePlugin(
                    component=component,
                    dist=tmpl.distribution,
                    plugins_dir=obj.config.get_plugins_dir(),
                    executor=executor,
                    artifacts_dir=obj.config.get_artifacts_dir(),
                    verbose=obj.config.verbose,
                    debug=obj.config.debug,
                    skip_if_exists=obj.config.get("reuse-fetched-source"),
                ),
                getTemplatePlugin(
                    component=component,
                    template=tmpl,
                    plugins_dir=obj.config.get_plugins_dir(),
                    executor=executor,
                    artifacts_dir=obj.config.get_artifacts_dir(),
                    verbose=obj.config.verbose,
                    debug=obj.config.debug,
                    use_qubes_repo=obj.config.get("use-qubes-repo"),
                ),
                getSignPlugin(
                    component=component,
                    template=template,
                    dist=tmpl.distribution,
                    plugins_dir=obj.config.get_plugins_dir(),
                    executor=executor,
                    artifacts_dir=obj.config.get_artifacts_dir(),
                    verbose=obj.config.verbose,
                    debug=obj.config.debug,
                    gpg_client=obj.config.get("gpg-client"),
                    sign_key=obj.config.get("sign-key"),
                ),
                getPublishPlugin(
                    component=component,
                    template=template,
                    dist=tmpl.distribution,
                    plugins_dir=obj.config.get_plugins_dir(),
                    executor=executor,
                    artifacts_dir=obj.config.get_artifacts_dir(),
                    verbose=obj.config.verbose,
                    debug=obj.config.debug,
                    gpg_client=obj.config.get("gpg-client"),
                    sign_key=obj.config.get("sign-key"),
                    qubes_release=obj.config.get("qubes-release"),
                    publish_repository=obj.config.get("publish-repository"),
                ),
            ]
            for plugin in plugins:
                plugin.run(stage=stage_name)


@click.command(name="all", short_help="Run all template stages.")
@click.pass_obj
def _all_template_stage(obj: ContextObj):
    for s in STAGES:
        _template_stage(obj=obj, stage_name=s)


@template.command()
@click.pass_obj
def fetch(obj: ContextObj):
    _template_stage(obj=obj, stage_name="fetch")


@template.command()
@click.pass_obj
def prep(obj: ContextObj):
    _template_stage(obj=obj, stage_name="prep")


@template.command()
@click.pass_obj
def build(obj: ContextObj):
    _template_stage(obj=obj, stage_name="build")


@template.command()
@click.pass_obj
def post(obj: ContextObj):
    _template_stage(obj=obj, stage_name="post")


@template.command()
@click.pass_obj
def verify(obj: ContextObj):
    _template_stage(obj=obj, stage_name="verify")


@template.command()
@click.pass_obj
def sign(obj: ContextObj):
    _template_stage(obj=obj, stage_name="sign")


@template.command()
@click.pass_obj
def publish(obj: ContextObj):
    _template_stage(obj=obj, stage_name="publish")


template.add_command(fetch)
template.add_command(prep)
template.add_command(build)
template.add_command(post)
template.add_command(verify)
template.add_command(sign)
template.add_command(publish)
template.add_command(_all_template_stage)

template.add_alias(**STAGES_ALIAS)
