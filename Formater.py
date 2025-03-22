#!/usr/bin/env python3

import subprocess as sbp
import asyncio as asy


async def main():
    
    sbp.run(["diskutil", "list"], check=True)
    
    CleId = input("Entre l'identifiant de la clé : ")
    
    while CleId == "":
        print("⚠️ Attention ⚠️")
        await asy.sleep(2)
        CleId = input("Entre l'identifiant de la clé : ")
    
    NouveauNom = input("Comment Voulez vous renommer votre clé? : ")
    
    if NouveauNom == "":
        NouveauNom = "USBFormater"
    
    print("Choisisez le type de formatage")
    print("1: Format ExFAT (compatible Windows & macOS)")
    print("2: Format FAT32 (ancien mais très compatible)")
    print("3: Format macOS (APFS/Mac OS")
    print("4: Format JHFS  (Mac OS étendu journalisé)")
    
    Choix = int(input("Entre le numéro de ton choix (defaut : 1): "))
    Demontage = ["diskutil", "unmountDisk", f"/dev/{CleId}"]
    sbp.run(Demontage, check=True)    
    
    if Choix == 1:
        FormatExFat = ["diskutil", "eraseDisk", "ExFAT", f"{NouveauNom}", f"/dev/{CleId}"]
        sbp.run(FormatExFat, check=True)
    
    elif Choix == 2:
        FormaFat32 = ["diskutil", "eraseDisk", "MS-DOS", f"{NouveauNom}" f"/dev/{CleId}"]
        sbp.run(FormaFat32, check=True)
    
    elif Choix == 3:
        FormatAPFS = ["diskutil", "eraseDisk", "APFS", f"{NouveauNom}", f"/dev/{CleId}"]
        sbp.run(FormatAPFS, check=True)
    elif Choix == 4:
        FormatJHFS = ["diskutil", "eraseDisk", "JHFS+" f"{NouveauNom}", f"/dev/{CleId}"]
        sbp.run(FormatJHFS, check=True)
    else:
        print("Choix Invalide nous allons formater en ExFAt! ")
        FormatPardfaut = ["diskutil", "eraseDisk", "ExFAT", f"{NouveauNom}", f"/dev/{CleId}"]
        sbp.run(FormatPardfaut, check=True)
        
    
    Ejecter = input("Veux tu Ejecter ? (O/N) : ")
    
    if  Ejecter in ( "O", "o", "Oui", "oui"):
        Ejection = ["diskutil", "eject", f"/dev/{CleId}"]
        sbp.run([Ejection], check=True)
        print("C'est bon Tu peux retirer ta clé Pourrite la 🤣🤣")

    print("Fin de l'opéarion faut gérer un léger djai a Py hein🐍🤣")

asy.run(main())