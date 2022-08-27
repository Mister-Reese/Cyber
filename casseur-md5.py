#!/usr/bin/env python3
# coding:utf8
from ntpath import join
import string
import sys
import time
import hashlib
import argparse

def crack_dict(md5, file):
    try:
        trouve = False
        ofile = open(file, "r")
        for mot in ofile.readlines():
            mot = mot.strip("\n")
            hashmd5 = hashlib.md5(mot.encode("utf8")).hexdigest()
            if hashmd5 == md5:
                print("Mot de passe trouvé : " + str(mot) + " (" + hashmd5 + ")")
                trouve = True
        if not trouve:
            print("Mot de passe non trouvé :(")
        ofile.close()
    except FileNotFoundError:
        print("Erreur ; nom de dossier ou fichier introuvable !")
        sys.exit(1)
    except Exception as err:
        print("Erreur : " + str(err))
        sys.exit(2)

def crack_incr(md5, length, currpass=[]):                               #fonction recursive
    
    lettres = string.ascii_letters
    try:
        if length >= 1:
            if len(currpass) == 0:
                currpass = ['a' for _ in range(length)]
                crack_incr(md5, length, currpass)
            else:
                for c in lettres:
                    currpass[length - 1] = c
                    
                    if hashlib.md5("".join(currpass).encode("utf8")).hexdigest() == md5:
                        print("Password Founded !! " + "".join(currpass))
                    else:
                        crack_incr(md5, length - 1, currpass)
    except Exception as err:
        print("Erreur : " + str(err))
        sys.exit(2)

parser = argparse.ArgumentParser(description="Description du programme qui s'affichera ensuite")
parser.add_argument("-f", "--file", dest="file", help="Chemin du fichier voulu", required=False)       #Ajoute un ou des arguments "-fB, --forceBrute" dest=variable qui va contenir le fichier ou le chemin du fichier
parser.add_argument("-g", "--gen", dest="gen", help="Genère un hash de mot de passe md5", required=False)
parser.add_argument("-md5", dest="md5", help="Mot de passe hashé (MD5)", required=False)
parser.add_argument("-l", dest="plength", help="Longueur du Mot de passe)", required=False, type=int)

args = parser.parse_args()

debut = time.time()

if args.gen:
    print("[ Le Hash MD5 de " + args.gen + " :" + hashlib.md5(args.gen.encode("utf8")).hexdigest() + " ]")
elif args.md5:
    print("[Crack Du Hash " + args.md5 + "]")        
    if args.file:
        print("Utilisation Du Fichier Dictionnaire " + args.file + "]")
        crack_dict(args.md5, args.file)
    elif args.plength:
        print("Mode incrémentation brute force pour " + str(args.plength) + " lettre(s)")
        crack_incr(args.md5, args.plength)
    elif args.file and args.plength:
        print("Veuillez seulement soit générer un mot de passe(ex: -g) soit cracker un mot de passe (ex: -f, -md5)")    
else:
    print("Veuillez choisir le mode -f ou -l (1 à la fois)")


print("Durée : " + str(time.time() - debut)) 
    

debut = time.time()

print("Durée : " + str(time.time() - debut) + " secondes")