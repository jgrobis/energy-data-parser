import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
import tkinter.filedialog as fd

t = np.arange(1, 25)

class DataExtractor:
    def __init__(self, root):
        self.root = root
        self.file_path = tk.StringVar()
        self.e_oddana = np.array([])
        self.e_pobrana = np.array([])
        self.e_bilans = np.array([])
        self.create_widgets()
    
    def create_widgets(self):
        tk.Label(self.root, text="Enter file path:").grid(row=0, column=0, padx=10, pady=10)
        e = tk.Entry(self.root, textvariable=self.file_path)
        e.grid(row=0, column=1, padx=3, pady=3) #side='left', fill='x',, expand=True
        
        tk.Button(self.root, text="Choose File", command=self.choose_file).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(self.root, text="Extract Data", command=self.extract_data).grid(row=1, column=1, padx=5, pady=5)

    def choose_file(self):
        # Open a file dialog and get the selected file's path
        file_path = fd.askopenfilename()
        self.file_path.set(file_path)
    
    def extract_data(self):
        # Load data from CSV file
        df = pd.read_csv(self.file_path.get(), delimiter=";", decimal=",")

        # Get indices of rows containing certain values in column 2
        first_ocp_e_oddana_df = df[df.iloc[:, 2] == "En.Czynna Oddana"].index[0]
        last_ocp_e_oddana_df = df[df.iloc[:, 2] == "En.Czynna Oddana"].index[-1]
        first_ocp_e_pobrana_df = df[df.iloc[:, 2] == "En.Czynna Pobrana"].index[0]
        last_ocp_e_pobrana_df = df[df.iloc[:, 2] == "En.Czynna Pobrana"].index[-1]
        first_ocp_e_bilans_df = df[df.iloc[:, 2] == "En. Czynna zbilansowana"].index[0]
        last_ocp_e_bilans_df = df[df.iloc[:, 2] == "En. Czynna zbilansowana"].index[-1]

        # Extract relevant data from dataframe
        e_oddana_df = df.iloc[first_ocp_e_oddana_df:last_ocp_e_oddana_df, 3:27]
        e_pobrana_df = df.iloc[first_ocp_e_pobrana_df:last_ocp_e_pobrana_df, 3:27]
        e_bilans_df = df.iloc[first_ocp_e_bilans_df:last_ocp_e_bilans_df, 3:27]

        # Convert dataframes to numpy arrays and transpose them
        e_oddana_TT = np.array(e_oddana_df)
        self.e_oddana = e_oddana_TT.T
        e_pobrana_TT = np.array(e_pobrana_df)
        self.e_pobrana = e_pobrana_TT.T
        e_bilans_TT = np.array(e_bilans_df)
        self.e_bilans = e_bilans_TT.T

        tk.Label(self.root, text="Data extracted successfully.").grid(row=2, column=1, padx=1, pady=1)

