import random
import mido
from mido import MidiFile, MidiTrack, Message
import streamlit as st
import os
from midi2audio import FluidSynth  # To convert MIDI to WAV

# Initialize FluidSynth
synth = FluidSynth()

# Scales
SCALES = {
    "Major": {
        "C": [60, 62, 64, 65, 67, 69, 71, 72],
        "D": [62, 64, 66, 67, 69, 71, 73, 74],
        "E": [64, 66, 68, 69, 71, 73, 75, 76],
        "F": [65, 67, 69, 70, 72, 74, 76, 77],
        "G": [67, 69, 71, 72, 74, 76, 78, 79],
        "A": [69, 71, 73, 74, 76, 78, 80, 81],
        "B": [71, 73, 75, 76, 78, 80, 82, 83],
    },
    "Minor": {
        "C": [60, 62, 63, 65, 67, 68, 70, 72],
        "D": [62, 64, 65, 67, 69, 70, 72, 74],
        "E": [64, 66, 67, 69, 71, 72, 74, 76],
        "F": [65, 67, 68, 70, 72, 73, 75, 77],
        "G": [67, 69, 70, 72, 74, 75, 77, 79],
        "A": [69, 71, 72, 74, 76, 77, 79, 81],
        "B": [71, 73, 74, 76, 78, 79, 81, 83],
    },
}

# Common chord progressions
COMMON_PROGRESSIONS = {
    "I-IV-V": [0, 3, 4],
    "I-vi-ii-V": [0, 5, 2, 4],
    "ii-V-I": [2, 4, 0],
}

def _midi(notes_sequence, filename="output.mid", tempo=120, instrument=0):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    track.append(Message('program_change', program=instrument))

    microseconds_per_beat = int(60000000 / tempo)
    track.append(mido.MetaMessage('set_tempo', tempo=microseconds_per_beat))

    for note in notes_sequence:
        velocity = random.randint(60, 100)
        track.append(Message('note_on', note=note, velocity=velocity, time=0))

        pause_duration = random.choice([240, 480, 720])
        track.append(Message('note_off', note=note, velocity=velocity, time=pause_duration))

    mid.save(filename)

def generate_chords(possible_notes, progression):
    chords = []

    for degree in progression:
        root_note = possible_notes[degree]
        chord = [root_note, root_note + 4, root_note + 7]
        chords.append(chord)
    return chords

# Fitness Function
def fitness(sequence, use_chords, progression):
    # Encourage unique notes
    unique_notes = len(set(sequence))

    # Smooth transitions (lower melodic jumps)
    melodic_contour_score = sum(abs(sequence[i] - sequence[i - 1]) for i in range(1, len(sequence)))

    # Rhythmic stability
    rhythmic_variance_score = len(set([random.choice([0.25, 0.5, 1.0, 1.5]) for _ in sequence]))

    # chord notes if using chords
    if use_chords:
        chord_score = sum(1 for i in range(len(sequence)) if (sequence[i] % 12) in progression)
    else:
        chord_score = 0

    # total
    total_fitness = unique_notes + rhythmic_variance_score - melodic_contour_score + chord_score
    return total_fitness

