from utils import common, configuration, triplet_cl_methods
from statistics import mean, stdev

if __name__ == "__main__":

    cfg_json_list = [
        # "config/a_continued_experiments/huff_nc10_eda_norig1_c.json",
        # "config/a_continued_experiments/huff_nc10_eda_norig1_a.json",
        # "config/a_continued_experiments/fewrel_nc10_eda_norig1_c.json",
        # "config/a_continued_experiments/fewrel_nc10_eda_norig1_a.json",
        # "config/a_continued_experiments/amzn_nc3_eda_norig1_c.json",
        # "config/a_continued_experiments/amzn_nc3_eda_norig1_a.json",
        # "config/a_continued_experiments/covidclu_nc3_eda_norig1_c.json",
        # "config/a_continued_experiments/covidclu_nc3_eda_norig1_a.json",

        # "config/a_continued_experiments/huff_nc10_eda_norig1_r.json",
        # "config/a_continued_experiments/fewrel_nc10_eda_norig1_r.json",
        # "config/a_continued_experiments/amzn_nc3_eda_norig1_r.json",
        # "config/a_continued_experiments/covidclu_nc3_eda_norig1_r.json",
    ]

    for cfg_json in cfg_json_list:

        cfg = configuration.triplet_ap_cl_gradual_config.from_json(cfg_json); print(f"\n\n\nconfig from {cfg_json}")
    
        acc_list = []
        for seed_num in range(cfg.num_seeds):

            common.set_random_seed(seed_num)
            acc = triplet_cl_methods.train_eval_cl_gradual_model(cfg, seed_num)
            acc_list.append(acc)
        
        acc_mean = mean(acc_list)
        acc_stdev = stdev(acc_list) if len(acc_list) > 1 else -1
        print(f"acc: {acc_mean:.3f} pm {acc_stdev:.3f} ; {acc_list}")
