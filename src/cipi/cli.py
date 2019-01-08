import click

import cipi.core


@click.command()
@click.version_option(version=cipi.__version__)
def main():
    cipi.core.main(sh_name='cipi.sh')
