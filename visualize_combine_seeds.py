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

def get_combined_seeds_lists(input_folder):

    print(input_folder)

    log_csv_file_list = [e for e in input_folder.iterdir() if e.is_file() and 'logs.csv' in str(e)]

    update_num_master_list, val_acc_master_list = [], []

    for log_csv_file in log_csv_file_list:
        update_num_list, val_acc_list = read_val_acc(log_csv_file)
        update_num_master_list.append(update_num_list)
        val_acc_master_list.append(val_acc_list)

    average_update_list = average_master_list(update_num_master_list)
    average_val_acc_list = average_master_list(val_acc_master_list)

    return average_update_list, average_val_acc_list, len(update_num_master_list)

def plot_single_combined_plot(input_folder):

    output_plot_path = input_folder.joinpath("combined_plot.png")
    average_update_list, average_val_acc_list, num_seeds = get_combined_seeds_lists(input_folder)

    visualization.plot_jasons_lineplot(
        average_update_list,
        average_val_acc_list, 
        "updates",
        "val acc",
        f"average plot for {input_folder.name} over {num_seeds} seeds",
        output_plot_path,
        )

def plot_cra_combined_plot(
        folder_stem,
    ):

    curriculum_folder = Path(str(folder_stem) + 'curriculum')
    random_folder = Path(str(folder_stem) + 'random')
    anti_folder = Path(str(folder_stem) + 'anti')

    average_update_list, curr_val_acc_list, num_seeds = get_combined_seeds_lists(curriculum_folder)
    _, random_val_acc_list, _ = get_combined_seeds_lists(random_folder)
    _, anti_val_acc_list, _ = get_combined_seeds_lists(anti_folder)

    output_png_path = Path("combined_plots").joinpath(folder_stem.name + '.png')
    visualization.plot_cra_lineplot(
        x = average_update_list,
        curr_y = curr_val_acc_list,
        rand_y = random_val_acc_list,
        anti_y = anti_val_acc_list,
        title = f"{folder_stem.name} for {num_seeds} seeds",
        output_png_path = output_png_path,
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
    # plot_single_combined_plot(Path("plots/huff_nc5_augeda_norig1_currcurriculum"))

    # plot_cra_combined_plot(Path("plots/huff_nc5_augeda_norig1_curr"))
    # plot_cra_combined_plot(Path("plots/huff_nc5_augrd_norig1_curr"))
    # plot_cra_combined_plot(Path("plots/huff_nc5_augsr_norig1_curr"))
    plot_cra_combined_plot(Path("plots/fewrel_nc5_augsr_norig1_curr"))
    # plot_cra_combined_plot(Path("plots/fewrel_nc5_augeda_norig1_curr"))
    # plot_cra_combined_plot(Path("plots/fewrel_nc5_augrd_norig1_curr"))