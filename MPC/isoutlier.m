function [tf, lthresh, uthresh, center] = isoutlier(a,varargin)
% ISOUTLIER Find outliers in data
%   TF = ISOUTLIER(A) returns a logical array whose elements are true when 
%   an outlier is detected in the corresponding element. An outlier is an 
%   element that is greater than 3 scaled median absolute deviation (MAD) away 
%   from the median. The scaled MAD is defined as K*MEDIAN(ABS(A-MEDIAN(A))) 
%   where K is the scaling factor and is approximately 1.4826. If A is a 
%   matrix or a table, ISOUTLIER operates on each column separately. If A is
%   an N-D array, ISOUTLIER operates along the first array dimension
%   whose size does not equal 1.
%
%   TF = ISOUTLIER(A, METHOD) specifies the method to determine outliers, 
%   where METHOD is one of the following:
%     'median'    - Returns all elements more than 3 scaled MAD from the 
%                   median. This is the default.
%     'mean'      - Returns all elements more than 3 standard deviations 
%                   from the mean. This is also known as the three-sigma 
%                   rule, and is a fast but less robust method.
%     'quartiles' - Returns all elements more than 1.5 interquartile ranges 
%                   (IQR) above the upper quartile or below the lower quartile.
%                   This method makes few assumptions about data distribution,
%                   and is appropriate if A is not normally distributed.
%     'grubbs'    - Applies Grubbs' test for outliers, which is an iterative 
%                   method that removes one outlier per iteration until no
%                   more outliers are found. This method uses formal statistics
%                   of hypothesis testing and gives more objective reasoning backed
%                   by statistics behind its outlier identification. It assumes normal 
%                   distribution and may not be appropriate if A is not normal.
%     'gesd'      - Applies the generalized extreme Studentized deviate
%                   test for outliers. Like 'grubbs', this is another iterative
%                   method that removes one outlier per iteration. It may offer 
%                   improved performance over 'grubbs' when there are multiple
%                   outliers that mask one another.
%
%   TF = ISOUTLIER(A, MOVMETHOD, WL) uses a moving window method to determine 
%   contextual outliers instead of global outliers. Contextual outliers are 
%   outliers in the context of their neighborhood, and may not be the
%   maximum or minimum values in A. MOVMETHOD can be:
%     'movmedian' - Returns all elements more than 3 local scaled MAD from 
%                   the local median, over a sliding window of length WL.
%     'movmean'   - Returns all elements more than 3 local standard deviations 
%                   from the local mean, over a sliding window of length WL.
%   WL is the length of the moving window. It can either be a scalar or a
%   two-element vector, which specifies the number of elements before and
%   after the current element.
%
%   TF = ISOUTLIER(..., DIM) specifies the dimension to operate along.
%
%   TF = ISOUTLIER(..., 'ThresholdFactor', P) modifies the outlier detection 
%   thresholds by a factor P. For the 'grubbs' and 'gesd' methods, P is a 
%   scalar between 0 and 1. For all other methods, P is a nonnegative 
%   scalar. See the documentation for more information.
%
%   TF = ISOUTLIER(...,'SamplePoints',X) specifies the sample points 
%   X representing the location of the data in A, which is used by moving 
%   window methods. X must be a numeric or datetime vector, and must be 
%   sorted with unique elements. For example, X can specify time stamps for 
%   the data in A. By default, outliers uses data sampled uniformly at 
%   points X = [1 2 3 ... ].
%        
%   TF = ISOUTLIER(...,'DataVariables', DV) finds outliers only in the table 
%   variables specified by DV. The default is all table variables in A. DV 
%   must be a table variable name, a cell array of table variable names, a 
%   vector of table variable indices, a logical vector, or a function handle 
%   that returns a logical scalar (such as @isnumeric). TF has the same size as A.
%
%   TF = ISOUTLIER(..., 'MaxNumOutliers', MAXN) specifies the maximum number 
%   of outliers for the 'gesd' method only. The default is 10% of the number 
%   of elements. Set MAXN to a larger value to ensure it returns all outliers. 
%   Setting MAXN too large can reduce efficiency.
%
%   [TF, LTHRESH, UTHRESH, CENTER] = ISOUTLIER(...) also returns the
%   lower threshold, upper threshold, and the center value used by the 
%   outlier detection method.
%
%   Examples:
%      % Detect outliers in a data vector
%      x = [60 59 49 49 58 1000 61 57 48 62];
%      tf = isoutlier(x);
%
%   Class support for input A:
%      float: double, single
%      table, timetable
%
%   See also FILLOUTLIERS, SMOOTHDATA, FILLMISSING, RMMISSING,
%            ISLOCALMAX, ISLOCALMIN, ISCHANGE, ISMISSING

