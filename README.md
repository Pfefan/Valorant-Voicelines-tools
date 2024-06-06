# Valorant Voice lines Tools

This repository contains two Python scripts that can be used to download and merge voice lines from Valorant agents.

## vldownloader.py

This script downloads voice lines of a specified Valorant agent. These voice lines are downloaded from the Valorant Fandom website.

### Usage

```bash
python vldownloader.py <output_path> <agent_name>
```

- `<output_path>`: The directory where the downloaded voice lines will be saved.
- `<agent_name>`: The name of the Valorant agent whose voice lines you want to download.

## audiomerger.py

This script merges audio files from a specified directory into a single audio file.

### Usage

```bash
python audiomerger.py <input_path> <output_path> --filename <filename>
```

- `<input_path>`: The directory containing the audio files to be merged.
- `<output_path>`: The directory where the merged audio file will be saved.
- `<filename>`: The name of the merged audio file (optional, default is "merged_audio").
