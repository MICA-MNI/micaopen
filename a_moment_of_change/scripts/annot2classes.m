function classes = annot2classes(lh_annot, rh_annot, hemi_split)

% converts the labels in a freesurfer annotation file into a vector
% where the classes correspond to the order in the color look up table
%
% input:
% lh_annot          filename of left annotation file
% rh_annot          filename of right annotation file
% hemi_split        logical value (0 or 1) stating whether the count should
%                   continue to increase from the left to right. If 0, the same order is
%                   presumed in left and right hemispheres.
%
% output:
% classes           vector the length of vertices in left and right
%                   hemisphere combined


[~, lh_l, lh_ctb] = read_annotation(lh_annot);
[~, rh_l, rh_ctb] = read_annotation(rh_annot);
classes = zeros(length(lh_l), 1);
for ii = 1:length(lh_l)
    which_row = find(lh_ctb.table(:,5) == lh_l(ii));
    if lh_l(ii) == 0
        classes(ii) = 0;
    elseif isempty(which_row)
        classes(ii) = 0;
    else
        classes(ii) = which_row;
    end
end
for ii = 1:length(rh_l)
    which_row = find(rh_ctb.table(:,5) == rh_l(ii));
    if rh_l(ii) == 0
        classes(ii+length(lh_l)) = 0;
    elseif isempty(which_row)
        classes(ii) = 0;
    else
        if hemi_split == 1
            classes(ii+length(lh_l)) = which_row + length(lh_ctb.table(:,5));
        else
            classes(ii+length(lh_l)) = which_row;
        end
    end
end