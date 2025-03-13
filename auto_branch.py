import subprocess as sbp
import datetime as dt


Q1_Init = input("le dépot déja initialisé? Y/N :")

try:
    if Q1_Init == "Y" or Q1_Init=="y":
        Nom_branche = input("Comment veux tu appeler ta branche? : ")
        commit_message = input("Entre un méssage pour le commit : ")
        
        if commit_message=="":
            commit_message = f"commit du : {dt.datetime.now().strftime('%d-%m-%Y à %H:%M:%S')}"
        
        sbp.run(["git", "checkout", "-b", Nom_branche], check=True)
        sbp.run(["git", "add", "."], check=True)
        sbp.run(["git", "commit", "-m", commit_message], check=True)


    elif Q1_Init == "N" or Q1_Init=="n":
        link_repos = input("Entre le lien du repositorie : ")

        while link_repos == "":
                print("Attention")
                link_repos = input("Entre le lien du repositorie : ")
        
        sbp.run(["git", "init"], check=True)
        sbp.run(["git", "remote", "add", "origin", ""], check=True)
        
        Nom_branche = input("Comment veux tu appeler ta branche? : ")
        commit_message = input("Entre un méssage pour le commit : ")
        
        if commit_message=="":
            commit_message = f"commit du : {dt.datetime.now().strftime('%d-%m-%Y à %H:%M:%S')}"
        
        sbp.run(["git", "checkout", "-b", Nom_branche], check=True)
        sbp.run(["git", "add", "."], check=True)
        sbp.run(["git", "commit", "-m", commit_message], check=True)
        sbp.run(["git", "push", "-u", "origin", Nom_branche], check=True)


except sbp.CalledProcessError as e:
    print(f"Erreur lors de l'exécution de {e}")