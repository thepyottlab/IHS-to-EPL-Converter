# IHS-to-EPL-Converter
IHS-to-EPL Converter can be used to convert IHS' Auditory Brainstem Response (ABR) format (confirmed working with SmartEP version 5.54.23) to the in-house format of the Eaton-Peabody Laboratory to be able to analyze the data with the '[ABR Peak Analysis](https://github.com/EPL-Engineering/abr-peak-analysis)' software (compatible with version 1.10.1).

## Features
- Import raw IHS data that was exported from the IHS Peakinfo application and split it into separate files for each ID and each frequency that are compatible with the EPL ABR Peak Analysis software.
- Set highpass and lowpass filter cutoffs.
- Specify filter order.
- Toggle whether the full trial (0-12 ms) is displayed or only the first half of the trial (0-6 ms).
- Supports converting multiple files that were exported with IHS Peakinfo simultaneously.

## Filter characteristics
The filter is a zero-phase second order sections butterworth bandpass filter, which is a maximally flat filter that is more numerically stable than direct-form representations, allowing for better filter performance at higher orders. The filter is applied forward and backward to counteract phase distortion that would be caused by a single pass of filtering. Because of the backward and forward filtering, filter order is doubled, so a filter order of 1 has -12 dB/octave attenuation rather than the default -6 dB/octave attenuation.

## Installation
1. Navigate to [Releases](https://github.com/TomNaber/IHS-to-EPL-Converter/releases).
2. Download the 'IHS-to-EPL Converter Setup.exe' file.
3. Run the installer.

## Usage
1. Export ABR data using IHSPeakInfo.exe (default location C:\IHSPROGS\IHSPeakInfo.exe) and ensure the Extract Raw Data toggle is ticked.
2. Run the IHS-to-EPL Converter application.
3. Press 'Select files' and select the text file export of IHSPeakInfo (multiple files is supported).
4. Set the highpass and lowpass cutoffs for the bandpass filtering.
5. Set the filter order (-12 dB/octave per filter order).
6. Press OK.
7. Open the EPL ABR Peak Analysis software and ensure the Filter type is set to None to prevent double filtering of the ABRs.
8. Load the newly created ABR files into the EPL ABR Peak Analysis software for analysis.

To test the application, you can download a sample dataset:
[Sample Data - Exported IHS SmartEP files.csv](https://github.com/thepyottlab/ASR-Inspect/blob/main/Sample%20Data%20-%20Kinder%20Scientific%20ASR%20Assay.csv)
