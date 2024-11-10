# Créé par CYTech Student, le 07/11/2024 en Python 3.7
import librosa as lb
# Charger deux fichiers audio
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import *
import os

#extraction de l'empreinte du son, renvoie l'empreinte
def extract_empreinte(audio, taille_fenetre=2048, pas_saut=512):
    # Charge l'audio spécifié et le convertit en un signal numérique
    signal, hz = lb.load(audio)

    # applique fournier sur le signal,
    #cad : recupere le spectogramme du signal
    stft = np.abs(lb.stft(signal, n_fft=taille_fenetre, hop_length=pas_saut))

    # recupere moyenne des amplitudes de chaque fréquence pour simplifier chaque ligne
    fingerprint = np.mean(stft, axis=1)

    return fingerprint

#audio utilisé pour voir si ça renvoie bien faux pour la comparaisonOneVSOne
audio_exemple = lb.example('trumpet')
fingerprint  = extract_empreinte(audio_exemple)
print("Empreinte audio trompette :")
print(fingerprint)

#audio weeknd1
musique = "The Weeknd.mp3"
print("Empreinte audio de theweek end :")
extracttheweekd1= extract_empreinte(musique)
print(extracttheweekd1)

#audio weeknd2
musique2 = "The Weeknd2.mp3"
print("Empreinte audio de theweek end 2 :")
extracttheweekd2=extract_empreinte(musique2)
print(extracttheweekd2)


#affichage du spectre avec matplotlib
def afficher_spectrogramme(audio, taille_fenetre=2048, pas_saut=512):
    # Charge l'audio
    signal, sr = lb.load(audio)

    # Applique la STFT pour obtenir le spectrogramme
    D = np.abs(lb.stft(signal, n_fft=taille_fenetre, hop_length=pas_saut))

    # Convertir l'amplitude en décibels pour une meilleure visualisation
    DB = lb.amplitude_to_db(D, ref=np.max)

    # Afficher le spectrogramme avec matplotlib
    plt.figure(figsize=(12, 8))
    plt.imshow(DB, aspect='auto', cmap='inferno', origin='lower',
               extent=[0, DB.shape[-1], 0, DB.shape[0]])
    plt.colorbar(format="%+2.0f dB")
    plt.title(f"Spectrogramme de {audio}")
    plt.xlabel('Temps')
    plt.ylabel('Fréquence')
    plt.show()


#compare deux empreintes de son et renvoie vrai si ils sont identiques
def comparer_empreintesOneVSOne(empreinte1, empreinte2, margeerreur=0.01):
    # Ajuster la taille des empreintes pour qu'elles soient identiques
    min_len = min(len(empreinte1), len(empreinte2))
    empreinte1, empreinte2 = empreinte1[:min_len], empreinte2[:min_len]

    # Calculer la distance du cosinus entre les deux vecteurs (plus elle est proche de 0, plus elles sont similaires)
    distance = cosine(empreinte1, empreinte2)

    # Retourne si la distance est inférieure à la tolérance définie
    if (distance<margeerreur):
        return True

    else :
        return False

#compare une musique d'entrée avec tout les fichiers .mp3 et .wav des sous dossiers du dossier choisi
def comparer_empreintesData(empreinte_choisie, dossier_base, marge_erreur=0.01):

    # Parcourt tous les sous-dossiers et fichiers dans le dossier principal
    for racine, _, fichiers in os.walk(dossier_base):
        for fichier in fichiers:
            # Construit le chemin complet du fichier audio
            chemin_fichier = os.path.join(racine, fichier)

            # Vérifie que le fichier est bien un fichier audio (ici, on filtre pour .wav et .mp3)
            if fichier.endswith(('.wav', '.mp3')):
                # Extraction de l'empreinte du fichier dans la base de données
                empreinte_fichier = extract_empreinte(chemin_fichier)

                # Ajuste les longueurs des empreintes pour qu'elles soient identiques
                min_len = min(len(empreinte_choisie), len(empreinte_fichier))
                empreinte_choisie, empreinte_fichier = empreinte_choisie[:min_len], empreinte_fichier[:min_len]

                # Calcule la distance de cosinus entre les deux empreintes
                distance = cosine(empreinte_choisie, empreinte_fichier)

                # Si la distance est inférieure à la marge d'erreur, considère les empreintes comme similaires
                if distance < marge_erreur:
                    nom_fichier = os.path.basename(chemin_fichier)
                    print(f"Correspondance trouvée avec : {nom_fichier} (distance : {distance})")
                    return chemin_fichier  # Retourne le chemin du fichier correspondant

    print("Aucune correspondance trouvée dans le dossier.")
    return None  # Aucun fichier similaire trouvé

# Exemple utilisation affichage spectogramme :
musique = "The Weeknd.mp3"
afficher_spectrogramme(musique)
musique2 = "The Weeknd2.mp3"
afficher_spectrogramme(musique2)
musique3 = lb.example('trumpet')
afficher_spectrogramme(musique3)

#exemple utilisation compare_empreinte :
#compare deux sons similaires
print(comparer_empreintesOneVSOne(extracttheweekd1,extracttheweekd2))
#comparaison de the week end avec trumpet
print(comparer_empreintesOneVSOne(extracttheweekd1,fingerprint))


#exemple1 BDD
# Empreinte de la musique d'entrée
empreinte_entree = extract_empreinte(r"H:\Documents\ING2 CYTECH\ING2-TraitementSignal\Projet Traitement Signal\Data\genres_original\blues\blues.00016.wav")
# Chemin du dossier contenant les empreintes de la base de données
dossier_base = r"H:\Documents\ING2 CYTECH\ING2-TraitementSignal\Projet Traitement Signal\Data\genres_original"
# Appel de la fonction
fichier_similaire = comparer_empreintesData(empreinte_entree, dossier_base)
nom_fichier = os.path.basename(fichier_similaire)
if fichier_similaire:
    print(f"Musique similaire trouvée : {nom_fichier}")
else:
    print("Aucune musique similaire trouvée dans la base de données.")


#exemple2 BDD
empreinte_entree = extract_empreinte("The Weeknd.mp3")
# Chemin du dossier contenant les empreintes de la base de données
dossier_base = r"H:\Documents\ING2 CYTECH\ING2-TraitementSignal\Projet Traitement Signal\Data\genres_original"
# Appel de la fonction
fichier_similaire = comparer_empreintesData(empreinte_entree, dossier_base)
nom_fichier = os.path.basename(fichier_similaire)
if fichier_similaire:
    print(f"Musique similaire trouvée : {nom_fichier}")
else:
    print("Aucune musique similaire trouvée dans la base de données.")

#exemple2 BDD
empreinte_entree = extract_empreinte("The Weeknd.mp3")
# Chemin du dossier contenant les empreintes de la base de données
dossier_base = r"H:\Documents\ING2 CYTECH\ING2-TraitementSignal\Projet Traitement Signal\Data\genres_original"
# Appel de la fonction
fichier_similaire = comparer_empreintesData(empreinte_entree, dossier_base)
nom_fichier = os.path.basename(fichier_similaire)
if fichier_similaire:
    print(f"Musique similaire trouvée : {nom_fichier}")
else:
    print("Aucune musique similaire trouvée dans la base de données.")

#musique = "The Weeknd.mp3"
#afficher_spectrogramme(musique)
#afficher_spectrogramme(fichier_similaire)
