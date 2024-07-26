"""
Copyright (C) 2022-2024 Stella Technologies (UK) Limited.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""

import importlib
from typing import Any, List

import click
from loguru import logger

from stellanow_cli.core.utils.logger_utils import log_processed_and_skipped_result
from stellanow_cli.exceptions.cli_exceptions import (
    StellaNowCLILanguageNotSupportedException,
    StellaNowCLINamespaceNotProvidedException,
)
from stellanow_cli.services.code_generator.code_generator import CodeGeneratorService, pass_code_generator_service
from stellanow_cli.services.code_generator.tools import (
    collect_all_model_references,
    collect_model_references,
    fetch_model_details,
    generate_event_files,
    generate_model_files,
)


@click.command()
@click.option("--namespace", "-n", default="", help="The namespace for the generated classes.")  # if empty raise in C#
@click.option("--destination", "-d", default=".", help="The directory to save the generated classes.")
@click.option("--force", "-f", is_flag=True, help="Overwrite existing files.")
@click.option("--event_names", "-e", multiple=True, help="List of specific events to generate.")
@click.option(
    "--language",
    "-l",
    type=click.Choice(["csharp"], case_sensitive=False),
    default="csharp",
    help="The programming language for the generated classes.",
)
@pass_code_generator_service
def generate(
    service: CodeGeneratorService,
    destination: str,
    force: bool,
    event_names: List[str],
    language: str,
    **kwargs: dict[str, Any],
):
    """Fetches the latest event specifications from the API and generates corresponding class code in the desired
    programming language."""

    if language == "csharp" and not kwargs.get("namespace"):
        raise StellaNowCLINamespaceNotProvidedException

    logger.info("Generating...")

    generator_class_name = f"{language.capitalize()}CodeGenerator"
    try:
        generator_class = getattr(
            importlib.import_module(f"stellanow_cli.code_generators.{language}_code_generator"), generator_class_name
        )
    except ImportError:
        raise StellaNowCLILanguageNotSupportedException(language)

    events = service.get_events()

    if event_names:
        events = [event for event in events if event.name in event_names]

    model_refs = collect_model_references(service=service, events=events)
    all_model_refs = collect_all_model_references(service=service, model_ids=model_refs)
    models_details = fetch_model_details(service=service, model_refs=all_model_refs)

    models_processed, models_skipped = generate_model_files(
        generator_class=generator_class, models_details=models_details, destination=destination, force=force, **kwargs
    )
    events_not_found, events_processed, events_skipped = generate_event_files(
        generator_class=generator_class,
        events=events,
        event_names=event_names,
        service=service,
        models_details=models_details,
        destination=destination,
        force=force,
        **kwargs,
    )

    all_skipped_files = models_skipped + events_skipped

    log_processed_and_skipped_result(models_processed + events_processed, all_skipped_files, events_not_found)


generate_cmd = generate
