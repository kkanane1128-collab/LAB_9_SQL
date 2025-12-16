import subprocess
import datetime
import os
import click

@click.command()
@click.option("--user", default="root", help="Utilisateur MySQL pour le dump.")
@click.option("--password", prompt=True, hide_input=True, help="Mot de passe MySQL de l'utilisateur.")
@click.option("--db", default="universite", help="Base de données à sauvegarder.")
def backup_db(user, password, db):
    """Effectue un dump (sauvegarde) de la base de données via mysqldump."""
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"dump_{db}_{ts}.sql"
    
    click.echo(f"Démarrage du backup de la base '{db}'...")

    try:
        command = [
        r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe",
        "-u", user, 
        f"-p{password}", 
        "--routines", 
        "--triggers", 
        db,
       "-r", filename
        ]
        
        subprocess.run(command, check=True, capture_output=True, text=True)
        
        click.echo(f" Backup réussi ! Sauvegardé dans : {os.path.abspath(filename)}")
        
    except subprocess.CalledProcessError as e:
        click.echo(f" Erreur lors de l'exécution de mysqldump : {e.stderr}")
    except FileNotFoundError:
        click.echo(" Erreur : 'mysqldump' non trouvé. Veuillez installer MySQL Client Tools.")

if __name__ == "__main__":
    backup_db()