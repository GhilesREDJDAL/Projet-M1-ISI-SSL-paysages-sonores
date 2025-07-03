import os
import shutil
import librosa
from tqdm import tqdm # For loading bar

# === PARAMÈTRES ===
# Change folders/files accordingly
audio_dir = "downsampled_24kHz_wavs_3s_per_10s_chunk/" 
problematic_dir = os.path.join(audio_dir, "problematic_files_backup/")
txt_files = ["train_wav.txt", "val_wav.txt"]
target_duration = 3.0  # seconds
duration_tolerance = 0.01

# === CRÉATION DOSSIER SAUVEGARDE ===
os.makedirs(problematic_dir, exist_ok=True)

audio_extensions = (".wav", ".flac", ".mp3") # Accepted formats by WavTokenizer

def is_audio_file(filename):
    return filename.lower().endswith(audio_extensions)

def move_file(src_path, dest_folder):
    filename = os.path.basename(src_path)
    dest_path = os.path.join(dest_folder, filename)
    base, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(dest_path):
        dest_path = os.path.join(dest_folder, f"{base}_{counter}{ext}")
        counter += 1
    shutil.move(src_path, dest_path)

def check_and_move_files(directory):
    load_errors = []
    zero_length_files = []
    wrong_duration_files = []

    all_files = [
        os.path.join(root, fname)
        for root, _, files in os.walk(directory)
        for fname in files
        if is_audio_file(fname)
    ]

    for file_path in tqdm(all_files, desc="Checking audio files"):
        try:
            y, sr = librosa.load(file_path, sr=None)
            duration = librosa.get_duration(y=y, sr=sr)

            if y.size == 0:
                zero_length_files.append(file_path)
                move_file(file_path, problematic_dir)
            elif not (target_duration - duration_tolerance <= duration <= target_duration + duration_tolerance):
                wrong_duration_files.append(file_path)
                move_file(file_path, problematic_dir)
        except Exception as e:
            load_errors.append((file_path, str(e)))
            move_file(file_path, problematic_dir)

    print(f"\nTotal audio files checked: {len(all_files)}")
    print(f"Zero-length files moved: {len(zero_length_files)}")
    print(f"Wrong-duration files moved: {len(wrong_duration_files)}")
    print(f"Files with load errors moved: {len(load_errors)}")

    return zero_length_files, wrong_duration_files, load_errors

def get_bad_files_from_folder(bad_folder):
    return set(os.listdir(bad_folder))

def remove_bad_files_from_txt(bad_folder, txt_file_paths):
    bad_files = get_bad_files_from_folder(bad_folder)

    for txt_path in txt_file_paths:
        with open(txt_path, 'r') as f:
            lines = f.readlines()

        cleaned_lines = []
        removed_count = 0
        for line in lines:
            filename = os.path.basename(line.strip())
            if filename in bad_files:
                removed_count += 1
                continue
            cleaned_lines.append(line)

        with open(txt_path, 'w') as f:
            f.writelines(cleaned_lines)

        print(f"Cleaned {txt_path}: removed {removed_count} lines.")

# === EXÉCUTION ===
zero_files, wrong_duration_files, error_files = check_and_move_files(audio_dir)
remove_bad_files_from_txt(problematic_dir, txt_files)
