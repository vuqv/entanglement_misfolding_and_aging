#!/bin/bash
cur_dir=`pwd`
for i in {0..49}
do
        cd ${cur_dir}/${i}/
        sbatch job_GQ_mgc.sh 
done

