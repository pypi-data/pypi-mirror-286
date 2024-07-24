import click

log_format = click.option(
    "--log-format",
    envvar="MORPH_LOG_FORMAT",
    help="Specify the format of logging to the console and the log file. Use --log-format-file to configure the format for the log file differently than the console.",
    type=click.Choice(["text", "debug", "json", "default"], case_sensitive=False),
    default="default",
)


def require_canvas_if_dag(ctx, param, value):
    if ctx.params.get("dag") and not value:
        raise click.BadParameter("--canvas is required when --dag is specified.")
    return value


canvas = click.option(
    "--canvas",
    "-c",
    help="Specify the canvas name.",
    callback=require_canvas_if_dag,
)

dag = click.option(
    "--dag",
    "-d",
    is_flag=True,
    help="Run as a Directed Acyclic Graph (DAG).",
)

dry_run = click.option(
    "--dry-run",
    "-n",
    is_flag=True,
    help="Perform a dry run without executing the tasks.",
)

file = click.option(
    "--file",
    "-f",
    type=click.Path(exists=True),
    help="Specify the path to the resource.",
)

alias = click.option(
    "--alias",
    "-a",
    type=str,
    help="Specify the alias of the resource.",
)

connection = click.option(
    "--connection",
    "-c",
    type=str,
    help="Specify the connection slug.",
)

output_paths = click.option(
    "--output-paths",
    "-o",
    type=click.Path(exists=False),
    multiple=True,
    help="Specify the output paths.",
)
