import torch
import torchaudio
import os
import tqdm
from multiprocessing import Process
from decoder.pretrained import WavTokenizer
from encoder.utils import convert_audio

# === CONFIGURATION ===
NUM_GPUS = torch.cuda.device_count()
assert NUM_GPUS > 0, "Aucun GPU disponible !"

# Chemins
AUDIO_DIR = "/home/m1projetisi/data/datasets/nouragues_19-23/2019/Data"
OUTPUT_DIR = "result_tokens_v9"
CONFIG = "WavTokenizer/result/train/train_flac_10sslices_rand3s/lightning_logs/version_9/config.yaml"
MODEL_PATH = "WavTokenizer/result/train/train_flac_10sslices_rand3s/lightning_logs/version_9/checkpoints/last.ckpt"

# === Lister tous les fichiers FLAC ===
file_list = [
    os.path.join(AUDIO_DIR, f)
    for f in sorted(os.listdir(AUDIO_DIR))
    if f.endswith(".flac")
]

# Répartition équilibrée des fichiers
def split_list(lst, n):
    k, m = divmod(len(lst), n)
    return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]

file_sublists = split_list(file_list, NUM_GPUS)

# === Traitement sur un seul GPU ===
def process_files_on_gpu(files, gpu_id):
    device = torch.device(f"cuda:{gpu_id}")
    print(f"🔧 GPU {gpu_id} → {len(files)} fichiers")

    model = WavTokenizer.from_pretrained0802(CONFIG, MODEL_PATH).to(device)
    # Pas de model.eval()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for filepath in tqdm.tqdm(files, desc=f"[GPU {gpu_id}]", position=gpu_id):
        try:
            waveform, sr = torchaudio.load(filepath)
            waveform = convert_audio(waveform, sr, 24000, 1).to(device)
            bandwidth_id = torch.tensor([0]).to(device)

            # Pas de torch.no_grad() si tu veux garder tout en mode train
            _, discrete_code = model.encode_infer(waveform, bandwidth_id=bandwidth_id)

            filename = os.path.basename(filepath).replace(".flac", ".pt")
            output_path = os.path.join(OUTPUT_DIR, filename)
            torch.save(discrete_code.cpu(), output_path)

        except Exception as e:
            print(f"[GPU {gpu_id}] Erreur fichier {filepath} : {e}")

# === Lancer les processus ===
if __name__ == "__main__":
    processes = []

    for gpu_id in range(NUM_GPUS):
        p = Process(target=process_files_on_gpu, args=(file_sublists[gpu_id], gpu_id))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    print("Traitement terminé sur tous les GPUs.")
