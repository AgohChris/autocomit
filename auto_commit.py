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
        diff_output = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True).stdout

        if not diff_output.strip():
            msg = "rien d'extra."
            return msg
        
        completion = openai.ChatCompletion.create(
            # extra_headers={
            #     "HTTP-Referer": "https://votre-site.com",
            #     "X-Title": "Auto-Commit AI",
            # },
            model="openai/gpt-4.1",  # Modèle utilisé
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Tu es un assistant qui aide à générer des messages de commit Git clairs et descriptifs. "
                        "Analyse les changements fournis et propose un message de commit adapté. "
                        "Le message doit être court, précis et refléter les modifications apportées."
                    )
                },
                {"role": "user", "content": f"Voici les changements dans le projet :\n{diff_output}"}
            ],
            max_tokens=100,
            temperature=0.7,
        )
     # Extraire le message généré
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