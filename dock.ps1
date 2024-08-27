docker build -t pratik1188/ffmpeg.v1 .
docker image prune --force
docker run -it --rm -v D:\Study\Projects\Vided\vided-container-apps\root:/mnt -p 8000:8000 pratik1188/ffmpeg.v1