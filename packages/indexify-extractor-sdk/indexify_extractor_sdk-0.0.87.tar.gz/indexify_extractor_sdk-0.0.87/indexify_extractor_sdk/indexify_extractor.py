import asyncio
from . import coordinator_service_pb2
from .base_extractor import ExtractorWrapper, ExtractorDescription
from typing import Optional, Tuple, List
from .base_extractor import Content, EXTRACTOR_MODULE_PATH
import nanoid
import json
from .extractor_worker import ExtractorModule, create_executor, describe
from .agent import ExtractorAgent
import os
from .coordinator_service_pb2 import Extractor
from .downloader import save_extractor_description, create_extractor_db


def local(extractor: str, text: Optional[str] = None, file: Optional[str] = None):
    if text and file:
        raise ValueError("You can only pass either text or file, not both.")
    if not text and not file:
        raise ValueError("You need to pass either text or file")
    if text:
        content = Content.from_text(text)
    if file:
        content = Content.from_file(file)
    module, cls = extractor.split(":")
    wrapper = ExtractorWrapper(module, cls)
    result = wrapper.extract_batch({"task_id": content}, input_params={"task_id": "{}"})
    print(result)


def split_validate_extractor(name: str) -> Tuple[str, str]:
    try:
        module, cls = name.split(":")
    except ValueError:
        raise ValueError(
            "The extractor name should be in the format 'module_name:class_name'"
        )
    return module, cls


def join(
    workers: int,
    listen_port: int,
    coordinator_addr: str = "localhost:8950",
    ingestion_addr: str = "localhost:8900",
    advertise_addr: Optional[str] = None,
    config_path: Optional[str] = None,
    extractor: Optional[str] = None,
    download_method: str = "direct",
):
    print(
        f"joining {coordinator_addr} and sending extracted content to {ingestion_addr}"
    )
    executor = create_executor(workers=workers, extractor_id=extractor)
    asyncio.set_event_loop(asyncio.new_event_loop())
    descriptions: List[
        ExtractorDescription
    ] = asyncio.get_event_loop().run_until_complete(
        describe(asyncio.get_event_loop(), executor)
    )

    # Available extractors locally.
    extractors: List[Extractor] = []

    for description in descriptions:
        embedding_schemas = {}
        for name, embedding_schema in description.embedding_schemas.items():
            embedding_schemas[name] = embedding_schema.model_dump_json()

        metadata_schemas = {}
        for name, metadata_schema in description.metadata_schemas.items():
            metadata_schemas[name] = json.dumps(metadata_schema)

        extractors.append(
            Extractor(
                name=description.name,
                description=description.description,
                input_params=description.input_params,
                input_mime_types=description.input_mime_types,
                metadata_schemas=metadata_schemas,
                embedding_schemas=embedding_schemas,
            )
        )

    id = nanoid.generate()
    print(f"executor id: {id}")

    server = ExtractorAgent(
        id,
        extractors=extractors,
        executor=executor,
        coordinator_addr=coordinator_addr,
        num_workers=workers,
        extractor_arg=extractor,
        listen_port=listen_port,
        ingestion_addr=ingestion_addr,
        advertise_addr=advertise_addr,
        config_path=config_path,
        download_method=download_method,
    )

    try:
        asyncio.get_event_loop().run_until_complete(server.run())
    except asyncio.CancelledError as ex:
        print("exiting gracefully", ex)


def describe_sync(extractor):
    module, cls = extractor.split(":")
    wrapper = ExtractorWrapper(module, cls)
    print(wrapper.describe())


def install_local(extractor, install_system_dependencies=False):
    # Copy everything in the current directory to the extractors directory.
    parent_dir = os.path.basename(os.getcwd())
    destination = os.path.join(EXTRACTOR_MODULE_PATH, parent_dir)
    os.system(f"cp -r . {destination}")
    print(f"copied to {destination} for testing")

    # Describe the extractor.
    module, cls = extractor.split(":")
    module_name = f"indexify_extractors.{parent_dir}.{module}"
    wrapper = ExtractorWrapper(module_name, cls)
    # FIX ME - This doesn't work on Mac
    # Meant to only work on Ubuntu
    if install_system_dependencies:
        install_system_dependencies = wrapper._instance.system_dependencies
        os.system(f"sudo apt-get install -y {' '.join(install_system_dependencies)}")
    description = wrapper.describe()

    # Create a new extractor description.
    extractor_id = f"{parent_dir}.{module}:{cls}"
    create_extractor_db()
    save_extractor_description(extractor_id, description)

    print("extractor ready for testing. Run: indexify-extractor join-server")
    print(f"The module name for the extractor is: indexify_extractors.{parent_dir}.{module}:{cls}")
    print(f"To package the extractor in a docker container: indexify-extractor package indexify_extractors.{parent_dir}.{module}:{cls}")

