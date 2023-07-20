from sqlalchemy import Column, Integer, create_engine, VARCHAR, LargeBinary
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Publication(Base):
    __tablename__ = 'References'

    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR)
    authors = Column(VARCHAR)
    document = Column(LargeBinary)

class Cancelled(Exception):
    pass

import platform

def password_dialog() -> str:
    from PyQt6.QtWidgets import QInputDialog, QLineEdit
    dialog = QInputDialog()
    dialog.setInputMode(QInputDialog.InputMode.TextInput)
    dialog.setWindowTitle("Enter password")
    dialog.setLabelText("Password:")
    dialog.setTextEchoMode(QLineEdit.EchoMode.Password)
    ok = dialog.exec()
    if ok:
        return dialog.textValue()
    else:
        raise Cancelled("Cancelled")

def get_set_password():

    username="dsakurai"

    if platform.system() == "Darwin":

        keyring_name = 'keyring_reference_database'

        def get_password():

            import keyring

            # return None on failure
            return keyring.get_password(keyring_name, username)

        def set_password():
            import keyring
            from getpass import getpass

            print("This will save password to the system key chain")

            passwd    = password_dialog()

            keyring.set_password(keyring_name, username, passwd)

        pw = get_password()
        if pw:
            return pw
        else:
            set_password()
            return get_password()


def add_row(row: Publication):

    # The format of the connection string is:
    # dialect+driver://username:password@host:port/database


    password = get_set_password()

    engine = create_engine(
        'mysql+pymysql://dsakurai@localhost:3306/Reference_DSakurai',
        connect_args={'password': password}
    )
    Base.metadata.create_all(engine)
    session = Session(engine)

    session.add(row)
    session.commit()

