from pathlib import Path

import pytest
from lib.infrastructure.config.containers import Container
from tests.markers import RUNNING_IN_CI


@pytest.mark.skipif(RUNNING_IN_CI, reason="Skipping test in CI")
def test_localgpt_embedding_service(app_container: Container):
    localgpt_embedding_service = app_container.localgpt_embedding_gateway()
    assert localgpt_embedding_service is not None
    thesis_pdf = Path("tests/mocks/source_docs/MA_Thesis_LABG.pdf")
    assert thesis_pdf.exists()
    assert thesis_pdf.is_file()
    document = localgpt_embedding_service.load_single_document(path=str(thesis_pdf))
    localgpt_embedding_service.create_embeddings(documents=[document])

    localgpt_inference_service = app_container.localgpt_inference_gateway()
    assert localgpt_inference_service is not None

    qa = localgpt_inference_service.qa

    query = "What were Pareto's main contributions to the development of Expected Utility Theory?"

    res = qa(query)
    answer, documents = res["result"], res["source_documents"]
    print(f"Query: {query}\nAnswer: {answer}\nDocuments: {documents}")
    assert answer is not None
    assert len(documents) > 0
