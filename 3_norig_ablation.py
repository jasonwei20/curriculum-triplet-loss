from utils import common, configuration, triplet_cl_methods
from statistics import mean, stdev

if __name__ == "__main__":

    cfg_json_list = [
        # "config/orig_ratio/huff_nc5_eda_norig0_c.json",
        # "config/orig_ratio/huff_nc5_eda_norig1_c.json",
        # "config/orig_ratio/huff_nc5_eda_norig2_c.json",
        # "config/orig_ratio/huff_nc5_eda_norig4_c.json",
        # "config/orig_ratio/huff_nc5_eda_norig8_c.json",
        # "config/orig_ratio/huff_nc5_eda_norig0_r.json",
        # "config/orig_ratio/huff_nc5_eda_norig1_r.json",
        # "config/orig_ratio/huff_nc5_eda_norig2_r.json",
        # "config/orig_ratio/huff_nc5_eda_norig4_r.json",
        # "config/orig_ratio/huff_nc5_eda_norig8_r.json",
        # "config/orig_ratio/huff_nc5_sr_norig0_c.json",
        # "config/orig_ratio/huff_nc5_sr_norig1_c.json",
        # "config/orig_ratio/huff_nc5_sr_norig2_c.json",
        # "config/orig_ratio/huff_nc5_sr_norig4_c.json",
        # "config/orig_ratio/huff_nc5_sr_norig8_c.json",
        # "config/orig_ratio/huff_nc5_sr_norig0_r.json",
        # "config/orig_ratio/huff_nc5_sr_norig1_r.json",
        # "config/orig_ratio/huff_nc5_sr_norig2_r.json",
        # "config/orig_ratio/huff_nc5_sr_norig4_r.json",
        # "config/orig_ratio/huff_nc5_sr_norig8_r.json",
        #
        # "config/orig_ratio/huff_nc5_eda_norig0_a.json",
        # "config/orig_ratio/huff_nc5_eda_norig1_a.json",
        # "config/orig_ratio/huff_nc5_eda_norig2_a.json",
        # "config/orig_ratio/huff_nc5_sr_norig0_a.json",
        # "config/orig_ratio/huff_nc5_sr_norig1_a.json",
        # "config/orig_ratio/huff_nc5_sr_norig2_a.json",
        #
        # "config/orig_ratio/huff_nc5_rd_norig0_c.json",
        # "config/orig_ratio/huff_nc5_rd_norig1_c.json",
        # "config/orig_ratio/huff_nc5_rd_norig2_c.json",
        # "config/orig_ratio/huff_nc5_rd_norig0_r.json",
        # "config/orig_ratio/huff_nc5_rd_norig1_r.json",
        # "config/orig_ratio/huff_nc5_rd_norig2_r.json",
        # "config/orig_ratio/huff_nc5_rd_norig0_a.json",
        # "config/orig_ratio/huff_nc5_rd_norig1_a.json",
        # "config/orig_ratio/huff_nc5_rd_norig2_a.json",
        #
        # "config/orig_ratio/fewrel_nc5_rd_norig0_c.json",
        # "config/orig_ratio/fewrel_nc5_rd_norig1_c.json",
        # "config/orig_ratio/fewrel_nc5_rd_norig2_c.json",
        # "config/orig_ratio/fewrel_nc5_rd_norig0_r.json",
        # "config/orig_ratio/fewrel_nc5_rd_norig1_r.json",
        # "config/orig_ratio/fewrel_nc5_rd_norig2_r.json",
        # "config/orig_ratio/fewrel_nc5_rd_norig0_a.json",
        # "config/orig_ratio/fewrel_nc5_rd_norig1_a.json",
        # "config/orig_ratio/fewrel_nc5_rd_norig2_a.json",
        #
        # "config/orig_ratio/fewrel_nc5_eda_norig0_c.json",
        # "config/orig_ratio/fewrel_nc5_eda_norig1_c.json",
        # "config/orig_ratio/fewrel_nc5_eda_norig2_c.json",
        # "config/orig_ratio/fewrel_nc5_eda_norig0_r.json",
        # "config/orig_ratio/fewrel_nc5_eda_norig1_r.json",
        # "config/orig_ratio/fewrel_nc5_eda_norig2_r.json",
        # "config/orig_ratio/fewrel_nc5_eda_norig0_a.json",
        # "config/orig_ratio/fewrel_nc5_eda_norig1_a.json",
        # "config/orig_ratio/fewrel_nc5_eda_norig2_a.json",
        #
        # "config/orig_ratio/huff_nc5_rd_norig4_c.json",
        # "config/orig_ratio/huff_nc5_rd_norig4_r.json",
        # "config/orig_ratio/huff_nc5_rd_norig4_a.json",
        #
        # "config/orig_ratio/fewrel_nc5_rd_norig4_c.json",
        # "config/orig_ratio/fewrel_nc5_rd_norig4_r.json",
        # "config/orig_ratio/fewrel_nc5_rd_norig4_a.json",
        #
        # "config/orig_ratio/fewrel_nc5_sr_norig0_c.json",
        # "config/orig_ratio/fewrel_nc5_sr_norig1_c.json",
        # "config/orig_ratio/fewrel_nc5_sr_norig2_c.json",
        # "config/orig_ratio/fewrel_nc5_sr_norig0_r.json",
        # "config/orig_ratio/fewrel_nc5_sr_norig1_r.json",
        # "config/orig_ratio/fewrel_nc5_sr_norig2_r.json",
        # "config/orig_ratio/fewrel_nc5_sr_norig0_a.json",
        # "config/orig_ratio/fewrel_nc5_sr_norig1_a.json",
        # "config/orig_ratio/fewrel_nc5_sr_norig2_a.json",
        #
        # "config/orig_ratio/huff_nc5_sr_norig4_a.json",
        # "config/orig_ratio/huff_nc5_sr_norig8_a.json",
        # "config/orig_ratio/huff_nc5_eda_norig4_r.json",
        # "config/orig_ratio/huff_nc5_eda_norig4_a.json",
        # "config/orig_ratio/huff_nc5_eda_norig8_a.json",
        # "config/orig_ratio/fewrel_nc5_sr_norig4_c.json",
        # "config/orig_ratio/fewrel_nc5_sr_norig4_r.json",
        # "config/orig_ratio/fewrel_nc5_sr_norig4_a.json",
        # "config/orig_ratio/fewrel_nc5_eda_norig4_c.json",
        # "config/orig_ratio/fewrel_nc5_eda_norig4_r.json",
        # "config/orig_ratio/fewrel_nc5_eda_norig4_a.json",
        # "config/orig_ratio/fewrel_nc5_eda_norig0_r.json",
        # "config/orig_ratio/fewrel_nc5_eda_norig1_r.json",
        # "config/orig_ratio/fewrel_nc5_eda_norig2_r.json",
        # "config/orig_ratio/fewrel_nc5_rd_norig0_r.json",
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
