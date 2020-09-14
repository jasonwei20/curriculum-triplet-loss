from utils import common, configuration, triplet_cl_methods

if __name__ == "__main__":

    cfg_json_list = [
        "config/prelim/fewrel_nc5_sr_c.json",
        "config/prelim/fewrel_nc5_sr_r.json",
        "config/prelim/fewrel_nc5_sr_a.json",
        "config/prelim/fewrel_nc5_sr_n.json",
    ]

    for cfg_json in cfg_json_list:

        cfg = configuration.triplet_ap_cl_gradual_config.from_json(cfg_json); print(f"config from {cfg_json}")

        for seed_num in range(cfg.num_seeds):

            common.set_random_seed(seed_num)
            triplet_cl_methods.train_eval_cl_gradual_model(cfg, seed_num)