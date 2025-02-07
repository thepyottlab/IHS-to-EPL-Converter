# IHS-to-EPL Converter
<p align="center">
  <img src="https://github.com/user-attachments/assets/a0c97d8a-1d67-4a06-8be8-6e7f5fee1632" width="753" height="663">
</p>
IHS-to-EPL Converter is a tool designed to convert Intelligent Hearing Systems (IHS) Auditory Brainstem Response (ABR) data (tested with SmartEP version 5.54.23) into the Eaton-Peabody Laboratory's in-house format. This conversion enables compatibility with the [ABR Peak Analysis](https://github.com/EPL-Engineering/abr-peak-analysis) software (version 1.10.1).

## Features
- Imports raw IHS data exported from IHSPeakInfo.
- Splits data into separate files per ID and frequency for EPL ABR Peak Analysis compatibility.
- Configurable highpass and lowpass filter cutoffs.
- Adjustable filter order.
- Option to display either the full trial or only the first half – i.e., only show the first 6 ms rather than the full 12 ms when using a 25 µs sampling period. The full ABR is always used for filtering.
- Batch processing support for multiple files exported from IHSPeakInfo.

## Filter Characteristics
The converter applies a zero-phase second-order sections Butterworth bandpass filter, which provides a maximally flat frequency response while ensuring numerical stability. The filter is applied forward and backward to eliminate phase distortion. Due to this bidirectional filtering, the effective filter order is doubled, resulting in an attenuation of -12 dB/octave per filter order rather than the default -6 dB/octave.

## Installation
1. Go to the [Releases](https://github.com/TomNaber/IHS-to-EPL-Converter/releases) page.
2. Download the `IHS-to-EPL Converter Setup.exe` file.
3. Run the installer and follow the on-screen instructions.

## Usage
1. Export ABR data using `IHSPeakInfo.exe` (default location: `C:\IHSPROGS\IHSPeakInfo.exe`). Ensure the 'Extract Raw Data' option is enabled.
2. Open the IHS-to-EPL Converter application.
3. Click 'Select files' and choose the exported text file(s) from IHSPeakInfo.
4. Set the highpass and lowpass cutoffs for bandpass filtering.
5. Specify the filter order (-12 dB/octave per order).
6. Click 'OK' to process the files.
7. Open the EPL ABR Peak Analysis software and set 'Filter type' to 'None' to prevent double filtering.
8. Load the converted ABR files into EPL ABR Peak Analysis for analysis.

### Sample Dataset
To test the application, download a sample dataset:
[Sample Data - IHSPeakInfo Export.TXT](https://github.com/thepyottlab/IHS-to-EPL-Converter/blob/main/Sample%20Data%20-%20IHSPeakInfo%20Export.TXT)
