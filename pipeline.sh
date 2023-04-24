#!/bin/bash

#Step 0: start cloud if not active

#python3 startInstance.py
#sleep 8

# NOTE: this only works with the specific configuration that exists. Might need to update
TABLE=$(~/Downloads/google-cloud-sdk/bin/gcloud compute instances list --project symmetric-axle-384300)
ExtIP=0
i=0
for datum in $TABLE
do
    if [ $i -eq 11 ]
    then
        ExtIP=$datum
    fi
    i=$((i+1))
done
echo $ExtIP

#Step 1: assign work to cloud through ssh

echo '############ connecting to VM ############'
ssh -i ~/.ssh/gckey wittnebeljohn@$ExtIP -f 'cd aliera; screen -d -m; ./worker.sh 160 100 > /dev/null'
echo '############     exited VM    ############'

#Step 2: run test.py with proportional work (like 100 to 160), approx 30min -> 46 generations/day potentially

python3 test.py 100

#Step 3: retrieve data from VM, shutdown VM

scp -i ~/.ssh/gckey wittnebeljohn@$ExtIP:~/aliera/AI/data.zip ./AI/
while [ $? -eq 1 ];
do
    echo "NOK"</br>
    python3 test.py 10
    scp -i ~/.ssh/gckey wittnebeljohn@$ExtIP:~/aliera/AI/data.zip ./AI/
done

echo '############ connecting to VM ############'
ssh -i ~/.ssh/gckey wittnebeljohn@$ExtIP 'cd aliera/AI; rm data.zip; rm -rf trainingData2; mkdir trainingData2; sudo shutdown -h now'
echo '############    exited VM    #############'

#Step 4: Combine data

cd AI
unzip data.zip
NUMLOCAL=$(ls trainingData | wc -l)
i=$(($NUMLOCAL))

for picklefile in $(ls trainingData2)
do
    cp trainingData2/$picklefile ./trainingData/pos${i}.pickle
    i=$(($i+1))
done

rm -rf trainingData2

#Step 5: train, verify that new generation is better
cd ..
python3 test.py train 
