function [f, ca, o] = mica_spider(data,tle,rng,lbl,col,ax)
% create a spider plot for ranking the data
% function [f, ca, o] = spider(data,tle,rng,lbl,leg,f)
%
% inputs  6 - 5 optional
% data    input data (NxM) (# axes (M) x # data sets (N))     class real
% tle     spider plot title                                   class char
% rng     peak range of the data (Mx1 or Mx2)                 class real
% lbl     cell vector axes names (Mxq) in [name unit] pairs   class cell
% leg     data set legend identification (1xN)                class cell
% f       figure handle or plot handle                        class real
%
% outptus 3 - 3 optional
% f       figure handle                                       class integer
% x       axes handle                                         class real
% o       series object handles                               class real
%
% michael arant - jan 30, 2008
%
% to skip any parameter, enter null []
% 
% examples
% 
%  	spider([1 2 3; 4 5 6; 7 8 9; 10 11 12; 13 14 15;16 17 18; ...
%  	19 20 21; 22 23 24; 25 26 27]','test plot');
% 
%  	spider([1 2 3 4; 4 5 6 7; 7 8 9 10; 10 11 12 13; 13 14 15 16; ...
%  	16 17 18 19; 19 20 21 22; 22 23 24 25; 25 26 27 28],'test plot', ...
%  	[[0:3:24]' [5:3:29]'],[],{'Case 1' 'Case 2' 'Case 3' 'Case 4'});
% 
%  	spider([1 2 3 4; 4 5 6 7; 7 8 9 10; 10 11 12 13; 13 14 15 16; ...
%  	16 17 18 19; 19 20 21 22; 22 23 24 25; 25 26 27 28],'test plot', ...
%  	[],[],{'Case 1' 'Case 2' 'Case 3' 'Case 4'});
%
% 	figure; clf; set(gcf,'color','w'); s = zeros(1,4);
%  	for ii = 1:4; s(ii) = subplot(2,2,ii); end
%  	 
%  	spider([1 2 3; 4 5 6; 7 8 9; 10 11 12; 13 14 15;16 17 18; ...
%  	19 20 21; 22 23 24; 25 26 27]','test plot 1',[],[],[],s(1));
% 
% 	spider([1 2 3; 4 5 6; 7 8 9; 10 11 12; 13 14 15;16 17 18; ...
%  	19 20 21; 22 23 24; 25 26 27],'test plot 2',[0 30],[],[],s(2));
% 
%  	spider([1 2 3 4; 4 5 6 7; 7 8 9 10; 10 11 12 13; 13 14 15 16; ...
%  	16 17 18 19; 19 20 21 22; 22 23 24 25; 25 26 27 28]','test plot 3', ...
% 	[0 30],{'Label 1' 'Unit 1'; 'Label 2' 'Unit 2'; 'Label 3' 'Unit 3'; ...
%  	'Label 4' 'Unit 4'},{'Case 1' 'Case 2' 'Case 3' 'Case 4' 'Case 5' ...
%  	'Case 6' 'Case 7' 'Case 8' 'Case 9'},s(3));
% 
%  	spider([1 2 3 4; 4 5 6 7; 7 8 9 10; 10 11 12 13; 13 14 15 16; ...
%  	16 17 18 19; 19 20 21 22; 22 23 24 25; 25 26 27 28],'test plot 4', ...
%  	[[0:3:24]' [5:3:29]'],[],{'Case 1' 'Case 2' 'Case 3' 'Case 4'},s(4));

% data check
if nargin < 1; help spider; error('Need data to plot'); end

% size segments and number of cases
[r c] = size(data);
% exit for too few axes
if r < 3
	errordlg('Must have at least three measuremnt axes')
	error('Program Termination:  Must have a minimum of three axes')
end

% title
if ~exist('tle','var') || isempty(tle) || ~ischar(tle)
	tle = '';
end

% check for maximum range
if ~exist('rng','var') || isempty(rng) || ~isreal(rng)
	% no range given or range is in improper format
	% define new range
	rng = [min([min(data,[],2) zeros(r,1)],[],2) max(data,[],2)];
	% check for negative minimum values
	if ~isempty(ismember(-1,sign(data)))
		% negative value found - adjust minimum range
		for ii = 1:r
			% negative range for axis ii - set new minimum
			if min(data(ii,:)) < 0
				rng(ii,1) = min(data(ii,:)) - ...
							0.25 * (max(data(ii,:)) - min(data(ii,:)));
			end
		end
	end
elseif size(rng,1) ~= r
	if size(rng,1) == 1
		% assume that all axes have commom scale
		rng = ones(r,1) * rng;
	else
		% insuffent range definition
		uiwait(msgbox(char('Range size must be Mx1 - number of axes x 1', ...
			sprintf('%g axis ranges defined, %g axes exist',size(rng,1),r))))
		error(sprintf('%g axis ranges defined, %g axes exist',size(rng,1),r))
	end
elseif size(rng,2) == 1
	% assume range is a maximum range - define minimum
	rng = sort([min([zeros(r,1) min(data,[],2) - ...
						0.25 * (max(data,[],2) - min(data,[],2))],[],2) rng],2);
end

% check for axis labels
if ~exist('lbl','var') || isempty(lbl)
	% no labels given - define a default lable
	lbl = cell(r,1); for ii = 1:r; lbl(ii) = cellstr(sprintf('Axis %g',ii)); end
elseif size(lbl,1) ~= r
	if size(lbl,2) == r
		lbl = lbl';
	else
		uiwait(msgbox(char('Axis labels must be Mx1 - number of axes x 1', ...
			sprintf('%g axis labels defined, %g axes exist',size(lbl,1),r))))
		error(sprintf('%g axis labels defined, %g axes exist',size(lbl,1),r))
	end
elseif ischar(lbl)
	% check for charater labels
	lbl = cellstr(lbl);
end




ca = ax; 
cla(ca); 

hold on

% set the axes to the current text axes
axes(ax)
% set to add plot
set(ax,'nextplot','add');

% clear figure and set limits
set(ca,'visible','off'); %set(f,'color','w')
set(ca,'xlim',[-1.25 1.25],'ylim',[-1.25 1.25]); axis(ca,'equal','manual')
% title
text(0,1.3,tle,'horizontalalignment','center','fontweight','bold');


% scale by range
angw = linspace(0,2*pi,r+1)';
mag = (data - rng(:,1) * ones(1,c)) ./ (diff(rng,[],2) * ones(1,c));
% scale trimming
mag(mag < 0) = 0; mag(mag > 1) = 1;
% wrap data (close the last axis to the first)
ang = angw(1:end-1); angwv = angw * ones(1,c); magw = [mag; mag(1,:)];


% make the plot
% define the axis locations
start = [zeros(1,r); cos(ang')]; stop = [zeros(1,r); sin(ang')];
% plot the axes
plot(ca,start,stop,'color',[.6 .6 .6],'linestyle','-'); axis equal
% plot axes markers
inc = 0.25:.25:1; mk = .025 * ones(1,4); tx = 4 * mk; tl = 0:.25:1;
% loop each axis ang plot the line markers and labels
% add axes
for ii = 1:r
	% plot tick marks
	tm = plot(ca,[[cos(ang(ii)) * inc + sin(ang(ii)) * mk]; ...
			[cos(ang(ii)) * inc - sin(ang(ii)) * mk]], ...
			[[sin(ang(ii)) * inc - cos(ang(ii)) * mk] ;
			[sin(ang(ii)) * inc + cos(ang(ii)) * mk]],'color',[ .6 .6 .6]);
	% label the tick marks
    if ii == 1
        for jj = [1 4]
    % 		temp = text([cos(ang(ii)) * inc(jj) + sin(ang(ii)) * tx(jj)], ...
    % 				[sin(ang(ii)) * inc(jj) - cos(ang(ii)) * tx(jj)], ...
    % 				num2str(chop(rng(ii,1) + inc(jj)*diff(rng(ii,:)),2)), ...
    % 				'fontsize',8);
            temp = text([cos(ang(ii)) * inc(jj) + sin(ang(ii)) * tx(jj)], ...
                    [sin(ang(ii)) * inc(jj) - cos(ang(ii)) * tx(jj)], ...
                    num2str(rd(rng(ii,1) + inc(jj)*diff(rng(ii,:)),-2)), ...
                    'fontsize',8);
            temp.Color = [.6 .6 .6];     
            % flip the text alignment for lower axes
            if ang(ii) >= pi
                set(temp,'HorizontalAlignment','right')
            end
        end
	end
	% label each axis
	temp = text([cos(ang(ii)) * 1.1 + sin(ang(ii)) * 0], ...
			[sin(ang(ii)) * 1.1 - cos(ang(ii)) * 0], ...
			char(lbl(ii,:)));
	% flip the text alignment for right side axes
	if ang(ii) > pi/2 && ang(ii) < 3*pi/2
		set(temp,'HorizontalAlignment','right')
	end
end


% plot the data
o = polar(ca,angw*ones(1,c),magw);
% set color of the lines
for ii = 1:c; 
    set(o(ii),'color',col(ii,:),'linewidth',1.5); 
end

% apply the legend
% temp = legend(o,leg,'location','best');

return

function [v] = rd(v,dec)
% quick round function (to specified decimal)
% function [v] = rd(v,dec)
%
% inputs  2 - 1 optional
% v       number to round    class real
% dec     decimal loaction   class integer
%
% outputs 1
% v       result             class real
%
% positive dec shifts rounding location to the right (larger number)
% negative dec shifts rounding location to the left (smaller number)
%
% michael arant
% Michelin Maericas Research and Development Corp
if nargin < 1; help rd; error('I/O error'); end

if nargin == 1; dec = 0; end

v = v / 10^dec;
v = round(v);
v = v * 10^dec;

function [val] = color_index(len)
% get unique colors for each item to plot
% function [val] = color_index(len)
%
% inputs  1
% len     number of objects     class integer
%
% outputs 1
% val     color vector          class real
%
% michael arant

if nargin < 1 || nargout < 1; help color_index; error('I / O error'); end

if len == 1
	val = [0 0 0];
else
	% initial color posibilities (no white)
	% default color scale
	col = [	0 0 0
			0 0 1
			0 1 1
			0 1 0
			1 1 0
			1 0 1
			1 0 0];

	% reduce if fewer than 6 items are needed (no interpolation needed)
	switch len
		case 1, col([2 3 4 5 6 7],:) = [];
		case 2, col([2 3 4 5 6],:) = [];
		case 3, col([3 4 5 6],:) = [];
		case 4, col([3 5 6],:) = [];
		case 5, col([5 6],:) = [];
		case 6, col(6,:) = [];
	end

	% number of requested colors
	val = zeros(len,3); val(:,3) = linspace(0,1,len)';

	% interpolate to fill in colors
	val(:,1) = interp1q(linspace(0,1,size(col,1))',col(:,1),val(:,3));
	val(:,2) = interp1q(linspace(0,1,size(col,1))',col(:,2),val(:,3));
	val(:,3) = interp1q(linspace(0,1,size(col,1))',col(:,3),val(:,3));
end

function [res] = isint(val)
% determines if value is an integer
% function [res] = isint(val)
%
% inputs  1
% val     value to be checked              class real
%
% outputs 1
% res     result (1 is integer, 0 is not)  class integer
%
% michael arant     may 15, 2004
if nargin < 1; help isint; error('I / O error'); end

% numeric?
if ~isnumeric(val); error('Must be numeric'); end

% check for real number
if isreal(val) & isnumeric(val)
%	check for integer
	if round(val) == val
		res = 1;
	else
		res = 0;
	end
else
	res = 0;
end

