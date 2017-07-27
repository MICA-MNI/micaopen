 function BoSurfStatPlotVolStat(slm, mask, template, vol0, thresh,RPATH,NPATH,prefix,view,varargin)
 
    % t-map
    mc2         = [ makeColorMap([1 1 0],[1 0 0],[0 0 0],512/4); ...
                    makeColorMap([0 0 0],[0.7 0.7 0.7],[0 0 0],512/4); ...
                    makeColorMap([0 0 0],[0 0 1],[0 1 1],512/4)];
    mc2 = flipud(mc2);   

    
    slm.t = slm.t.*mask; 
    my_nii = template; 
    my_nii.img = reshape(slm.t,size(my_nii.img)); 
    save_nii(my_nii, [NPATH prefix '.t.tools.nii']); 
    
    p = 1-tcdf(slm.t,slm.df); 
    
%     f=figure('Visible','off'); 
%         BoSurfStatViewsFlex( p, mask, vol0,  [0 thresh], view,varargin{:});
%         colormap([0 0 0; makeColorMap([1 1 0],[1 0 0],1000); 0 0 0]);
%         exportfigbo(f,[RPATH prefix '.p_uncorr.png'],'png',10);
%     close(f);
    
    %SurfStatWriteVol([NPATH prefix '.p_uncorr.nii'],p,vol0)   ; 
    my_nii = template; 
    my_nii.img = reshape(p,size(my_nii.img)); 
    save_nii(my_nii, [NPATH prefix '.puncorr.tools.nii']); 
    
    template0 = double(template.img(:))'; 
    try 
        [pval,peak,clus,clusid] = SurfStatP(slm,mask==1,thresh); 
    catch
        disp('SurfStatP failed')
    end
    
    maskedfeat = pval.C;
    maskedfeat(pval.C>0.05) = 1; 
    SurfStatWriteVol([NPATH prefix '.fwe_pmap.nii'],maskedfeat,vol0); 
    
    % only thresholded map
    if exist('pval') && isfield(pval,'C') && any(pval.C<0.05) 
%         f=figure('Visible','off'); 
%             BoSurfStatViewsFlex( pval.C, mask, vol0,  [0 0.05], view,varargin{:});
%             colormap([0 0 0; makeColorMap([1 1 0],[1 0 0],1000); 0 0 0]);
%             exportfigbo(f,[RPATH prefix '.fwe_black.png'],'png',10);
%         close(f);

        % overlay
        
        mydata = (template0/max(template0))/10+0.05;
        mydata(pval.C<0.05) = p(pval.C<0.05);
        mydata(mask==0) = -6666;

%         f=figure('Visible','off'); 
%             BoSurfStatViewsFlex( mydata, mask, vol0,  [0 0.15], view,varargin{:}); 
%             colormap([0 0 0; makeColorMap([1 1 0],[1 0 0],1/thresh); gray(4900)]);
%             exportfigbo(f,[RPATH prefix '.fwe.png'],'png',10);
%         close(f);
    end
    
    disp('Write volume files')
    %SurfStatWriteVol([NPATH prefix '.template.nii'],template0,vol0);
    %SurfStatWriteVol([NPATH prefix 'fwe_black.nii'],pval.C,vol0)
    %SurfStatWriteVol([NPATH prefix 'puncor.nii'],p,vol0); 
    %SurfStatWriteVol([NPATH prefix '.t.nii'],slm.t,vol0); 
    my_nii = template; 
    %my_nii.img = reshape(p,size(my_nii.img)); 
    save_nii(my_nii, [NPATH prefix '.template.tools.nii']); 
    
    maskedfeat = slm.t;
    maskedfeat(p>thresh) = 0; 
    SurfStatWriteVol([NPATH prefix '.t_pthresh.nii'],maskedfeat,vol0); 
    
    my_nii = template; 
    my_nii.img = reshape(maskedfeat,size(my_nii.img)); 
    save_nii(my_nii, [NPATH prefix '.t_pthresh.tools.nii']); 
    
    if exist('pval') && isfield(pval,'C') && any(pval.C<0.05) 
        
        maskedfeat = slm.t;
        maskedfeat(pval.C>0.05) = 0; 
        %SurfStatWriteVol([NPATH prefix '.t_fwethresh.nii'],maskedfeat,vol0); 
        my_nii = template; 
        my_nii.img = reshape(maskedfeat,size(my_nii.img)); 
        save_nii(my_nii, [NPATH prefix '.t_fwethresh.tools.nii']); 
        
    end
    
    [qval] = SurfStatQ(slm,mask>0); 
    min(qval.Q)
    if isfield(qval,'Q') && any(qval.Q<0.05);
        %SurfStatWriteVol([NPATH prefix '.fdr.nii'],maskedfeat,vol0);
        maskedfeat = slm.t;
        maskedfeat(qval.Q>0.05) = 0; 
        my_nii = template; 
        my_nii.img = reshape(maskedfeat,size(my_nii.img)); 
        save_nii(my_nii, [NPATH prefix '.t_fdrthresh.tools.nii']); 
%          f=figure('Visible','off'); 
%             BoSurfStatViewsFlex( mydata, mask, vol0,  [0 0.15], view,varargin{:}); 
%             colormap([0 0 0; makeColorMap([1 1 0],[1 0 0],1/thresh); gray(4900)]);
%             exportfigbo(f,[RPATH prefix '.q.png'],'png',10);
%         close(f);
    end
    
%     if isfield(qval,'Q') && any(qval.Q<0.1);
%         %SurfStatWriteVol([NPATH prefix '.fdr.nii'],maskedfeat,vol0);
%         maskedfeat = slm.t;
%         maskedfeat(qval.Q>0.05) = 0; 
%         my_nii = template; 
%         my_nii.img = reshape(maskedfeat,size(my_nii.img)); 
%         save_nii(my_nii, [NPATH prefix '.t_fdr_0.1_thresh.tools.nii']); 
%          f=figure('Visible','off'); 
%             BoSurfStatViewsFlex( mydata, mask, vol0,  [0 0.15], view,varargin{:}); 
%             colormap([0 0 0; makeColorMap([1 1 0],[1 0 0],1/thresh); gray(4900)]);
%             exportfigbo(f,[RPATH prefix '.q_01.png'],'png',10);
%         close(f);
%     end