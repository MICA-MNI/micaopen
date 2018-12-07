function [Abs,group1big,group2big] = mica_permdiff_corrcoeff_alltails(group1, group2, num_rand)
% function [abs_corr_diff,perm_corr_diff_p] = mica_permdiff_corrcoeff(group1, group2, num_rand)

N1 = size(group1,1);
N2 = size(group2,1);
N_tgroup = N1 + N2;
tgroup_Reg = [group1;group2];


% compute absolute differences 
R_matrix1 = corrcoef(group1);
R_matrix2 = corrcoef(group2);

zdiff_a   = mica_zdiff(R_matrix1,R_matrix2,N1,N2);
Absdiff   = abs(zdiff_a); %abs(R_matrix1 - R_matrix2); 

Count     = zeros(size(Absdiff)); 
Count_G1  = zeros(size(Absdiff)); 
Count_G2  = zeros(size(Absdiff));

fprintf('\n\nCalculating correlation differences of randomized groups.\n')
for i = 1: num_rand

    fprintf('\n i = %d\n',i);
    %fprintf('-');    
    rp            = randperm(N_tgroup);
    rerand_corr_1 = (corrcoef(tgroup_Reg(rp(1:N1),:))) ;
    rerand_corr_2 = (corrcoef(tgroup_Reg(rp((N1+1):N_tgroup),:))) ;
    zdiff_p       = mica_zdiff(rerand_corr_1,rerand_corr_2,N1,N2);
    Permdiff      = abs(zdiff_p); 
    %Permdiff     = abs( (rerand_corr_1 - rerand_corr_2) ); 
    Adder         = Permdiff > Absdiff; 
    Count         = Count + Adder; 


end

abs_corr_diff    = Absdiff; 
perm_corr_diff_p = (Count+1) / (num_rand+1); 
perm_corr_diff_p = perm_corr_diff_p + diag(diag(ones(size(perm_corr_diff_p))));

