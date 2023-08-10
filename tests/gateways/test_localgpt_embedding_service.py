from lib.infrastructure.config.containers import Container


def test_localgpt_embedding_service(app_container: Container):
    localgpt_embedding_service = app_container.localgpt_embedding_service()
    assert localgpt_embedding_service is not None
    text = "The quick brown fox jumps over the lazy dog."
    # embeddings = localgpt_embedding_service.get_embeddings(text=text)
    # print(embeddings)