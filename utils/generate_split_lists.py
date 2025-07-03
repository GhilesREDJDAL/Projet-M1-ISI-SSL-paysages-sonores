import os
import argparse
import random
from sklearn.model_selection import train_test_split

def generate_file_lists(data_folder_path, output_train, output_val, base_path_prefix, test_size=0.1, random_state=42, max_files=-1):
    if not os.path.isdir(data_folder_path):
        raise FileNotFoundError(f"Le dossier '{data_folder_path}' est introuvable.")

    all_files = [
        os.path.join(data_folder_path, f)
        for f in os.listdir(data_folder_path)
        if f.endswith('.flac') or f.endswith('.wav')
    ]

    if not all_files:
        raise ValueError(f"Aucun fichier .flac trouvé dans le dossier '{data_folder_path}'.")

    # Optionally limit to max_files
    if max_files > 0:
        if max_files > len(all_files):
            print(f"⚠️ max_files ({max_files}) > total files ({len(all_files)}), utilisation de tous les fichiers disponibles.")
        else:
            random.seed(random_state)
            all_files = random.sample(all_files, max_files)

    train_files, val_files = train_test_split(all_files, test_size=test_size, random_state=random_state)

    with open(output_train, 'w') as f_train:
        for file in sorted(train_files):
            f_train.write(os.path.join(base_path_prefix, file) + '\n')

    with open(output_val, 'w') as f_val:
        for file in sorted(val_files):
            f_val.write(os.path.join(base_path_prefix, file) + '\n')

    print(f"Fichiers générés :\n- {output_train} ({len(train_files)} fichiers)\n- {output_val} ({len(val_files)} fichiers)")
    print(f"Total de fichiers .flac traités : {len(all_files)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Générer les listes de fichiers .flac pour train/val à partir d’un dossier donné.")

    parser.add_argument('--data_folder', type=str, required=True, help="Dossier contenant les fichiers .flac (ex: sliced_3s_ffmpeg)")
    parser.add_argument('--output_train', type=str, required=True, help="Chemin du fichier texte de sortie pour l'entraînement")
    parser.add_argument('--output_val', type=str, required=True, help="Chemin du fichier texte de sortie pour la validation")
    parser.add_argument('--base_prefix', type=str, default="/home/m1projetisi", help="Préfixe à ajouter aux chemins des fichiers (défaut: /home/m1projetisi)")
    parser.add_argument('--test_size', type=float, default=0.1, help="Taille du set de validation (ex: 0.1 pour 10%%)")
    parser.add_argument('--max_files', type=int, default=-1, help="Nombre maximum de fichiers à traiter (défaut: tous)")

    args = parser.parse_args()

    generate_file_lists(
        data_folder_path=args.data_folder,
        output_train=args.output_train,
        output_val=args.output_val,
        base_path_prefix=args.base_prefix,
        test_size=args.test_size,
        max_files=args.max_files
    )