import torch
from dtokenizer.audio.model.semanticodec_model import SemanticodecTokenizer
import torchaudio

ht = SemanticodecTokenizer('semanticodec_25_035')
code, stuff_for_decode = ht.encode_file('./sample2_22k.wav')
waveform = ht.decode(code)
print(code)
import soundfile as sf

sf.write("output.wav", waveform[0, 0], 16000)
