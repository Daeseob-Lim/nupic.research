# Spatial Pooler Without Topology
* random SDRs, fixed sparsity

`python train_sp.py -b 1 -d randomSDR --spatialImp py --trackOverlapCurve 1 -e 50`

* random SDRs, varying sparsity

`python train_sp.py -b 1 -d randomSDRVaryingSparsity --spatialImp cpp --trackOverlapCurve 1 -e 100 --name randomSDRVaryingSparsityNoTopology`
 
* Continuous learning experiment

	* Train SP on random SDR dataset until converge
	* Then switch to a different dataset
	* The SP should adapt to the new dataset

`python train_sp.py -b 1 -d randomSDRVaryingSparsity --trackOverlapCurve 1 --name continuous_learning_without_topology --spatialImp cpp --changeDataSetAt 50 -e 120` 

* Fault tolerance experiment (no topology)

	* Train SP on random SDR dataset until converge
	* kill a fraction of the SP columns

`python train_sp.py -b 1 --name trauma_boosting_without_topology --spatialImp faulty_sp --killCellsAt 50 --killCellPrct 0.5 --trackOverlapCurve 1`

* Random Bar Pairs Vs. Random Cross (No Topology)

`python train_sp.py -d randomBarPairs  -e 200 -b 1 --showExampleRFs 1`
`python train_sp.py -d randomCross --spatialImp monitored_sp -e 200 -b 1 --showExampleRFs 1`

* Two input fields with correlated SDR pairs

`python train_sp.py -b 1 –d correlatedSDRPairs`

# Spatial Pooler With Topology

* Random SDRs with varying sparsity

`python train_sp.py -t 1 -b 1 -d randomSDRVaryingSparsity --spatialImp cpp --trackOverlapCurve 1 -e 100 --name randomSDRVaryingSparsity`

* Continuous learning experiment

`python train_sp.py -t 1 -b 1 -d randomSDRVaryingSparsity --spatialImp cpp --trackOverlapCurve 1 -e 120 --changeDataSetAt 50 --name randomSDRVaryingSparsityContinuousLearning `

* Random Bar Pairs Vs. Random Cross (With Topology)

`python train_sp.py -t 1 -d randomCross --spatialImp py -e 200 -b 1`
`python train_sp.py -t 1 -d randomBarPairs --spatialImp py -e 200 -b 1`

* Random bar sets (more than two random bars per input)

`python train_sp.py -t 1 -d randomBarSets -b 1 --name random_bars_with_topology \
--spatialImp monitored_sp --changeDataSetContinuously 1 --boosting 1`

# Fault tolerance experiment (with topology)

* Fault tolerance to SP column death 
Train faulty_SP on random bar set dataset

`python train_sp.py -t 1 -d randomBarSets -b 1 --name trauma_boosting_with_topology \
--changeDataSetContinuously 1 --spatialImp faulty_sp --killCellsAt 180 \
--trackOverlapCurve 0 -e 600 --checkTestInput 1 --checkRFCenters 1 \
--saveBoostFactors 1 --checkInputSpaceCoverage 1`

* Fault tolerance to input afferents death

`python train_sp.py -t 1 -d randomBarSets -b 1 --name trauma_inputs_with_topology \
--changeDataSetContinuously 1 --spatialImp faulty_sp --killInputsAfter 180 \
--trackOverlapCurve 0 -e 600 --checkTestInput 1 --checkRFCenters 1 \
--saveBoostFactors 1 --checkInputSpaceCoverage 1`

* Analyze fault tolerance experiment results

`python analyze_trauma_experiment.py`

* Make trauma movie (requires ffmpeg)

 In figures/traumaMovie/ run:

`ffmpeg -start_number 100 -i trauma_inputs_with_topology_frame_%03d.png traumaMovie1.mp4`

# NYC Taxi experiment
* Run with random SP (no learning, no boosting)

	`python python_sp_tm_model.py --trainSP 0`
* Run with learning SP, but without boosting
 
	`python python_sp_tm_model.py --trainSP 1 --boostStrength 0`
* Run with learning SP, and boosting
 
`python python_sp_tm_model.py --trainSP 1 --boostStrength 20`
* plot results

# MNIST experiment
`python train_sp.py -t 1 -d mnist --spatialImp py -e 2 -b 1`