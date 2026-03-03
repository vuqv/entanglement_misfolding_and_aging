#!/bin/bash
cur_dir=`pwd`
for i in {0..49}
do
        #cd ${cur_dir}/${i}/
        echo ${i}
       tail -n 1 ${cur_dir}/${i}/fQ.dat	
done

