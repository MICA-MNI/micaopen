function colour_coding = colour2gradients(G1, G2)

% colour_coding = colour2gradients(G1, G2)
% colours nodes by their proximity to the apex of the triangles in 2d
% gradient space
% G1max ~ red
% G2max ~ green
% G2min ~ blue
%
% written in November 2018, Casey Paquola

G1peak = max(G1);
G2min = min(G2);
G2max = max(G2);

for ii = 1:length(G1)
    
    if G1(ii) > 0
        colourness(ii,1) = 1 - (G1peak - G1(ii));
    else
        colourness(ii,1) = 1 - (G1peak + abs(G1(ii)));
    end
    if G2(ii) > 0
        colourness(ii,2) = 1 - (abs(G2min) + G2(ii));
        colourness(ii,3) = 1 - (G2max- G2(ii));
    else
        colourness(ii,2) = 1 - (abs(G2min) - abs(G2(ii)));
        colourness(ii,3) = 1 - (G2max + abs(G2(ii)));
    end
    
end

for col = 1:3
    colour_coding(:,col) = rescale(colourness(:,col), 0, 1);
end