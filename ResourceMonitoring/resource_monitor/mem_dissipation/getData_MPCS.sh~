rm ./data_mpcs/MPCS_memDissipation_*.dat

BASE_PATH_XML=../../../HERO-CLUSTER_QSTAT_XML_OUTPUT/cronJob/

for xmlFile in ${BASE_PATH_XML}/MPCS/*.xml;
do
  echo $xmlFile
  python main_dissipation.py --fromFile $xmlFile       >> ./data_mpcs/MPCS_memDissipation_average.dat 
done





