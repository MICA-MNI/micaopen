function metric_scatter_3d(coord,z,clim,filename,cmap)
% Core function for 3D scatter plots
%
%   METRIC_SCATTER(coord,z,clim,filename,cmap) creates a 3D scatter plot
%   where points have coordinates coord and intensities z. The color limits
%   are set with clim. The figure is stored as a .png file in filename. A
%   colormap may be defined with cmap. If cmap is not included then it
%   defaults to parula.

if ~exist('cmap','var')
    cmap = parula;
end

h.figure = figure('Color','w');
h.axes = axes;
h.sct = scatter3(coord(:,1),coord(:,2),coord(:,3),200,z,'.');
colormap(cmap)
xlabel('Gradient 1')
ylabel('Gradient 2')
zlabel('Gradient 3')
set(h.axes                                          , ...
    'PlotBoxAspectRatio'    , [1 1 1]               , ...
    'DataAspectRatio'       , [1 1 1]               , ...
    'XLim'                  , [-4 4]                , ...
    'XTick'                 , [-4 0 4]              , ...
    'YLim'                  , [-4 4]                , ...
    'YTick'                 , [-4 0 4]              , ...
    'ZLim'                  , [-4 4]                , ...
    'ZTick'                 , [-4 0 4]              , ...
    'FontName'              , 'DroidSans'           , ...
    'FontSize'              , 22                    );
caxis(clim)
grid on

export_fig(char(filename), '-m2', '-png');
close(gcf); 
end