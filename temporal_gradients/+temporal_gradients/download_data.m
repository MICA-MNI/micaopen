function download_data()
package_dir = regexp(mfilename('fullpath'),'.*\+temporal_gradients','match','once');
try
    websave([package_dir '/data/figure_data.mat'], 'https://box.bic.mni.mcgill.ca/s/M0WDuW61Q3eFL3t/download');
catch err
    if err.identifier == "MATLAB:webservices:CopyContentToDataStreamError"
        error('Error communicating with the server. Please try again later. If the issue persists try downloading directly from https://box.bic.mni.mcgill.ca/s/M0WDuW61Q3eFL3t through a webbrowser.');
    else
        rethrow(err)
    end
end