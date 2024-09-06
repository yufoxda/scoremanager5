from Database.Schema.schema import Base,engine

Base.metadata.create_all(engine)