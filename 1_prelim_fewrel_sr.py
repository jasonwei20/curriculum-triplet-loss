from utils import common, configuration, triplet_cl_methods
from statistics import mean, stdev

if __name__ == "__main__":

    cfg_json_list = [
        "config/prelim_hnm/fewrel_nc5_sr_c.json",
        "config/prelim_hnm/fewrel_nc5_sr_r.json",
        "config/prelim_hnm/fewrel_nc5_sr_a.json",
        "config/prelim_hnm/fewrel_nc5_sr_n.json",
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
