import os
import asyncio
import pathlib
from cognee import config, add, cognify, search, SearchType, prune, visualize_graph
# from cognee.shared.utils import render_graph
from cognee.infrastructure.engine import DataPoint

async def main():
    data_directory_path = str(
        pathlib.Path(
            os.path.join(pathlib.Path(__file__).parent, ".data_storage")
        ).resolve()
    )
    # Set up the data directory. Cognee will store files here.
    config.data_root_directory(data_directory_path)

    cognee_directory_path = str(
        pathlib.Path(
            os.path.join(pathlib.Path(__file__).parent, ".cognee_system")
        ).resolve()
    )
    # Set up the Cognee system directory. Cognee will store system files and databases here.
    config.system_root_directory(cognee_directory_path)
    
    # Prune data and system metadata before running, only if we want "fresh" state.
    await prune.prune_data()
    await prune.prune_system(metadata=True)

    text = "The Python programming language is widely used in data analysis, web development, and machine learning."

    # Add the text data to Cognee.
    await add(text)


    # Define a custom graph model for programming languages.
    class FieldType(DataPoint):
        name: str = "Field"

    class Field(DataPoint):
        name: str
        is_type: FieldType

    class ProgrammingLanguageType(DataPoint):
        name: str = "Programming Language"

    class ProgrammingLanguage(DataPoint):
        name: str
        used_in: list[Field] = []
        is_type: ProgrammingLanguageType


    # Cognify the text data.
    await cognify(graph_model=ProgrammingLanguage)

    # # Get a graphistry url (Register for a free account at https://www.graphistry.com)
    # url = await render_graph()
    # print(f"Graphistry URL: {url}")

    # Or use our simple graph preview
    graph_file_path = str(
        pathlib.Path(
            os.path.join(pathlib.Path(__file__).parent, ".artifacts/graph_visualization.html")
        ).resolve()
    )
    await visualize_graph(graph_file_path)

    # Completion query that uses graph data to form context.
    completion = await search(SearchType.GRAPH_COMPLETION, "What is python?")
    print("Graph completion result is:")
    print(completion)

    # Completion query that uses document chunks to form context.
    completion = await search(SearchType.COMPLETION, "What is Python?")
    print("Completion result is:")
    print(completion)

    # Query all summaries related to query.
    summaries = await search(SearchType.SUMMARIES, "Python")
    print("Summary results are:")
    for summary in summaries:
        print(summary)

    chunks = await search(SearchType.CHUNKS, query_text="Python")
    print("Chunk results are:")
    for chunk in chunks:
        print(chunk)


if __name__ == "__main__":
    asyncio.run(main())
