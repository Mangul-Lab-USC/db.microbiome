#!/usr/bin/python
. /u/local/Modules/default/init/modules.sh
module load python/2.6


python /u/home/a/akarlsbe/scratch/fungi/db.microbiome/Code/UpdateDatabase.py


# make sh file executable:
# chmod +x run_taxID_updates.sh
# CD into sh file directory. Then run this command in terminal to submit to hoffman:
# qsub -m bea -cwd -V -N taxIdUpdates -l h_data=24G,highp,time=24:00:00 run_taxID_updates.sh


# qsub -cwd -V -N test -l h_data=24G,highp,time=10:00:00 run.sh

# ln -s /path/to/libc.so.6 /lib64/libc.so.6

# ln -s /lib64/libc.so.6 /lib64/libc.so.6

# ln -s /lib/libc.so.6 /lib64/libc.so.6

# /lib/libc.so.6
# /lib/i686/nosegneg/libc.so.6
# /lib64/libc.so.6


