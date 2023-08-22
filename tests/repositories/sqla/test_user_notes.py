from lib.core.entity.models import NoteType
from lib.infrastructure.repository.sqla.models import SQLAUser, SQLAUserNote

def test_crud_user_notes(db_session):
    maany = SQLAUser(prada_user_uuid="maany")
    
    note  = SQLAUserNote(
        title="Test Note",
        content="This is a test note",
        user = maany,
        type = NoteType.USER
    )

    with db_session() as session:
        session.add_all([maany, note])
        session.commit()

    with db_session() as session:
        user = session.query(SQLAUser).filter_by(prada_user_uuid="maany").first()
        assert user.notes[0].title == "Test Note"
        assert user.notes[0].content == "This is a test note"
        assert user.notes[0].type == NoteType.USER

def test_delete_notes(db_session):
    maany = SQLAUser(
        prada_user_uuid="maany",
        notes=[
            SQLAUserNote(
                title="Test Note",
                content="This is a test note",
                type = NoteType.USER
            ),
            SQLAUserNote(
                title="Test Note 2",
                content="This is a test note 2",
                type = NoteType.USER
            )
        ]
    )

    with db_session() as session:
        session.add(maany)
        session.commit()

    with db_session() as session:
        user = session.query(SQLAUser).filter_by(prada_user_uuid="maany").first()
        assert len(user.notes) == 2

        session.delete(user.notes[0])
        session.commit()

    with db_session() as session:
        user = session.query(SQLAUser).filter_by(prada_user_uuid="maany").first()
        assert len(user.notes) == 1
        assert user.notes[0].title == "Test Note 2"
        assert user.notes[0].content == "This is a test note 2"
        assert user.notes[0].type == NoteType.USER