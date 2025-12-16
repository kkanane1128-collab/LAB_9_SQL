from sqlalchemy import (create_engine, Column, Integer, String, 
                        ForeignKey, Date, Float)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import date

MYSQL_PASSWORD = "*******" 
DATABASE_URL = f"mysql+pymysql://root:{MYSQL_PASSWORD}@localhost/universite"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Etudiant(Base):
    __tablename__ = "ETUDIANT"
    id    = Column(Integer, primary_key=True, autoincrement=True)
    nom   = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    inscriptions = relationship("Inscription", back_populates="etudiant")
    examens = relationship("Examen", back_populates="etudiant")

class Professeur(Base):
    __tablename__ = "PROFESSEUR"
    id    = Column(Integer, primary_key=True, autoincrement=True)
    nom   = Column(String(100), nullable=False)
    specialite = Column(String(100))
    enseignements = relationship("Enseignement", back_populates="professeur")

class Cours(Base):
    __tablename__ = "COURS"
    id      = Column(Integer, primary_key=True, autoincrement=True)
    titre   = Column(String(200), nullable=False)
    credits = Column(Integer, default=3)
    enseignements = relationship("Enseignement", back_populates="cours")
    inscriptions = relationship("Inscription", back_populates="cours")

class Enseignement(Base):
    __tablename__ = "ENSEIGNEMENT"
    prof_id = Column(Integer, ForeignKey('PROFESSEUR.id'), primary_key=True)
    cours_id = Column(Integer, ForeignKey('COURS.id'), primary_key=True)
    annee = Column(Integer, primary_key=True, default=date.today().year)
    professeur = relationship("Professeur", back_populates="enseignements")
    cours = relationship("Cours", back_populates="enseignements")

class Inscription(Base):
    __tablename__ = "INSCRIPTION"
    etudiant_id = Column(Integer, ForeignKey('ETUDIANT.id'), primary_key=True)
    cours_id = Column(Integer, ForeignKey('COURS.id'), primary_key=True)
    date_inscription = Column(Date, default=date.today)
    etudiant = relationship("Etudiant", back_populates="inscriptions")
    cours = relationship("Cours", back_populates="inscriptions")

class Examen(Base):
    __tablename__ = "EXAMEN"
    id          = Column(Integer, primary_key=True, autoincrement=True)
    etudiant_id = Column(Integer, ForeignKey('ETUDIANT.id'), nullable=False)
    cours_id    = Column(Integer, ForeignKey('COURS.id'), nullable=False)
    note        = Column(Float)
    date_examen = Column(Date, default=date.today)
    etudiant = relationship("Etudiant", back_populates="examens")
    cours = relationship("Cours")

if __name__ == '__main__':
    print("Création des tables dans la base universite...")
    Base.metadata.create_all(engine)

    print("Tables créées.")
