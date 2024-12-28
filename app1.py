import random
import mido
from mido import MidiFile, MidiTrack, Message
import streamlit as st
import os

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

# Function to generate MIDI notes sequence and save it to a file
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

# Function to generate chords based on progression
def generate_chords(possible_notes, progression):
    chords = []

    for degree in progression:
        root_note = possible_notes[degree]
        chord = [root_note, root_note + 4, root_note + 7]
        chords.append(chord)
    return chords

# Fitness Function for the Genetic Algorithm
def fitness(sequence, use_chords, progression):
    unique_notes = len(set(sequence))
    melodic_contour_score = sum(abs(sequence[i] - sequence[i - 1]) for i in range(1, len(sequence)))
    rhythmic_variance_score = len(set([random.choice([0.25, 0.5, 1.0, 1.5]) for _ in sequence]))
    
    if use_chords:
        chord_score = sum(1 for i in range(len(sequence)) if (sequence[i] % 12) in progression)
    else:
        chord_score = 0

    total_fitness = unique_notes + rhythmic_variance_score - melodic_contour_score + chord_score
    return total_fitness

# Genetic Algorithm
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

        parents = population[:population_size // 2]
        offspring = []
        for _ in range(population_size // 2):
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            child = crossover(parent1, parent2)
            offspring.append(child)

        for child in offspring:
            if random.random() < mutation_rate:
                child[random.randint(0, sequence_length - 1)] = random.choice(possible_notes)

        population = parents + offspring

    return population[0], best_fitness_over_time

# Crossover Function
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child

# Streamlit UI
st.title("🎶 Music Composition with Genetic Algorithm 🎶")

# Instrument selection
instruments = {
    "Acoustic Grand Piano": 0, "Electric Piano 1": 4, "Electric Guitar (clean)": 27,
    "Violin": 40, "Cello": 42, "Trumpet": 56, "Flute": 73
}

selected_instrument = st.selectbox("🎻 Select Instrument", list(instruments.keys()))

# Scale and Key selection
selected_scale = st.selectbox("🎹 Select Scale", list(SCALES.keys()))
selected_key = st.selectbox("🎸 Select Key", list(SCALES[selected_scale].keys()))

available_notes = SCALES[selected_scale][selected_key]

# Genetic Algorithm parameters
generations = st.slider("🧬 Generations", min_value=10, max_value=500, value=100)
population_size = st.slider("👨‍👩‍👧‍👦 Population Size", min_value=10, max_value=50, value=20)
sequence_length = st.slider("📏 Sequence Length", min_value=8, max_value=64, value=32)
use_chords = st.checkbox("🎼 Include Chords")
progression_choice = st.selectbox("🎶 Select Chord Progression (optional)", ["None"] + list(COMMON_PROGRESSIONS.keys()))
selected_progression = COMMON_PROGRESSIONS.get(progression_choice) if progression_choice != "None" else None
tempo = st.slider("🎵 Tempo (BPM)", min_value=40, max_value=200, value=120)
mutation_rate = st.slider("🔄 Mutation Rate", min_value=0.01, max_value=1.0, value=0.1)

# Function to play MIDI using JavaScript (MIDI.js)
def play_midi_with_js(filename):
    midi_file_path = os.path.join(os.getcwd(), filename)
    
    midi_js = f"""
    <script src="https://cdn.jsdelivr.net/npm/midi.js"></script>
    <script type="text/javascript">
        var midi = new MIDI();
        midi.loadPlugin({
            onsuccess: function() {{
                midi.loadFile("{midi_file_path}", function() {{
                    midi.play();
                }});
            }}
        });
    </script>
    """
    st.components.v1.html(midi_js, height=300)

# Generate music button
if st.button("📝 Compose Music"):
    st.balloons()
    best_sequence, fitness_over_time = genetic_algorithm(generations, population_size, sequence_length, available_notes, use_chords, selected_progression, mutation_rate)

    st.write("✨ Best sequence of notes (MIDI):", best_sequence)

    st.line_chart(fitness_over_time)

    # Save MIDI file
    _midi(best_sequence, filename="genetic_music.mid", tempo=tempo, instrument=instruments[selected_instrument])

    # Play MIDI using JavaScript
    play_midi_with_js("genetic_music.mid")
