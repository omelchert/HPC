
BASE_PATH_XML=../../../HERO-CLUSTER_QSTAT_XML_OUTPUT/cronJob/

for xmlFile in ${BASE_PATH_XML}/MPCS/*_2013*_h*m00.xml;
do
  echo $xmlFile
  #python main_slotStats.py --fromFile $xmlFile  >> ./data_slots/MPCS_nOccSlots_201310.dat 
  python main_slotStats.py --fromFile $xmlFile  >> ./data_slots/MPCS_nOccSlots_2013.dat 
done



