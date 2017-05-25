# author: boris@bic.mni.mcgill.ca
#
# v. 1.0 
# may 25, 2017
# 
# use: $0 <dcmdir> 
# creates a folder called <dcmdir_sorted> in which the different dicoms are sorted into 
# subfolders relative to their their subject and sequence information 
# i.e. dcmdir_sorted/patientid/scannumber_sequencename/ 

if [ $# -lt 1 ]
then
	echo "use: ./$0 <dcmdir> to create sorted copy <dcmdir_sorted> in the same folder" 
	exit 
fi

IN=${1}
OUT=${1%/}_sorted

mkdir -v ${OUT}

echo "SORT DICOMS******************************************************"
for i in `ls ${IN}/*`
do 

	#echo ${i}
	P=`dcminfo ${i} | grep "patient" | awk -F ' ' '{print $2}'`
	N=`dcminfo ${i} | grep "series" | awk -F ' ' '{print $2}'`
	N=${N:1}
	N=${N%]}
	S=`dcminfo ${i} | grep "series" | awk -F ' ' '{print $3}'`
	
	
	if [ ! -d "${OUT}/${P}" ]; then
		mkdir -v ${OUT}/${P}
	fi 
	
	
	if [ ! -d "${OUT}/${P}/${N}_${S}/" ]; then
		mkdir -v ${OUT}/${P}/${N}_${S}
	fi
	
	cp -v ${i} ${OUT}/${P}/${N}_${S}/	

done 
