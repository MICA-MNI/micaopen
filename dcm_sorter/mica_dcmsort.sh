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
