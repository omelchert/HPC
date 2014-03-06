rm ./data_august/MPCS_memDissipation_*.dat

BASE_PATH_XML=../../../HERO-CLUSTER_QSTAT_XML_OUTPUT/cronJob/

for xmlFile in ${BASE_PATH_XML}/MPCS/*_201308*_h*m00.xml;
do
  echo $xmlFile
  python main_dissipation.py --fromFile $xmlFile --all >> ./data_august/MPCS_memDissipation_raw.dat 
  python main_dissipation.py --fromFile $xmlFile       >> ./data_august/MPCS_memDissipation_average.dat 
done

cd gp
bash MPCS_memDissipation_raw_mem.sh ../data_august/MPCS_memDissipation_raw.dat
bash MPCS_memDissipation_raw_memPerSlot.sh ../data_august/MPCS_memDissipation_raw.dat