def genetic_algorithm(generations, population_size, sequence_length, possible_notes, use_chords, progression, mutation_rate):
    population = []
    for _ in range(population_size):
        if use_chords:
            chords = generate_chords(possible_notes, progression)
            flat_notes = [note for chord in chords for note in chord]
            individual = random.choices(flat_notes, k=sequence_length)
        else:
            individual = random.choices(possible_notes, k=sequence_length)
        population.append(individual)

    best_fitness_over_time = []
    for generation in range(generations):
        population = sorted(population, key=lambda ind: fitness(ind, use_chords, progression), reverse=True)
        best_fitness = fitness(population[0], use_chords, progression)
        best_fitness_over_time.append(best_fitness)

        # Select parents
        parents = population[:population_size // 2]

        # Crossover
        offspring = []
        for _ in range(population_size // 2):
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            child = crossover(parent1, parent2)
            offspring.append(child)

        # Mutation
        for child in offspring:
            if random.random() < mutation_rate:
                child[random.randint(0, sequence_length - 1)] = random.choice(possible_notes)

        # Update population
        population = parents + offspring

    return population[0], best_fitness_over_time

# Crossover Function
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child


# Streamlit UI
st.title("🎶 Music Composition with Genetic Algorithm 🎶")

instruments = {
    "Acoustic Grand Piano": 0, "Bright Acoustic Piano": 1, "Electric Grand Piano": 2, "Honky-Tonk Piano": 3,
    "Electric Piano 1": 4, "Electric Piano 2": 5, "Harpsichord": 6, "Clavinet": 7, "Celesta": 8, "Glockenspiel": 9,
    "Music Box": 10, "Vibraphone": 11, "Marimba": 12, "Xylophone": 13, "Tubular Bells": 14, "Dulcimer": 15,
    "Drawbar Organ": 16, "Percussive Organ": 17, "Rock Organ": 18, "Church Organ": 19, "Reed Organ": 20,
    "Accordion": 21, "Harmonica": 22, "Tango Accordion": 23, "Acoustic Guitar (nylon)": 24, "Acoustic Guitar (steel)": 25,
    "Electric Guitar (jazz)": 26, "Electric Guitar (clean)": 27, "Electric Guitar (muted)": 28, "Overdriven Guitar": 29,
    "Distortion Guitar": 30, "Guitar Harmonics": 31, "Acoustic Bass": 32, "Electric Bass (finger)": 33,
    "Electric Bass (pick)": 34, "Fretless Bass": 35, "Slap Bass 1": 36, "Slap Bass 2": 37, "Synth Bass 1": 38,
    "Synth Bass 2": 39, "Violin": 40, "Viola": 41, "Cello": 42, "Contrabass": 43, "Tremolo Strings": 44,
    "Pizzicato Strings": 45, "Orchestral Harp": 46, "Timpani": 47, "String Ensemble 1": 48, "String Ensemble 2": 49,
    "SynthStrings 1": 50, "SynthStrings 2": 51, "Choir Aahs": 52, "Voice Oohs": 53, "Synth Voice": 54,
    "Orchestra Hit": 55, "Trumpet": 56, "Trombone": 57, "Tuba": 58, "Muted Trumpet": 59, "French Horn": 60,
    "Brass Section": 61, "SynthBrass 1": 62, "SynthBrass 2": 63, "Soprano Sax": 64, "Alto Sax": 65, "Tenor Sax": 66,
    "Baritone Sax": 67, "Oboe": 68, "English Horn": 69, "Bassoon": 70, "Clarinet": 71, "Piccolo": 72,
    "Flute": 73, "Recorder": 74, "Pan Flute": 75, "Blown Bottle": 76, "Shakuhachi": 77, "Whistle": 78,
    "Ocarina": 79, "Lead 1 (square)": 80, "Lead 2 (sawtooth)": 81, "Lead 3 (calliope)": 82, "Lead 4 (chiff)": 83,
    "Lead 5 (charang)": 84, "Lead 6 (voice)": 85, "Lead 7 (fifths)": 86, "Lead 8 (bass + lead)": 87,
    "Pad 1 (new age)": 88, "Pad 2 (warm)": 89, "Pad 3 (polysynth)": 90, "Pad 4 (choir)": 91,
    "Pad 5 (bowed)": 92, "Pad 6 (metallic)": 93, "Pad 7 (halo)": 94, "Pad 8 (sweep)": 95, "FX 1 (rain)": 96,
    "FX 2 (soundtrack)": 97, "FX 3 (crystal)": 98, "FX 4 (atmosphere)": 99, "FX 5 (brightness)": 100,
    "FX 6 (goblins)": 101, "FX 7 (echoes)": 102, "FX 8 (sci-fi)": 103, "Sitar": 104, "Banjo": 105,
    "Shamisen": 106, "Koto": 107, "Kalimba": 108, "Bagpipe": 109, "Fiddle": 110, "Shanai": 111,
    "Tinkle Bell": 112, "Agogo": 113, "Steel Drums": 114, "Woodblock": 115, "Taiko Drum": 116,
    "Melodic Tom": 117, "Synth Drum": 118, "Reverse Cymbal": 119, "Guitar Fret Noise": 120,
    "Breath Noise": 121, "Seashore": 122, "Bird Tweet": 123, "Telephone Ring": 124
}

selected_instrument = st.selectbox("🎻 Select Instrument", list(instruments.keys()))

selected_scale = st.selectbox("🎹 Select Scale", list(SCALES.keys()))
selected_key = st.selectbox("🎸 Select Key", list(SCALES[selected_scale].keys()))

available_notes = SCALES[selected_scale][selected_key]

generations = st.slider("🧬 Generations", min_value=10, max_value=500, value=100)
population_size = st.slider("👨‍👩‍👧‍👦 Population Size", min_value=10, max_value=50, value=20)
sequence_length = st.slider("📏 Sequence Length", min_value=8, max_value=64, value=32)
use_chords = st.checkbox("🎼 Include Chords")
progression_choice = st.selectbox("🎶 Select Chord Progression (optional)", ["None"] + list(COMMON_PROGRESSIONS.keys()))
selected_progression = COMMON_PROGRESSIONS.get(progression_choice) if progression_choice != "None" else None
tempo = st.slider("🎵 Tempo (BPM)", min_value=40, max_value=200, value=120)
mutation_rate = st.slider("🔄 Mutation Rate", min_value=0.01, max_value=1.0, value=0.1)

if st.button("📝 Compose Music"):
    st.balloons()
    best_sequence, fitness_over_time = genetic_algorithm(generations, population_size, sequence_length, available_notes, use_chords, selected_progression, mutation_rate)

    st.write("✨ Best sequence of notes (MIDI):", best_sequence)

    st.line_chart(fitness_over_time)

    _midi(best_sequence, filename="genetic_music.mid", tempo=tempo, instrument=instruments[selected_instrument])

    # Convert MIDI to WAV
    wav_filename = "genetic_music.wav"
    synth.midiToAudio("genetic_music.mid", wav_filename)

    # Play WAV using Streamlit audio
    if os.path.exists(wav_filename):
        with open(wav_filename, "rb") as f:
            st.audio(f.read(), format="audio/wav")
