global order
global orderLag

numgood=0;
tries=1000;
for i=1:tries
    good = CreateOrder_AllShort();
    numgood = numgood + good;
    if good
        csvwrite(sprintf('order_%d.txt',numgood),[order orderLag])
    end
%     if numgood == 30
%         break
%    end
end

numgood/tries
