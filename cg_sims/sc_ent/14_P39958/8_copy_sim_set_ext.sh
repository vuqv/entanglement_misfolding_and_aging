 
#!/bin/bash
cur_dir=`pwd`
for i in {0..49}
do
        cd ${cur_dir}
        cp template/job_cg_ext.sh ${i}/
        cp template/control_ext.cntrl ${i}/
        sed "s/SETINDEX/${i}/g" -i ${i}/job_cg_ext.sh
        sed "s/SETINDEX/${i}/g" -i ${i}/control_ext.cntrl        
# cd ${i}_*/ && qsub job.sh

done

