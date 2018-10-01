#!/bin/bash
#
# This script takes a volumetric myelin sensitive image, and evaluates 
# the intensity values along precreated intracortical surfaces. Additionally, 
# it will map a annotation file to the individual subject space. 
#
#
# Set up variables
# subject directory within BIDS structure
baseDir=/Data/BIDS/sub1
myeImage=/Data/BIDS/anat/sub1_myelin_scan.nii.gz
lhAnnot=/MPC/parcellations/lh.sjh.annot
rhAnnot=/MPC/parcellations/rh.sjh.annot
   
# set up and make necessary subfolders 
tmpDir="$baseDir"/tmpProcessingMyelin
warpDir="$baseDir"/xfms
for thisDir in $tmpDir $warpDir ; do
        [[ ! -d "$thisDir" ]] && mkdir "$thisDir"
done
    
subject=$(basename "$baseDir")
export SUBJECTS_DIR="$baseDir"/surfaces

# Register to Freesurfer space
bbregister --s "$subject" --mov "$myeImage" --reg "$warpDir"/"$subject"_mye2fs_bbr.lta --init-fsl --t1 

# Register to surface
for num_surfs in $(seq 10 1 30) ; do

	for hemi in l r; do 
		# find all equivolumetric surfaces and list by creation time
		x=$(ls -t "$SUBJECTS_DIR"/equivSurfs/"$num_surfs"surfs/${hemi}*)

		for n in $(seq 1 1 "$num_surfs") ; do
			
			# select a surfaces and copy to the freesurfer directory
			which_surf=$(sed -n "$n"p <<< "$x")
			cp "$which_surf" "$SUBJECTS_DIR"/"$subject"/surf/"$hemi"h."$n"by"$num_surfs"surf
		
		    # project intensity values from volume onto the surface
			do_cmd mri_vol2surf \
					--mov "$myeImage" \
					--reg "$warpDir"/"$subject"_mye2fs_bbr.lta \
					--hemi "$hemi"h \
					--out_type mgh \
					--trgsubject "$subject" \
					--out "$tmpDir"/"$hemi"h."$n".mgh \
					--surf "$n"by"$num_surfs"surf
		
		done
	
	done
	
done

# create symbolic link to fsaverage within the subject's directory
ln -s $FREESURFER_HOME/subjects/fsaverage $SUBJECTS_DIR 

# map annotation to subject space
mri_surf2surf --srcsubject fsaverage --trgsubject $subject --hemi lh \
    --sval-annot $lhAnnot
    --tval       $SUBJECTS_DIR/"$subject"/label/lh.sjh.annot
mri_surf2surf --srcsubject fsaverage --trgsubject $subject --hemi rh \
    --sval-annot $rhAnnot
    --tval       $SUBJECTS_DIR/"$subject"/label/rh.sjh.annot
