#rm ./data/*_memDissipation_*.dat

BASE_PATH_XML=../../../HERO-CLUSTER_QSTAT_XML_OUTPUT/cronJob/

for NODE_TYPE in CFDH CFDL MPCB MPCS;
do
  for xmlFile in ${BASE_PATH_XML}/${NODE_TYPE}/*.xml;
  do
    echo $xmlFile
    python main_dissipation.py --fromFile $xmlFile --all >> ./data/${NODE_TYPE}_memDissipation_raw.dat 
    python main_dissipation.py --fromFile $xmlFile       >> ./data/${NODE_TYPE}_memDissipation_average.dat 
  done
done
