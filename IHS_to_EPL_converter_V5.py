import pandas as pd
import numpy as np
from datetime import datetime
import os
import tkinter as tk
from tkinter import filedialog, scrolledtext
from scipy.signal import butter, sosfiltfilt
import threading
import sys
import io
import time

class ConsoleRedirector(io.StringIO):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    def write(self, message):
        self.widget.insert(tk.END, message)
        self.widget.see(tk.END)

    def flush(self):
        pass

def select_files():
    global file_paths
    file_paths = filedialog.askopenfilenames(title="Select dataset",
                                             filetypes=[("txt files", "*.txt")])
    listbox.delete(0, tk.END)
    for file in file_paths:
        listbox.insert(tk.END, file)

def on_ok():
    global highpass, lowpass, order, full_trials
    highpass = float(highpass_entry.get())
    lowpass = float(lowpass_entry.get())
    order = int(order_entry.get())
    full_trials = full_trials_var.get()

    threading.Thread(target=main, args=(file_paths,),
                     daemon=True).start()

def create_gui():
    global listbox, highpass_entry, lowpass_entry, order_entry, root, full_trials_var, console_output

    root = tk.Tk()
    root.title("IHS-to-EPL Converter")
    root.iconbitmap("icon.ico")

    tk.Label(root, text="Highpass cutoff").grid(row=0, column=0)
    highpass_entry = tk.Entry(root)
    highpass_entry.grid(row=0, column=1)
    highpass_entry.insert(0, "300")

    tk.Label(root, text="Lowpass cutoff").grid(row=1, column=0)
    lowpass_entry = tk.Entry(root)
    lowpass_entry.grid(row=1, column=1)
    lowpass_entry.insert(0, "3000")

    tk.Label(root, text="Filter order (-12 dB/octave/order)").grid(row=2,
                                                                 column=0)
    order_entry = tk.Entry(root)
    order_entry.grid(row=2, column=1)
    order_entry.insert(0, "2")

    full_trials_var = tk.BooleanVar()
    full_trials_toggle = tk.Checkbutton(root, text="Show full trials",
                                        variable=full_trials_var)
    full_trials_toggle.grid(row=3, column=0, columnspan=2)

    select_button = tk.Button(root, text="Select files", command=select_files)
    select_button.grid(row=4, column=0, columnspan=2)

    listbox = tk.Listbox(root, width=50, height=10)
    listbox.grid(row=5, column=0, columnspan=2)

    ok_button = tk.Button(root, text="OK", command=on_ok)
    ok_button.grid(row=6, column=0, columnspan=2)

    tk.Label(root, text="").grid(row=7, column=0, columnspan=2)
    console_output = scrolledtext.ScrolledText(root, width=70, height=10,
                                               state='normal')
    console_output.grid(row=8, column=0, columnspan=2)

    sys.stdout = ConsoleRedirector(console_output)
    sys.stderr = ConsoleRedirector(console_output)

    root.mainloop()

class Record:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.data = []

def read_txt(file_path):
    with open(file_path, 'r') as f:
        lines = [line.strip().split('|' if '|' in line else '\t') for line in f]

    df = pd.DataFrame([line + [None] * (max(len(l) for l in lines) - len(line)) for line in lines])
    df.columns = [f'Unnamed {i+1}' if not h or h.isspace() else h for i, h in enumerate(df.iloc[0])]
    return df[1:].reset_index(drop=True)

def process_df(df):
    df.columns = df.columns.str.replace('.', '_', regex=False)
    df = df.rename(columns={'Intesity': 'Intensity'}) if 'Intesity' in df.columns else df
    df['StimFreq'] = df['StimFreq'].replace(['--', ' -- '], '0')
    return df.drop_duplicates(subset=['SystemID', 'StimFreq', 'Intensity'], keep='last').reset_index(drop=True)

