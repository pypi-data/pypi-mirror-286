# Adam-mini
A PyTorch implementation of Adam-mini,  a mini-version of Adam that achieves on-par or better performance than AdamW with **45% to 50%** less memory footprint.  


## How to use 

```
from Adam_mini import Adam_mini

optimizer = Adam_mini(
            named_parameters = model.named_parameters(), 
            lr = lr, 
            betas = (beta1,beta2), 
            eps = eps,
            weight_decay = weight_decay, 
            model_sharding = True,
            dim = model_config.dim,
            n_heads = model_config.n_heads,
            n_kv_heads = model_config.n_kv_heads,
            )
            
```



**Regarding all the hyperparameters** including learning rate (lr), weight_decay, beta1, beta2, eps, we recommend using the same values as those used for AdamW.

If you are training a language model, please pass the following info to Adam-mini:

- model_sharding: set to True if you are using model parallelism with more than 1 GPU, including FSDP and zero_1,2,3 in Deepspeed. Set to False if you are using DDP or single-GPU training.

- dim: dimension for hidden feature. Could be unspecified if you are training non-transformer models.

- n_heads: number of attention heads. Could be unspecified if you are training non-transformer models.

- n_kv_heads: number of head for Key and Value. Or equivalently, number of query groups in Group query Attention. Also known as "n_query_groups".  If is None, it will be the same value as n_head. Could be unspecified if you are training non-transformer models.


## Citation

If you find this code helpful, please cite our paper in the following format.

```
@article{zhang2024adam,
  title     = {Adam-mini: Use Fewer Learning Rates To Gain More},
  author    = {Zhang, Yushun and Chen, Congliang  and Li, Ziniu and Ding, Tian and Wu, Chenwei and Ye, Yinyu and Luo, Zhi-Quan and Sun, Ruoyu},
  booktitle = {arXiv preprint arXiv:2406.16793},
  year      = {2024},
}
```
