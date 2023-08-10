from pathlib import Path
from lib.infrastructure.config.containers import Container


def test_localgpt_embedding_service(app_container: Container):
    localgpt_embedding_service = app_container.localgpt_embedding_service()
    assert localgpt_embedding_service is not None
    constitution_pdf = Path("tests/mocks/source_docs/constitution.pdf")
    assert constitution_pdf.exists()
    assert constitution_pdf.is_file()
    document = localgpt_embedding_service.load_single_document(path=str(constitution_pdf))
    chroma_collection = localgpt_embedding_service.create_embeddings(documents=[document])
    # print(embeddings)