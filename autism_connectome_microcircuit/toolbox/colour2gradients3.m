function colour_coding = colour2gradients3(G1, G2, G3)
% colour_coding = colour2gradients3(G1, G2, G3)
% colours nodes by their proximity to the apex of the triangles in 2d
% gradient space
% G1max ~ red
% G2max ~ green
% G3max ~ blue
%
% written in November 2018, Casey Paquola

G1max = max(G1);
G2max = max(G2);
G3max = max(G3);

for ii = 1:length(G1)
    
    if G1(ii) > 0
        colourness(ii,1) = 1 - (G1max - G1(ii));
    else
        colourness(ii,1) = 1 - (G1max + abs(G1(ii)));
    end
    if G2(ii) > 0
        colourness(ii,2) = 1 - (G2max- G2(ii));
    else
        colourness(ii,2) = 1 - (G2max + abs(G2(ii)));
    end
    if G3(ii) > 0
        colourness(ii,3) = 1 - (G3max- G3(ii));
    else
        colourness(ii,3) = 1 - (G3max + abs(G3(ii)));
    end
end

for col = 1:3
    colour_coding(:,col) = rescale(colourness(:,col), 0, 1);
end
