# !/usr/bin/env python3

import subprocess
import datetime as dt
import openai
import dotenv
import os
import traceback

dotenv.load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


openai.api_key=OPENROUTER_API_KEY
openai.api_base="https://openrouter.ai/api/v1"


def genererMessageAvecChatGpt():
    try:
        # Récupère le diff stagé
        diff_output = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True).stdout
        if not diff_output.strip():
            return "rien d'extra."

        # Liste des fichiers modifiés
        file_names = subprocess.run(["git", "diff", "--cached", "--name-only"], capture_output=True, text=True).stdout.strip()

        # Prend les 10 premières lignes de chaque fichier pour donner du contexte
        contenu_contextuel = ""
        for fichier in file_names.splitlines():
            if not os.path.isfile(fichier):
                continue
            try:
                with open(fichier, 'r') as f:
                    lignes = []
                    for i in range(10):
                        ligne = f.readline()
                        if not ligne:
                            break
                        lignes.append(ligne)
                    contenu_contextuel += f"\n\nFichier : {fichier}\n" + "".join(lignes)
            except Exception as fe:
                contenu_contextuel += f"\n\n[Fichier non lisible ou binaire] {fichier}\n"

        # Appel à l'API OpenRouter avec tout le contexte
        completion = openai.ChatCompletion.create(
            model="openai/gpt-4.1",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Tu es un assistant qui génère des messages de commit Git professionnels selon le style Conventional Commits "
                        "(ex: feat, fix, refactor, chore). Analyse les changements et les fichiers concernés pour produire un message "
                        "court, clair et significatif. Le message doit résumer la modification principale. Tu peux utiliser le français ou l'anglais."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Voici le diff (changements stagés) :\n{diff_output}\n\n"
                        f"Fichiers modifiés :\n{file_names}\n\n"
                        f"Contexte extrait des fichiers :\n{contenu_contextuel}"
                    )
                }
            ],
            max_tokens=100,
            temperature=0.5,
        )

        commit_message = completion.choices[0].message.content.strip()
        return commit_message

    except Exception as e:
        print(f"Erreur lors de la génération du message de commit : {e}")
        traceback.print_exc()
        return None



def autoCommit(succes=""):
    commit_message= genererMessageAvecChatGpt()

    if commit_message == "rien d'extra.":
        Date = dt.datetime.now().strftime('%d-%m-%Y à %H:%M:%S')
        commit_message = f"Auto-commit Gpt du : {Date}"

    if not commit_message:
        commit_message=input("Entre un méssage pour le commit : ")  

    if commit_message=="":
        Date = dt.datetime.now().strftime('%d-%m-%Y à %H:%M:%S')
        commit_message = f"Auto-commit du : {Date}"

    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        
        branch = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True).stdout.strip()
        
        subprocess.run(["git", "push", "origin", branch], check=True)

        succes = f"✅ Commit et push effectués sur la branche '{branch}' message : {commit_message}"
        print(succes)

    except subprocess.CalledProcessError as e:
       succes = f"❌ Erreur lors de l'exécution de Git : {e}"
       print(succes)
        
    return succes


if __name__ == "__main__":
    autoCommit()