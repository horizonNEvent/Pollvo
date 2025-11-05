from models.tust_models import Base, create_sqlite_engine

engine = create_sqlite_engine("sqlite:///tust.db", echo=True)
Base.metadata.create_all(engine)