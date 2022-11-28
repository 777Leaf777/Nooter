import pretty_midi
import librosa
import numpy as np
import soundfile as sf
y, sr = librosa.load('noot.wav', sr=8000) # y is a numpy array of the wav file, sr = sample rate
# Load MIDI file into PrettyMIDI object
midi_data = pretty_midi.PrettyMIDI('input.mid')
# Synthesize the resulting MIDI data using sine waves
list_data = []
for instrument in midi_data.instruments:
    if not instrument.is_drum:
        for note in instrument.notes:
            print(note)
            y_shifted = librosa.effects.pitch_shift(y, sr=8000, n_steps=int(note.pitch-75))
            print(y_shifted)
            list_data.append(y_shifted)
            final_data = np.append(list_data, y_shifted)
            print(final_data)
            print(len(list_data))
x = librosa.effects.time_stretch(final_data, rate=2)
sf.write('output.wav', x, sr, subtype='PCM_24')
