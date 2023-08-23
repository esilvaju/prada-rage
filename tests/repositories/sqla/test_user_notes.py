from faker import Faker
from lib.core.entity.models import NoteType
from lib.infrastructure.repository.sqla.models import SQLAUser, SQLAUserNote

def test_crud_user_notes(db_session, fake: Faker):
    username = fake.name()
    maany = SQLAUser(prada_user_uuid=username)
    
    note_title = fake.name()
    note  = SQLAUserNote(
        title=note_title,
        content=fake.text(),
        user = maany,
        type = NoteType.USER
    )

    with db_session() as session:
        session.add_all([maany, note])
        session.commit()

    with db_session() as session:
        user = session.query(SQLAUser).filter_by(prada_user_uuid=username).first()
        assert user.notes[0].title == note_title
        assert user.notes[0].type == NoteType.USER

def test_delete_notes(db_session, fake: Faker):
    username = fake.name()
    note_title = fake.name()
    maany = SQLAUser(
        prada_user_uuid=username,
        notes=[
            SQLAUserNote(
                title="Test Note",
                content="This is a test note",
                type = NoteType.USER
            ),
            SQLAUserNote(
                title=note_title,
                content="This is a test note 2",
                type = NoteType.USER
            )
        ]
    )

    with db_session() as session:
        session.add(maany)
        session.commit()

    with db_session() as session:
        user = session.query(SQLAUser).filter_by(prada_user_uuid=username).first()
        assert len(user.notes) == 2

        session.delete(user.notes[0])
        session.commit()

    with db_session() as session:
        user = session.query(SQLAUser).filter_by(prada_user_uuid=username).first()
        assert len(user.notes) == 1
        assert user.notes[0].title == note_title
        assert user.notes[0].content == "This is a test note 2"
        assert user.notes[0].type == NoteType.USER

def test_user_is_present_in_notes(db_session, faker: Faker):
    username = faker.name()
    note_title = faker.name()
    maany = SQLAUser(
        prada_user_uuid=username,
        notes=[
            SQLAUserNote(
                title=note_title,
                content="This is a test note",
                type = NoteType.USER
            ),
            SQLAUserNote(
                title=faker.name(),
                content="This is a test note 2",
                type = NoteType.USER
            )
        ]
    )

    with db_session() as session:
        session.add(maany)
        session.commit()

    with db_session() as session:
        note = session.query(SQLAUserNote).filter_by(title=note_title).first()
        assert note.user.prada_user_uuid == username
