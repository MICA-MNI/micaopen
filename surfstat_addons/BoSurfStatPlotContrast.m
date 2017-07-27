function myclus = BoSurfStatPlotContrast(slm,contrast,S,clusp,mask, RPATH, PREFIX)
% myclus = BoSurfStatPlotContrast(slm,contrast,S,clusp,mask, RPATH, PREFIX)
% Y      is thickness data [n x 5k] 
%        group is PATIENT controls 
% SW     surface file
% SInf   inflated surface
% clusp  cluster threshold. eg. 0.01 
% mask   [1 x 5k]
% RPATH  write files in this directory
% PREFIX use this as prefix

mc     = [zeros(1,3)*0.8; 
          zeros(127,1)   (0:126)'/127   ones(127,1)];
mycol  =  flipud(mc);

mc2         = [ makeColorMap([1 1 0],[1 0 0],[0 0 0],512/4); ...
                makeColorMap([0 0 0],[0.7 0.7 0.7],[0 0 0],512/4); ...
                makeColorMap([0 0 0],[0 0 1],[0 1 1],512/4)];
mc2 = flipud(mc2);            
%mc2(1:4,:)    = [];
%mc2(end-4:end,:)  = [];

slm     = SurfStatT(slm, contrast); 
slm.t   = slm.t.*mask; 
puncorr = 1 - tcdf(slm.t.*mask,slm.df);
[pval,peak,clus,clusid] = SurfStatP(slm,mask,clusp);


f=figure;
    BoSurfStatViewData(slm.t,S,[ PREFIX ' t']);
    SurfStatColLim([-5 5]);
    colormap(mc2);
    exportfigbo(f,...
            [RPATH PREFIX '.t.png'],'png',10);
close(f);

f=figure;
    BoSurfStatViewData(puncorr,S,[ PREFIX ' p']);
     colormap(mycol);
    SurfStatColLim([0 clusp]);
    exportfigbo(f,...
            [RPATH PREFIX '.p.' num2str(clusp) '.png'],'png',10);
close(f);

if isfield(pval,'C') & any(pval.C < 0.05)
    
    f=figure;
        BoSurfStatViewData(pval.C,S,[PREFIX ' fwe']);
        colormap(mycol);
        SurfStatColLim([0 0.05]);
        exportfigbo(f,...
            [RPATH PREFIX '.fwe.' num2str(clusp) '.png'],'png',10);
    close(f);


    myclus.fwe = pval.C; 
    myclus.clus = clus; 
    myclus.clusid = clusid; 
    myclus.peak = peak;
end
 myclus.puncorr = puncorr;
 myclus.t = slm.t; 