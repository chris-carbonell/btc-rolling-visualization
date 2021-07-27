ffmpeg -y -f image2 -itsscale 1.62 -i "../output/grp_inc_rr_z/btc_rr_%%05d.png" -s 1134x618 -b 5000k -vcodec libx264 btc_rr.avi
ffmpeg -y -f image2 -itsscale 0.07 -i "../output/grp_inc_rr_z/btc_z_%%05d.png" -s 1134x618 -b 5000k -vcodec libx264 btc_z.avi
ffmpeg -y -loop 1 -i "../output/grp_inc_rr_z/btc_z_03660.png" -c:v libx264 -t 5 -pix_fmt yuv420p -vf scale=1134:618 -b 5000k btc_last.avi
