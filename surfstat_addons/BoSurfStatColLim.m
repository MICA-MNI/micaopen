function cb=BoSurfStatViewColLim(clim);

%SurfStatViewColLim sets the colour limits for SurfStatView.
%
% Usage: cb = SurfStatViewColLim(clim);
%
% clim = [min, max] values of data for colour limits.
%
% cb   = handle to new colorbar.

a=get(gcf,'Children');
n=length(a);
for i=1:n
    tag = get(a(i),'Tag');
    if length(tag) > 12 & strcmp(tag(1:12),'SurfStatView')
        set(a(i),'CLim',clim);
    end
    if strcmp(tag,'Colorbar')
        title=get(get(a(i),'Title'),'String');
        delete(a(i));
    end
end
colorbar off;
cb=colorbar('location','South');
set(cb,'Position',[0.35 0.22 0.3 0.03]);
set(get(cb,'Title'),'String',title);

return
end
