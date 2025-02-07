# IHS-to-EPL-Converter
IHS-to-EPL Converter can be used to convert IHS' Auditory Brainstem Response (ABR) format to the in-house format of the Eaton-Peabody Laboratory, to be able to analyze the data with the '[ABR Peak Analysis](https://github.com/EPL-Engineering/abr-peak-analysis)' software (compatible with version 1.10.1).

## Features
- Load ASR measurement datasets (CSV files).
- Navigate between trials using arrow keys.
- Manually or automatically adjust the scale.
- Toggle trial status (Accepted ↔ Rejected) using the space bar.
- Remove rejected trials from the dataset.
- Export datasets before or after filtering or classifying.

## Installation
1. Navigate to [Releases](https://github.com/TomNaber/ASR-Inspect/releases).
2. Download the 'ASR Inspect Setup.exe' file.
3. Run the installer.

## Usage
1. Run the application.
2. Load a dataset (CSV exported from PCT software using the 'Reduce' functionality).
3. Navigate trials using arrow keys or enter a trial number.
4. Mark trials as rejected using the space bar.
5. Adjust Y-scale manually or enable auto-scaling.
6. Export the dataset before or after removing rejected trials.

To test the application, you can download a sample dataset:
[Sample Data - Kinder Scientific ASR Assay.csv](https://github.com/thepyottlab/ASR-Inspect/blob/main/Sample%20Data%20-%20Kinder%20Scientific%20ASR%20Assay.csv)

## Keyboard Shortcuts

| Key         | Action                   |
|------------|--------------------------|
| **→ / ←**  | Next/Previous trial    |
| **Space**  | Toggle Accept/Reject     |

## Acknowledgments
This repository was originally developed as part of [The Pyott Lab](https://github.com/thepyottlab/ASR-Inspect).  
Cloned and maintained here for personal portfolio.
