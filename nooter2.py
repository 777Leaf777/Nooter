import pretty_midi
import librosa
import numpy as np
import soundfile as sf
y, sr = librosa.load('noot2.wav', sr=8000) # y is a numpy array of the wav file, sr = sample rate
silence, sr2 = librosa.load('silence.wav', sr=8000) # y is a numpy array of the wav file, sr = sample rate
# Load MIDI file into PrettyMIDI object
midi_data = pretty_midi.PrettyMIDI('input.mid')
# Synthesize the resulting MIDI data using sine waves
final_data = []
current_pos = 0
silence_length = 0.51
note_start = 0
for instrument in midi_data.instruments:
    if not instrument.is_drum:
        for note in instrument.notes:
            silence_length = float(current_pos - note_start)*8
            print(silence_length)
            if silence_length <= 0:
                silence_length = 0.01
            note_start = note.start
            note_end = note.end
            print(note_start, note_end)
            silence = librosa.effects.time_stretch(silence, rate=silence_length)
            note_length = float(note_end-note_start)*1.5
            print(note_length, silence_length)
            y_shifted = librosa.effects.pitch_shift(y, sr=8000, n_steps=int(note.pitch-75))
            y_shifted = librosa.effects.time_stretch(y_shifted, rate=note_length)
            current_pos = note_end
            final_data = np.append(final_data, y_shifted)
            final_data = np.append(final_data, silence)
        break
x = librosa.effects.time_stretch(final_data, rate=1)
sf.write('output.wav', x, sr, subtype='PCM_24')
