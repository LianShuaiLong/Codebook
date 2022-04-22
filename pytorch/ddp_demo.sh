export CUDA_VISIBLE_DEVICES=1,2
python -m torch.distributed.launch --nproc_per_node=2 ddp_demo.py
