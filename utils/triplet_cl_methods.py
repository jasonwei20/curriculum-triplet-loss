from utils import dataloader, bert_avgpool, triplet_models, visualization, triplet_methods
import torch
import torch.optim as optim
from tqdm import tqdm
import random
from pathlib import Path

def train_eval_cl_gradual_model(
    cfg, 
    seed_num
):

    #load data
    train_sentence_to_label_orig, train_label_to_sentences_orig, _, test_sentence_to_label, train_sentence_to_encoding_orig, test_sentence_to_encoding = dataloader.load_ap_data_no_aug(cfg, seed_num)
    train_label_to_sentences_aug = train_label_to_sentences_orig.copy()
    train_sentence_to_label = train_sentence_to_label_orig.copy()
    train_sentence_to_encoding = train_sentence_to_encoding_orig.copy()

    # initialize model
    model, loss_fn, optimizer, device = triplet_methods.initialize_model(cfg)

    # train the model
    iter_bar = tqdm(range(cfg.total_updates + 1))
    update_num_list = []; train_loss_list = []; val_acc_list = []

    output_folder = f"plots/{cfg.exp_id}_nc{cfg.train_nc}_aug{cfg.aug_type}_norig{cfg.n_orig}_curr{cfg.curriculum_type}"
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    writer = open(f"{output_folder}/s{seed_num}_logs.csv", "w")
    mb_size = 64
    target_activated_examples = 64
    avg_percent_activated = 1.0
    percent_activated_list = []

    for update_num in iter_bar:

        ##################################################################################### sampling strategies
        # sample differently based on which stage of curriculum learning you're in
        if cfg.curriculum_type == "curriculum":
            if update_num == cfg.first_stage_updates:
                train_sentence_to_label, train_label_to_sentences_aug, train_sentence_to_encoding = dataloader.reload_ap_cl_data(train_sentence_to_label, train_label_to_sentences_orig, cfg, cfg.second_stage_alpha)
            elif update_num == cfg.second_stage_updates:
                train_sentence_to_label, train_label_to_sentences_aug, train_sentence_to_encoding = dataloader.reload_ap_cl_data(train_sentence_to_label, train_label_to_sentences_orig, cfg, cfg.third_stage_alpha)
            elif update_num == cfg.third_stage_updates:
                train_sentence_to_label, train_label_to_sentences_aug, train_sentence_to_encoding = dataloader.reload_ap_cl_data(train_sentence_to_label, train_label_to_sentences_orig, cfg, cfg.fourth_stage_alpha)
            elif update_num == cfg.fourth_stage_updates:
                train_sentence_to_label, train_label_to_sentences_aug, train_sentence_to_encoding = dataloader.reload_ap_cl_data(train_sentence_to_label, train_label_to_sentences_orig, cfg, cfg.fifth_stage_alpha)
            elif update_num == cfg.fifth_stage_updates:
                train_sentence_to_label, train_label_to_sentences_aug, train_sentence_to_encoding = dataloader.reload_ap_cl_data(train_sentence_to_label, train_label_to_sentences_orig, cfg, cfg.sixth_stage_alpha)

        elif cfg.curriculum_type == "random":
            if update_num % 50 == 0:
                random_alpha = random.choice([0.1, 0.2, 0.3, 0.4, 0.5])
                train_sentence_to_label, train_label_to_sentences_aug, train_sentence_to_encoding = dataloader.reload_ap_cl_data(train_sentence_to_label, train_label_to_sentences_orig, cfg, random_alpha)

        elif cfg.curriculum_type == "anti":
            if update_num == 1:
                train_sentence_to_label, train_label_to_sentences_aug, train_sentence_to_encoding = dataloader.reload_ap_cl_data(train_sentence_to_label, train_label_to_sentences_orig, cfg, cfg.sixth_stage_alpha)
            elif update_num == cfg.first_stage_updates:
                train_sentence_to_label, train_label_to_sentences_aug, train_sentence_to_encoding = dataloader.reload_ap_cl_data(train_sentence_to_label, train_label_to_sentences_orig, cfg, cfg.fifth_stage_alpha)
            elif update_num == cfg.second_stage_updates:
                train_sentence_to_label, train_label_to_sentences_aug, train_sentence_to_encoding = dataloader.reload_ap_cl_data(train_sentence_to_label, train_label_to_sentences_orig, cfg, cfg.fourth_stage_alpha)
            elif update_num == cfg.third_stage_updates:
                train_sentence_to_label, train_label_to_sentences_aug, train_sentence_to_encoding = dataloader.reload_ap_cl_data(train_sentence_to_label, train_label_to_sentences_orig, cfg, cfg.third_stage_alpha)
            elif update_num == cfg.fourth_stage_updates:
                train_sentence_to_label, train_label_to_sentences_aug, train_sentence_to_encoding = dataloader.reload_ap_cl_data(train_sentence_to_label, train_label_to_sentences_orig, cfg, cfg.second_stage_alpha)
            elif update_num == cfg.fifth_stage_updates:
                train_sentence_to_label, train_label_to_sentences_aug, train_sentence_to_encoding = train_sentence_to_label_orig, train_label_to_sentences_orig, train_sentence_to_encoding_orig
        #####################################################################################
        
        anchor, pos, neg = dataloader.generate_triplet_batch(train_label_to_sentences_aug, train_sentence_to_encoding, device, mb_size=mb_size)

        model.train()
        model.zero_grad()

        logits = model(anchor, pos, neg)
        train_loss, percent_activated = loss_fn(*logits)

        train_loss.backward()
        optimizer.step()
        percent_activated_list.append(percent_activated)

        if update_num % cfg.eval_interval == 0:

            val_acc = triplet_methods.eval_model(
                model, 
                device, 
                train_sentence_to_label_orig, 
                train_label_to_sentences_orig, 
                train_sentence_to_encoding_orig, 
                test_sentence_to_label, 
                test_sentence_to_encoding,
            )
            avg_percent_activated = sum(percent_activated_list) / len(percent_activated_list)

            iter_bar_str =  ( f"update {update_num}/{cfg.total_updates}: " 
                            + f"mb_train_loss={float(train_loss):.4f}, "
                            + f"val_acc={float(val_acc):.4f}, "
                            + f"percent_activated={float(avg_percent_activated):.3f}, "
                            + f"mb_size={mb_size}"
                            )
            iter_bar.set_description(iter_bar_str)
            update_num_list.append(update_num); val_acc_list.append(val_acc); train_loss_list.append(train_loss)
            writer.write(f"{update_num},{val_acc:.4f},{train_loss:.4f}\n")
            percent_activated_list = []
            if cfg.hard_negative_mining == 'semi-hard':
                mb_size = min(int(target_activated_examples / avg_percent_activated), 2000)

    visualization.plot_jasons_lineplot(update_num_list, train_loss_list, 'updates', 'training loss', f"{cfg.exp_id} n_c={cfg.train_nc} aug={cfg.aug_type} curr={cfg.curriculum_type} max_val_acc={max(val_acc_list):.3f}", f"{output_folder}/s{seed_num}_train_loss.png")    
    visualization.plot_jasons_lineplot(update_num_list, val_acc_list, 'updates', 'validation accuracy', f"{cfg.exp_id} n_c={cfg.train_nc} aug={cfg.aug_type} curr={cfg.curriculum_type} max_val_acc={max(val_acc_list):.3f}", f"{output_folder}/s{seed_num}_val_acc{max(val_acc_list):.3f}.png")
    return max(val_acc_list)
