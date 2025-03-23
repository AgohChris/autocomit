#!/usr/bin/env python3

import subprocess as sbp
import os
import asyncio as asy
import shutil


async def main():
    
    sbp.run(["diskutil", "list"], check=True)
    Identifiant = input("Entre Id de la clé exp : disk2 : ")
    while Identifiant == "":
        await asy.sleep(1)
        print("⚠️ Attention ⚠️")
        await asy.sleep(2)
        Identifiant = input("Veuillez Entre l'identifiant de la clé à booter : ")
    
    Chemin = input("Entre le chemin ou se trouve l'iso : ")
    
    while Chemin == "":
        await asy.sleep(1)
        print("⚠️ Attention ⚠️")
        await asy.sleep(2)
        Identifiant = input("Veuillez Entre le chemin")
    
    Chemin = os.path.expanduser(Chemin)
    
    if not os.path.isfile(Chemin):
        print(f"Erreur Le Fichier ISO '{Chemin}' est Introuvable ")
        return
        
    sbp.run(["diskutil", "unmountDisk", "/dev/"+Identifiant] , check=True)
    
    try:
        if shutil.which("pv"):
            commandeBoot = f"sudo dd if={Chemin} | pv | sudo dd of=/dev/r{Identifiant} bs=1m"
        else:
            commandeBoot = f"sudo dd if={Chemin} of=/dev/r{Identifiant} bs=1m status=progress"
            processus = sbp.Popen(commandeBoot, shell=True, stdout=sbp.PIPE, stderr=sbp.STDOUT, text=True)
            
            for ligne in processus.stdout:
                print(ligne, end="")
            
            processus.wait()
        
        if processus.returncode !=0:
            raise sbp.CalledProcessError(processus.returncode, commandeBoot)
        
        sbp.run(commandeBoot,shell=True, check=True)
    
    except sbp.CalledProcessError as ex:
        print(f"❌ Erreur ❌ de le l'exécution de : {ex}")
    
    sbp.run(["diskutil", "eject", "/dev/"+Identifiant], check=True)    
     
    await asy.sleep(2)
    print("✅ c'est bon vous pouvez éteindre votre machine.")
    
        
asy.run(main())