import subprocess
import datetime

# Générer un message de commit automatique avec la date et l'heure
commit_message = f"Auto-commit: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

# Exécuter les commandes Git
try:
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    
    # Récupérer le nom de la branche actuelle
    branch = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True).stdout.strip()
    
    subprocess.run(["git", "push", "origin", branch], check=True)

    print(f"✅ Commit et push effectués sur la branche '{branch}' message : {commit_message}")

except subprocess.CalledProcessError as e:
    print(f"❌ Erreur lors de l'exécution de Git : {e}")
