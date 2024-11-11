import tkinter as tk
from tkinter import filedialog, messagebox
import librosa as lb
import numpy as np
from scipy.spatial.distance import cosine
import os

def extract_empreinte(audio, taille_fenetre=2048, pas_saut=512):
    signal, _ = lb.load(audio)
    stft = np.abs(lb.stft(signal, n_fft=taille_fenetre, hop_length=pas_saut))
    fingerprint = np.mean(stft, axis=1)
    return fingerprint

def comparer_empreintesOneVSOne(empreinte1, empreinte2, margeerreur=0.01):
    min_len = min(len(empreinte1), len(empreinte2))
    empreinte1, empreinte2 = empreinte1[:min_len], empreinte2[:min_len]
    distance = cosine(empreinte1, empreinte2)
    return distance < margeerreur

def comparer_empreintesData(empreinte_choisie, dossier_base, marge_erreur=0.01):
    for racine, _, fichiers in os.walk(dossier_base):
        for fichier in fichiers:
            if fichier.endswith(('.wav', '.mp3')):
                chemin_fichier = os.path.join(racine, fichier)
                empreinte_fichier = extract_empreinte(chemin_fichier)
                min_len = min(len(empreinte_choisie), len(empreinte_fichier))
                empreinte_choisie, empreinte_fichier = empreinte_choisie[:min_len], empreinte_fichier[:min_len]
                distance = cosine(empreinte_choisie, empreinte_fichier)
                if distance < marge_erreur:
                    return chemin_fichier
    return None

def load_file_and_compare():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])
    if file_path:
        empreinte = extract_empreinte(file_path)
        dossier_base = "chemin_vers_votre_dossier"  # Remplissez le chemin vers votre dossier de musique
        fichier_similaire = comparer_empreintesData(empreinte, dossier_base)
        if fichier_similaire:
            nom_fichier = os.path.basename(fichier_similaire)
            messagebox.showinfo("Résultat", f"Musique similaire trouvée : {nom_fichier}")
        else:
            messagebox.showinfo("Résultat", "Aucune musique similaire trouvée dans la base de données.")

# Créer la fenêtre principale
root = tk.Tk()
root.title("Reconnaissance Audio")
root.geometry("400x400")
root.configure(bg="#f0f0f0")  # Couleur de fond agréable

# Créer un cadre pour l'organisation
frame = tk.Frame(root, bg="white", bd=2, relief=tk.GROOVE)
frame.place(relx=0.5, rely=0.5, anchor='center', width=350, height=300)

# Ajouter un titre
title_label = tk.Label(frame, text="Reconnaître une chanson", font=("Helvetica", 18), bg="white", fg="#333")
title_label.pack(pady=10)

# Créer un bouton pour charger un fichier audio
load_button = tk.Button(frame, text="Charger une chanson", command=load_file_and_compare,
                        font=("Helvetica", 14), bg="#1DB954", fg="white", padx=20, pady=10)
load_button.pack(pady=20)

# Créer un bouton pour quitter l'application
quit_button = tk.Button(frame, text="Quitter", command=root.quit,
                        font=("Helvetica", 14), bg="#FF4500", fg="white", padx=20, pady=10)
quit_button.pack(pady=10)

# Lancer l'interface
root.mainloop()