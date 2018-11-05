function [sub_success] = surf2mpc(dataDir, sub, num_surf, parc_name)
%
% This script can be used as a wrapper to run the function build_mpc, and 
% thus construct microstructure profile covariance (MPC) matrices for a 
% group of individiuals. The following four variable need to be updated for
% your individual system/study. It will automatically save the intensity
% profiles and MPC matrices as a text files in the subject's BIDS folder, 
% alongside the preconstructed equivolumetric surfaces. 
%
% INPUT
% dataDir 		overarching BIDS directory
% sub 			subject id
% num_surf		surface solution number (default is 14)
% parc_name		name of parcellation in annotation file (default is sjh)

if nargin < 4
	parc_name='sjh';
end
if nargin < 3
	num_surf=14;
end
	

    % setting output directory
    OPATH = strcat(dataDir, '/', sub, '/surfaces/equivSurfs/', num2str(num_surf), 'surfs_out/');
    
    if exist(OPATH, 'dir')
    
    try
        
        % left hemisphere - looping through intracortical surfaces
        for ii = 1:num_surf
            
            % selects and reads surface files
            
            thisname_mgh    = strcat(OPATH, 'lh.', num2str(ii), '.mgh');
            data = MRIread(char(thisname_mgh));
            
            % inputs intensity value at each vertex along the the selected
            % intracortical surface into a matrix
            BBl(ii,:)    = data.vol;
        end
        
        % repeat for the right hemisphere
        for ii = 1:num_surf
            thisname_mgh    = strcat(OPATH, 'rh.', num2str(ii), '.mgh');
            data = MRIread(char(thisname_mgh));
            BBr(ii,:)    = data.vol;
        end
        
        % concatenate hemispheres and flip so pial surface is at the top
        BB = flipud([BBr BBl]);
        
        % load subject surface
        G = SurfStatReadSurf({strcat(dataDir, '/', sub, '/surfaces/', sub, '/surf/lh.pial'), strcat(dataDir, '/', sub, '/surfaces/', sub, '/surf/rh.pial')});
        
        % create mpc matrix (and nodal intensity profiles if parcellating)
        [~, lh_parc, ~] = read_annotation(strcat(dataDir, '/', sub, '/surfaces/', sub, '/label/lh.', parc_name, '.annot'));
        [~, rh_parc, ~] = read_annotation(strcat(dataDir, '/', sub, '/surfaces/', sub, '/label/rh.', parc_name, '.annot'));
        [MPC, I, problemNodes{s}] = build_mpc(BBs, vertcat(lh_parc,rh_parc));

        % check success of MPC and save output
        if nnz(isnan(MPC))
            sub_sucess = 0;
            fprintf('MPC building failed for subject: %s\n',sub);
        else
            sub_sucess = 1;
            dlmwrite(strcat(OPATH, '/intensity_profiles.txt'),I);
            dlmwrite(strcat(OPATH, '/mpc.txt'),MPC);
        end
        
		% cleanup
		clear('BBl','BBr','BB'); 
		catch
			warning('Missing files for subject: %s\n',sub);
			sub_sucess = -1;
			continue
        
		end
        
    else
        
        sub_sucess = -1;

    end
            
end

end %function
