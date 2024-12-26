
# Music Composition with Genetic Algorithm

This project leverages a genetic algorithm to compose music. The application is built using Python and incorporates several libraries to handle MIDI file generation, play music, and provide an interactive UI through Streamlit.

## Features

- **MIDI File Generation**: Generates a sequence of notes based on scales and chord progressions.
- **Genetic Algorithm**: Uses a genetic algorithm to optimize the sequence of notes based on various fitness criteria.
- **Interactive UI**: Allows users to select scales, instruments, and other parameters for music composition.
- **Playback**: Plays the generated MIDI files using Pygame.

## Installation

1. **Clone the Repository**
    ```sh
    git clone https://github.com/yourusername/music-composition-genetic-algorithm.git
    cd music-composition-genetic-algorithm
    ```

2. **Install Dependencies**
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Streamlit App**
    ```sh
    streamlit run app.py
    ```

2. **Select Parameters**
   - Choose the desired instrument, scale, key, and other parameters from the Streamlit interface.

3. **Compose Music**
   - Click on the "Compose Music" button to generate a sequence of notes using the genetic algorithm.
   - View the best sequence of notes and a fitness chart over time.
   - The generated MIDI file will be played automatically.

4. **Stop Music**
   - Click on the "Stop Music" button to stop the playback.

## Parameters

- **Instrument**: Select from a list of MIDI instruments.
- **Scale**: Choose between Major and Minor scales.
- **Key**: Select the key for the chosen scale.
- **Generations**: Number of generations for the genetic algorithm.
- **Population Size**: Size of the population for the genetic algorithm.
- **Sequence Length**: Length of the note sequence.
- **Include Chords**: Option to include chords in the composition.
- **Chord Progression**: Select common chord progressions.
- **Tempo (BPM)**: Set the tempo of the composition.
- **Mutation Rate**: Probability of mutation in the genetic algorithm.

## Example

1. **Select Instrument**: Acoustic Grand Piano
2. **Select Scale**: Major
3. **Select Key**: C
4. **Generations**: 100
5. **Population Size**: 20
6. **Sequence Length**: 32
7. **Include Chords**: Yes
8. **Chord Progression**: I-IV-V
9. **Tempo (BPM)**: 120
10. **Mutation Rate**: 0.1

Click on "Compose Music" to generate and play the composition.

## Dependencies

- `random`
- `mido`
- `streamlit`
- `pygame`

## Author

- **Nipun Patil**
- **Aspiring Data Engineer**
- **NMIMS'26 Computer Engineering Undergrad**
- nipunpatil2004@gmail.com
- [LinkedIn](https://www.linkedin.com/in/nipunpatil/)