class StatisticsCalculator:
    def __init__(self, root, data, e_oddana, e_pobrana):
        self.root = root
        self.data = data
        self.e_oddana = e_oddana
        self.e_pobrana = e_pobrana
        self.wyw = 0
        self.create_widgets()
        #frame = tk.Frame(self.root)
        #frame.grid(row=3 column=0, padx=10, pady=10)
        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear)
        self.clear_button.grid(row=7, column=0, padx=5, pady=5)#(side='left', padx=5, pady=5)
        self.close_button = tk.Button(self.root, text="Close", command=self.closegraph)
        self.close_button.grid(row=7, column=2, padx=5, pady=5)#(side='right', padx=5, pady=5)
        #frame = tk.Frame(self.root)
        #frame.grid(row=6, column=0, padx=10, pady=10)()
    
    def create_widgets(self):
        tk.Button(self.root, text="Calculate Statistics", command=self.calculate_statistics).grid(row=7, column=1, padx=5, pady=5)
        self.plot_max_button = tk.Button(self.root, text="Plot Max", command=self.plot_max)
        self.plot_max_button.grid(row=8, column=0, padx=5, pady=5)#(side='left', padx=5, pady=5)
        self.plot_min_button = tk.Button(self.root, text="Plot Min", command=self.plot_min)
        self.plot_min_button.grid(row=8, column=1, padx=5, pady=5)#(side='left', padx=5, pady=5)
        self.plot_mean_button = tk.Button(self.root, text="Plot Mean", command=self.plot_mean)
        self.plot_mean_button.grid(row=8, column=2, padx=5, pady=5)#(side='left', padx=5, pady=5)
    
    def calculate_statistics(self):
        # Calculate maximum, minimum, and mean for each row
        self.data_max = np.max(self.data, axis=1)
        self.data_min = np.min(self.data, axis=1)
        self.data_mean = np.mean(self.data, axis=1)
        
        # Calculate maximum value and its position
        data_max_1 = np.max(self.data_max)
        y_data_max_1 = np.where(self.data_max == data_max_1)[0][0]
        x_data_max_1 = t[y_data_max_1]
        data_min_1 = np.min(self.data_min)
        y_data_min_1 = np.where(self.data_min == data_min_1)[0][0]
        x_data_min_1 = t[y_data_min_1]
        data_mean_1 = np.mean(self.data_mean)
        bilans_energetyczny = 0.8*(np.sum(self.e_oddana) - np.sum(self.e_pobrana))
        #y_data_mean_1 = np.where(self.data_mean == data_mean_1)[0][0]
        #x_data_mean_1 = t[y_data_mean_1]
        
        self.wyw += 2
        tk.Label(self.root, text=f"Max: {data_max_1:.2f}[kWh] at position {x_data_max_1}").grid(row=7+self.wyw, column=0, padx=5, pady=5)
        tk.Label(self.root, text=f"Min: {data_min_1:.2f}[kWh] at position {x_data_min_1}").grid(row=7+self.wyw, column=1, padx=5, pady=5)
        tk.Label(self.root, text=f"Mean: {data_mean_1:.2f}[kWh]").grid(row=7+self.wyw, column=2, padx=5, pady=5)
        tk.Label(self.root, text=f"Energia w zapasie : {bilans_energetyczny:.2f}").grid(row=8+self.wyw, column=1, padx=5, pady=5)
    
    def plot_max(self):
        if not hasattr(self, "data_max"):
            self.calculate_statistics()
        # Plot minimum values
        plt.plot(t, self.data_max)
        plt.ylabel("Moc w [kWh]")
        plt.xlim(1, 24)
        plt.legend()
        plt.show()
    
    def plot_min(self):
        if not hasattr(self, "data_min"):
            self.calculate_statistics()
        # Plot minimum values
        plt.plot(t, self.data_min)
        plt.ylabel("Moc w [kWh]")
        plt.xlim(1, 24)
        plt.legend()
        plt.show()
    
    def plot_mean(self):
        if not hasattr(self, "data_mean"):
            self.calculate_statistics()
        # Plot minimum values
        plt.plot(t, self.data_mean)
        plt.ylabel("Moc w [kWh]")
        plt.xlim(1, 24)
        plt.legend()
        plt.show()

    def clear(self):
        plt.clf()

    def closegraph(self):
        plt.close()

def main():
    root = tk.Tk()
    root.title("Data Extraction and Statistics Calculation")
    
    data_extractor = DataExtractor(root)
    
    def calculate_statistics_callbacke_oddana():
        statistics_calculator = StatisticsCalculator(root, data_extractor.e_oddana, data_extractor.e_oddana, data_extractor.e_pobrana)
    
    tk.Button(root, text="Calculate Statistics for energia oddana", command=calculate_statistics_callbacke_oddana).grid(row=4, column=1, padx=2, pady=2)
    
    def calculate_statistics_callback_e_pobrana():
        statistics_calculator_e_pobrana = StatisticsCalculator(root, data_extractor.e_pobrana, data_extractor.e_oddana, data_extractor.e_pobrana)
    
    tk.Button(root, text="Calculate Statistics for energia pobrana", command=calculate_statistics_callback_e_pobrana).grid(row=5, column=1, padx=2, pady=2)
    
    def calculate_statistics_callback_e_bilans():
        statistics_calculator_e_bilans = StatisticsCalculator(root, data_extractor.e_bilans, data_extractor.e_oddana, data_extractor.e_pobrana)
    
    tk.Button(root, text="Calculate Statistics for energia zbilansowana", command=calculate_statistics_callback_e_bilans).grid(row=6, column=1, padx=2, pady=2)
    
    def exit_program():
        plt.clf()
        plt.close()
        root.destroy()

    tk.Button(root, text="EXIT program", command=exit_program).grid(row=1, column=2, padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
