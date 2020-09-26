from pathlib import Path
from statistics import mean
from utils import visualization

def read_val_acc(log_csv_file):

    update_num_list, val_acc_list = [], []
    lines = open(log_csv_file, 'r').readlines()
    for line in lines:
        if len(line) > 3:
            parts = line[:-1].split(',')
            update_num = int(parts[0])
            val_acc = float(parts[1])
            update_num_list.append(update_num)
            val_acc_list.append(val_acc)
    
    return update_num_list, val_acc_list

def average_master_list(master_list):

    num_lists = len(master_list)
    num_items = len(master_list[0])
    average_list = []
    for j in range(num_items):
        numbers = [master_list[i][j] for i in range(num_lists)]
        avg_num = mean(numbers)
        average_list.append(avg_num)
    return average_list

def plot_combined_seeds(input_folder):
    output_plot_path = input_folder.joinpath("combined_plot.png")
    log_csv_file_list = [e for e in input_folder.iterdir() if e.is_file() and 'logs.csv' in str(e)]

    update_num_master_list, val_acc_master_list = [], []

    for log_csv_file in log_csv_file_list:
        update_num_list, val_acc_list = read_val_acc(log_csv_file)
        update_num_master_list.append(update_num_list)
        val_acc_master_list.append(val_acc_list)
    
    average_update_list = average_master_list(update_num_master_list)
    average_val_acc_list = average_master_list(val_acc_master_list)

    visualization.plot_jasons_lineplot(
        average_update_list,
        average_val_acc_list, 
        "updates",
        "val acc",
        f"average plot for {input_folder.name} over {len(update_num_master_list)} seeds",
        output_plot_path,
        )

if __name__ == "__main__":
    # plot_combined_seeds(Path("plots_2_prelim/huff_nc5_augsr_currcurriculum"))
    # plot_combined_seeds(Path("plots_2_prelim/huff_nc5_augsr_currrandom"))
    # plot_combined_seeds(Path("plots_2_prelim/huff_nc5_augrd_currcurriculum"))
    # plot_combined_seeds(Path("plots_2_prelim/huff_nc5_augrd_currrandom"))
    # plot_combined_seeds(Path("plots_2_prelim/huff_nc5_augeda_currcurriculum"))
    # plot_combined_seeds(Path("plots_2_prelim/huff_nc5_augeda_currrandom"))
    # plot_combined_seeds(Path("plots_2_prelim/fewrel_nc5_augsr_currcurriculum"))
    # plot_combined_seeds(Path("plots_2_prelim/fewrel_nc5_augsr_currrandom"))
    # plot_combined_seeds(Path("plots/huff_nc5_augeda_norig1_currcurriculum"))
    # plot_combined_seeds(Path("plots/huff_nc5_augeda_norig1_currrandom"))
    # plot_combined_seeds(Path("plots/huff_nc5_augeda_norig1_curranti"))