# database.py
 from imports import *
def create_app() -> Tuple[FastAPI, DeclarativeMeta]:
    app = FastAPI()

    # Set up SQLAlchemy
    database_url = 'sqlite:///products.db'
    engine = create_engine(database_url)
    Base.metadata.create_all(bind=engine)

    # Create SessionLocal
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = get_db

    return app, engine

