import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np
import tempfile

def spectogram(file_path):
    try:
        y, sr = librosa.load(file_path, sr=None)
        S = librosa.feature.melspectrogram(y=y, sr=sr)
        S_DB = librosa.power_to_db(S, ref=np.max)

        fig, ax = plt.subplots(figsize=(6, 4))
        librosa.display.specshow(S_DB, sr=sr, x_axis='time', y_axis='mel', ax=ax)
        ax.set(title='Mel-frequency spectrogram')
        ax.label_outer()

        # Simpan ke file temporer PNG
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        fig.savefig(temp_file.name, bbox_inches='tight', pad_inches=0.1)
        plt.close(fig)

        return temp_file.name
    except Exception as e:
        print("Error generating spectrogram:", e)
        return None