def create_records(df):
    named_cols = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    unnamed_cols = df.loc[:, df.columns.str.contains('^Unnamed')]
    records = []
    for i, row in named_cols.iterrows():
        rec = Record(**row.to_dict())
        if 'Raw Data (uV):' in row and not pd.isna(row['Raw Data (uV):']):
            rec.data.append(row['Raw Data (uV):'])
        if i < len(unnamed_cols):
            rec.data.extend(unnamed_cols.iloc[i].values)
        records.append(rec)
    return records

def group_records(records):
    grouped = {}
    for rec in records:
        system_id = getattr(rec, 'SystemID', None)
        stim_freq = getattr(rec, 'StimFreq', None)
        if system_id and stim_freq:
            grouped.setdefault(system_id, {}).setdefault(stim_freq, []).append(rec)
    return grouped

def bandpass_filter(data, low, high, fs, order):
    sos = butter(order, [low / (0.5 * fs), high / (0.5 * fs)], btype='bandpass', output='sos')
    return sosfiltfilt(sos, data)

def main(file_paths):
    template_path = r"EPL Template File"
    for file in file_paths:
        df = read_txt(file)
        if df is not None:
            df = process_df(df)
            records = create_records(df)
            grouped_records = group_records(records)

            for system_id, stim_freq_dict in grouped_records.items():
                for stim_freq, recs in stim_freq_dict.items():
                    with open(template_path, 'r') as template_file:
                        template = template_file.read()

                    rec_df = pd.DataFrame([r.__dict__ for r in recs])
                    rec_df['Intensity'] = pd.to_numeric(rec_df['Intensity'], errors='coerce')
                    rec_df = rec_df.sort_values(by='Intensity').reset_index(drop=True)

                    rec_date = datetime.strptime(rec_df['Rec_Date'].iloc[0], '%Y-%m-%d').strftime('%d/%m/%Y')
                    rec_time = datetime.strptime(rec_df['Rec_Time'].iloc[0], "%H:%M:%S").strftime("%I:%M %p")
                    freq = str(float(rec_df['StimFreq'].iloc[0]) / 1000) if rec_df['StimFreq'].iloc[0] != '0' else 'Clicks'
                    freq_name = f"{freq} kHz" if freq != 'Clicks' else freq
                    rec_name = f"{rec_df['SystemID'].iloc[0]} {freq_name}"
                    print(f"Converting {rec_name} to an Eaton-Peabody file")
                    sweeps = str(rec_df['Sweeps'].max())
                    rate = str(rec_df['Rate'].iloc[0])
                    sample_rate = str(rec_df['SamplingRate'].iloc[0])
                    intensities = ';'.join(map(str, rec_df['Intensity'].unique()))

                    raw_data = pd.DataFrame(rec_df['data'].tolist()).transpose().dropna(how='all', axis=0)
                    raw_data = raw_data.apply(pd.to_numeric, errors='coerce')

                    for col in raw_data.columns:
                        fs = 1000000 / float(sample_rate)
                        raw_data[col] = bandpass_filter(raw_data[col],
                                                        highpass, lowpass, fs, order)

                    raw_data = raw_data[int(len(raw_data) / 2):]
                    if full_trials:
                        raw_data = pd.concat([raw_data, raw_data])
                    data_str = raw_data.to_csv(sep='\t', index=False, header=False, lineterminator='\n')

                    template = template.replace('4/6/2007', rec_date)
                    template = template.replace('8:03 AM', rec_time)
                    template = template.replace('16.00', str(float(freq.split(' ')[0]) if freq != 'Clicks' else 0))
                    template = template.replace('512', sweeps)
                    template = template.replace('/sec): 40', f'/sec): {rate}')
                    template = template.replace('): 10', f'): {sample_rate}')
                    template = template.replace('10;15;20;25;30;35;40;45;50;60;70;80;', intensities)

                    if (start_index := template.find('-0.052685')) != -1:
                        template = template[:start_index] + data_str

                    with open(os.path.join(os.path.dirname(file), rec_name), 'w') as out_file:
                        out_file.write(template)

    print("Done! You can close this window now or select other files.")


if __name__ == "__main__":
    create_gui()
