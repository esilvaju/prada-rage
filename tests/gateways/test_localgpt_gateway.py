from pathlib import Path
from lib.infrastructure.config.containers import Container


def test_localgpt_embedding_service(app_container: Container):
    localgpt_embedding_service = app_container.localgpt_embedding_gateway()
    assert localgpt_embedding_service is not None
    constitution_pdf = Path("tests/mocks/source_docs/constitution.pdf")
    assert constitution_pdf.exists()
    assert constitution_pdf.is_file()
    document = localgpt_embedding_service.load_single_document(path=str(constitution_pdf))
    localgpt_embedding_service.create_embeddings(documents=[document])

    localgpt_inference_service = app_container.localgpt_inference_gateway()
    assert localgpt_inference_service is not None

    qa = localgpt_inference_service.qa

    query = "How long the president will stay in office?"

    res = qa(query)
    answer, documents = res["result"], res["source_documents"]
    print(f"Query: {query}\nAnswer: {answer}\nDocuments: {documents}")
    assert answer is not None
    assert len(documents) > 0
