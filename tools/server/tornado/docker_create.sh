nvidia-docker run -dit \
 --env LANG=C.UTF-8 \
 -v /dmcv/lianshuailong/cv/multi-modal:/workspace\
 --name vae0.1_test \
 -p 80:80 \
 --shm-size 200g \
 thub.autohome.com.cn/dmcv/lianshuailong/vae:v0.1 
