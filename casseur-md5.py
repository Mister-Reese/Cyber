#-°- MrReese -°-
#coding:utf8

from ntpath import join #Bibliothèques ou modules ici join pour joindre des variable sans avoir à changer leur types
import string           #Pour les chaines de caractères
import sys              #Pour ce qui est liés aux opérations systèmes
import time             #Pour ce qui est liés aux opérations temporelles
import hashlib          #Pour les fonctions de hashages
import argparse         #Pour gérer les arguments liés aux script ou programme final        

#Fonction de crackage de mot de passe par dictionnaire (fichier)
def crack_dict(md5, file):
    try:                                                                                #On commence la gestion des erreurs avec un try
        trouve = False                                                                  # initialisation de la variable trouve à faux
        ofile = open(file, "r")                                                         #On ouvre en lecture le fichier fourni par l'utilisateur
        for mot in ofile.readlines():                                                   #On créer une boucle pour lire les mots du fichier dictionnaire
            mot = mot.strip("\n")                                                       #On supprime les eventuelles espaces des chaines de caractères
            hashmd5 = hashlib.md5(mot.encode("utf8")).hexdigest()                       #On initialise une variable avec le mot actuel du fichier qu'on chiffre md5
            if hashmd5 == md5:                                                          # On créé une condition pour savoir si le mot du fichier correspond au md5 fourni par l'utilisateur 
                print("Mot de passe trouvé : " + str(mot) + " (" + hashmd5 + ")")       #Si oui on print le mot de passe trouvé et la variable trouve passe à True(Vrai)  
                trouve = True
                ofile.close()                                                           #Et on ferme le fichier
        if not trouve:                                                                  #Sinon, le mot de passe n'est pas trouvé dans le fichier
            print("Mot de passe non trouvé :(")                                         #On print la réponse négative
        ofile.close()                                                                   #Et on ferme aussi le fichier
    except FileNotFoundError:                                                           #On récupère l'erreur si on ne trouve pas le fichier
        print("Erreur ; nom de dossier ou fichier introuvable !")                       #On print 
        sys.exit(1)                                                                     #On quitte avec un code de sortie
    except Exception as err:                                                            #on récupère les autres erreurs
        print("Erreur : " + str(err))
        sys.exit(2)

def crack_incr(md5, length, currpass=[]):                               #fonction recursive, une sorte de brute force par incrémentation
                                                                        #avec ceque j'ai ecris au dessus vous devriez comprendre facilement cette fonction, elle est plus simple
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

        
#Ici on initialise les différents arguments que l'on souhaite add au programme 
parser = argparse.ArgumentParser(description="Description du programme qui s'affichera ensuite")
parser.add_argument("-f", "--file", dest="file", help="Chemin du fichier voulu", required=False)       #Ajoute un ou des arguments à une variable "-f, --file" dest=variable qui va contenir le fichier ou le chemin vers le fichier
parser.add_argument("-g", "--gen", dest="gen", help="Genère un hash de mot de passe md5", required=False) # C'est assez explicite
parser.add_argument("-md5", dest="md5", help="Mot de passe hashé (MD5)", required=False)
parser.add_argument("-l", dest="plength", help="Longueur du Mot de passe)", required=False, type=int)

args = parser.parse_args()  # onrécupère les args dans une variable pour les traiter plus facilement par lasuite

debut = time.time()         # on peut initialiser une variable temporelle pour calculer le temps que le programmemets à trouver le mot de passe

if args.gen:                #Pour éviter de détailler la logique des conditions si après disons que j'aai fais au mieux pour que tous lesarguments disponibles n'entre pas en conflit, exemple lrosque je veux généré un md5 je vais pas en cracker un en même temps
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