%   Copyright 2016-2017 The MathWorks, Inc.

[method, wl, dim, p, sp, vars, maxoutliers] = parseinput(a, varargin);
dim = min(dim, ndims(a)+1);

xistable = matlab.internal.datatypes.istabular(a);

if xistable
    tf = false(size(a));
    if nargout > 1
        if ismember(method, {'movmedian', 'movmean'})
            % with moving methods, the thresholds and center have the same
            % size as input
            lthresh = a(:,vars);
        else
            % with other methods, thresholds and center has reduced
            % dimension along first dimension
            lthresh = a(1,vars);
        end
        uthresh = lthresh;
        center = lthresh;
    end
    for i = 1:length(vars)
        vari = a.(vars(i));
        if ~(isempty(vari) || iscolumn(vari))
            error(message('MATLAB:isoutlier:NonColumnTableVar'));
        end
        if ~isfloat(vari)
            error(message('MATLAB:isoutlier:NonfloatTableVar',...
                a.Properties.VariableNames{vars(i)}, class(vari)));
        end
        if ~isreal(vari)
            error(message('MATLAB:isoutlier:ComplexTableVar'));
        end
        [out, lt, ut, c] = locateoutliers(vari, method, wl, p, ...
            sp, maxoutliers);
        tf(:,vars(i)) = any(out,2);
        if nargout > 1
            lthresh.(i) = lt;
            uthresh.(i) = ut;
            center.(i) = c;
        end
    end
else
    asparse = issparse(a);
    % Avoid overhead for unnecessary permute calls
    if (dim > 1) && ~isscalar(a)
        dims = 1:max(ndims(a),dim);
        dims(1) = dim;
        dims(dim) = 1;
        if asparse && dim > 2
            % permuting beyond second dimension not supported for sparse
            a = full(a);
        end
        a = permute(a, dims);
    end
    [tf, lthresh, uthresh, center] = locateoutliers(a, method, ...
        wl, p, sp, maxoutliers);
    
    if (dim > 1) && ~isscalar(a)
        tf = ipermute(tf, dims);
        if asparse
            % explicitly convert to sparse. If dim > 2, we have converted
            % to full previously
            tf = sparse(tf);
        end
        if nargout > 1
            lthresh = ipermute(lthresh, dims);
            uthresh = ipermute(uthresh, dims);
            center = ipermute(center, dims);
            if asparse
                lthresh = sparse(lthresh);
                uthresh = sparse(uthresh);
                center = sparse(center);
            end
        end
    end
end

function [method, wl, dim, p, samplepoints, datavariables, maxoutliers] = ...
    parseinput(a, input)
method = 'median';
wl = [];
p = [];
dim = [];
samplepoints = [];
datavariables = [];
maxoutliers = [];
funcname = mfilename;

validateattributes(a,{'single','double','table','timetable'}, {'real'}, funcname, 'A', 1);
aistable = matlab.internal.datatypes.istabular(a);
if aistable
    datavariables = 1:width(a);
end

