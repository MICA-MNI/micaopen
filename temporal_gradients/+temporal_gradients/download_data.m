function download_data()
package_dir = regexp(mfilename('fullpath'),'.*\+temporal_gradients','match','once');
websave([package_dir '/data/figure_data.mat'], 'https://box.bic.mni.mcgill.ca/s/M0WDuW61Q3eFL3t/download');
end