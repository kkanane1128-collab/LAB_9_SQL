import click
from db import get_conn 
from models import Session 

@click.group()
def cli():
    pass

@cli.command()
@click.argument("titre")
@click.option("--credits", default=3, type=int, help="Nombre de crédits du cours.")
def add_course(titre, credits):
    """Ajoute un nouveau cours (méthode native)."""
    conn = get_conn()
    if conn is None: return
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO COURS (titre, credits) VALUES (%s, %s)", (titre, credits))
        conn.commit()
        click.echo(f"Cours '{titre}' ajouté.")
    except Exception as e:
        conn.rollback()
        click.echo(f" Erreur lors de l'ajout: {e}")
    finally:
        conn.close()

@cli.command()
def list_courses():
    conn = get_conn()
    if conn is None: return
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, titre, credits FROM COURS ORDER BY id")
        click.echo("\n--- Liste des Cours ---")
        for (id, titre, credits) in cur:
            click.echo(f"[{id}] {titre} ({credits} crédits)")
    finally:
        conn.close()
        
@cli.command()
@click.argument("nom")
@click.argument("email")
def add_student_orm(nom, email):
    """Ajoute un étudiant via l'ORM SQLAlchemy."""
    session = Session()
    try:
        from models import Etudiant 
        nouvel_etudiant = Etudiant(nom=nom, email=email)
        session.add(nouvel_etudiant)
        session.commit()
        click.echo(f"Étudiant '{nom}' (Email: {email}) ajouté via ORM.")
    except Exception as e:
        session.rollback()
        click.echo(f"Erreur ORM lors de l'ajout de l'étudiant: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    cli()