if ~isempty(input)
    i = 1;
    % parse methods and movmethod
    if ischar(input{i}) || isstring(input{i})
        str = validatestring(input{i},{'median', 'mean', 'quartiles', 'grubbs', ...
            'gesd', 'movmedian', 'movmean', 'SamplePoints', ...
            'DataVariables', 'ThresholdFactor', 'MaxNumOutliers'}, i+1);
        if ismember(str, {'median', 'mean', 'quartiles', 'grubbs','gesd'})
            % method
            method = str;
            i = i+1;
        elseif ismember(str, {'movmedian', 'movmean'})
            % movmethod
            method = str;
            if isscalar(input)
                error(message('MATLAB:isoutlier:MissingWindowLength',method));
            end
            wl = input{i+1};
            if (isnumeric(wl) && isreal(wl)) || islogical(wl) || isduration(wl) 
                if isscalar(wl)
                    if wl <= 0 || ~isfinite(wl) 
                        error(message('MATLAB:isoutlier:WindowLengthInvalidSizeOrClass'));
                    end
                elseif numel(wl) == 2
                    if any(wl < 0 | ~isfinite(wl)) 
                        error(message('MATLAB:isoutlier:WindowLengthInvalidSizeOrClass'));
                    end
                else
                    error(message('MATLAB:isoutlier:WindowLengthInvalidSizeOrClass'));
                end       
            else
                error(message('MATLAB:isoutlier:WindowLengthInvalidSizeOrClass'));
            end
            i = i+2;
        end
    end
    % parse dim
    if i <= length(input)
        if ~(ischar(input{i}) || isstring(input{i}))
            validateattributes(input{i},{'numeric'}, {'scalar', 'integer', 'positive'}, ...
                funcname, 'dim', i+1);
            dim = input{i};
            i = i+1;
        end
        
        % parse N-V pairs
        inputlen = length(input);
        if rem(inputlen - i + 1,2) ~= 0
            error(message('MATLAB:isoutlier:ArgNameValueMismatch'))
        end
        for i = i:2:inputlen
            name = validatestring(input{i}, {'SamplePoints', ...
                'DataVariables', 'ThresholdFactor', 'MaxNumOutliers'}, i+1);
            
            value = input{i+1};
            switch name
                case 'SamplePoints'
                    if istimetable(a)
                        error(message('MATLAB:isoutlier:SamplePointsTimeTable'));
                    end
                    if isfloat(value)
                        validateattributes(value,{'double','single'}, {'vector', 'increasing', 'finite', 'real'},...
                            funcname, 'SamplePoints', i+2)
                    elseif isdatetime(value) || isduration(value)
                        if ~(isvector(value) && issorted(value) &&  ...
                                length(unique(value))==length(value) && all(isfinite(value)))
                            error(message('MATLAB:isoutlier:InvalidSamplePoints'));
                        end
                    else
                        error(message('MATLAB:isoutlier:SamplePointsInvalidClass'));
                    end
                    samplepoints = value;
                case 'DataVariables'
                    if aistable
                        datavariables = unique(...
                            matlab.internal.math.checkDataVariables(a,value,'isoutlier'));
                    else
                        error(message('MATLAB:isoutlier:DataVariablesNonTable',class(a)));
                    end
                case 'ThresholdFactor'
                    validateattributes(value,{'numeric'}, {'real', 'scalar', ...
                        'nonnegative', 'nonnan'}, funcname, 'ThresholdFactor', i+2);
                    p = double(value);
                case 'MaxNumOutliers'
                    validateattributes(value,{'numeric'}, {'scalar', 'positive', ...
                        'integer'}, funcname, 'MaxNumOutliers', i+2);
                    maxoutliers = double(value);
            end
        end
    end
end
if isempty(p)  % default p
    switch method
        case {'median','mean','movmedian','movmean'}
            p = 3;
        case 'quartiles'
            p = 1.5;
        otherwise % grubbs, gesd
            p = 0.05;
    end
elseif ismember(method, {'grubbs', 'gesd'})
    if p > 1
        error(message('MATLAB:isoutlier:AlphaOutOfRange'));
    end
end

% dim
if isempty(dim)
    if aistable
        dim = 1;
    else
        dim = find(size(a) ~= 1,1);
        if isempty(dim)  % scalar x
            dim = 1;
        end
    end
elseif aistable && dim ~= 1
    error(message('MATLAB:isoutlier:TableDim'));
end

if ~isempty(maxoutliers)
    if ~strcmp(method, 'gesd')
        error(message('MATLAB:isoutlier:MaxNumOutliersGesdOnly'));
    elseif maxoutliers > size(a,dim)
        error(message('MATLAB:isoutlier:MaxNumOutliersTooLarge'));
    end
end

if ~isempty(samplepoints) && ~isequal(numel(samplepoints),size(a,dim))
    error(message('MATLAB:isoutlier:SamplePointsInvalidSize'));
end
if (isdatetime(samplepoints) || isduration(samplepoints)) && ...
        ~isempty(wl) && ~isduration(wl)
    error(message('MATLAB:isoutlier:SamplePointsNonDuration'));
end
if istimetable(a)
    samplepoints = a.Properties.RowTimes;
end



