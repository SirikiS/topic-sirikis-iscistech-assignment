from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = engine.begin().connection.engine.dialect.name is not None and __import__("sqlalchemy.orm").orm.declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def search_scans_by_query(db, query: str, owner_id: int | None = None) -> list:
    sql = text(
        """
        SELECT id, title, description, severity, status, cve_id, affected_component, owner_id, created_at
        FROM scan_results
        WHERE (title LIKE :query OR description LIKE :query OR cve_id LIKE :query OR affected_component LIKE :query)
          AND (:owner_id IS NULL OR owner_id = :owner_id)
        """
    )
    result = db.execute(sql, {"query": f"%{query}%", "owner_id": owner_id})
    return [dict(row._mapping) for row in result]
