# CERNN
Code Edit Recommendation Using a Recurrent Neural Network

# Data for the Experiment
You can download the data from http://salab.kaist.ac.kr/tse2015/AllProjects.zip. Then, please extract the data to the folder "dataset" under this project.


# Execution for the Experiment
You can run this source code for each project by typing the following command in your console window:

>> python rnn_recommend.py --project MDT --window_size 3 --step 10 --lookup 1000 --batch_size 32 --epochs 500 --threshold 0.91 --remove_dupe

>> python rnn_recommend.py --project ECF --window_size 3 --step 10 --lookup 1000 --batch_size 32 --epochs 500 --threshold 0.91 --remove_dupe

>> python rnn_recommend.py --project PDE --window_size 3 --step 10 --lookup 1000 --batch_size 32 --epochs 500 --threshold 0.91 --remove_dupe

>> python rnn_recommend.py --project Platform --window_size 3 --step 10 --lookup 1000 --batch_size 32 --epochs 500 --threshold 0.91 --remove_dupe

>> python rnn_recommend.py --project Mylyn --window_size 3 --step 10 --lookup 1000 --batch_size 32 --epochs 500 --threshold 0.91 --remove_dupe
