//
//  canvas.cpp
//  BPSO
//
//  Created by Craig Stark on 11/17/11.
//  Copyright 2011 Craig Stark. All rights reserved.
//

#include "wx/wxprec.h"
#ifndef WX_PRECOMP
#include "wx/wx.h"
#endif
#include <wx/app.h>
#include <wx/filename.h>
#include <wx/stdpaths.h>
#include <wx/image.h>
#include <wx/dcbuffer.h>
#include <wx/utils.h>
#include <wx/font.h>


#include "main.h"
#include "parameters.h"

extern c_DisplayFrame *MainFrame;

BEGIN_EVENT_TABLE(c_DisplayCanvas, wxWindow)
EVT_PAINT(c_DisplayCanvas::OnPaint)
EVT_KEY_DOWN(c_DisplayCanvas::OnKey)
EVT_LEFT_DOWN(c_DisplayCanvas::OnLMouseClick)
//EVT_ERASE_BACKGROUND(MyCanvas::OnErase)
END_EVENT_TABLE()

c_DisplayCanvas::c_DisplayCanvas(wxWindow *parent,int xsize,int ysize):
wxWindow(parent, wxID_ANY,wxPoint(0,0),wxSize(xsize,ysize))  {
    DisplayedImage = NULL;
    DisplayState = 0;
    Response = 0;
	DisplayedImage = new wxImage(xsize,ysize,true);
	SetBackgroundStyle(wxBG_STYLE_CUSTOM);
	SetBackgroundColour(wxColour((unsigned char) 255, (unsigned char) 255,(unsigned char) 255));
}


void c_DisplayCanvas::OnPaint(wxPaintEvent& WXUNUSED(event)) {
    wxAutoBufferedPaintDC dc(this);
    wxArrayString TouchLabels;

    wxMemoryDC memDC;
    if (DisplayedImage && !DisplayedImage->IsOk())
        return;
 //   if (DisplayState == DISP_Idle)
 //       return;
    //   PrepareDC(dc);
    wxSize sz = dc.GetSize();
    
    dc.SetFont(dc.GetFont().Scaled(2));
    static int i=0;
	i++;
    MainFrame->SetStatusText(wxString::Format("Resp %d %d",Response, i));
    if (DisplayState == DISP_Blank) // ISI
        dc.Clear();
    else if (DisplayState == DISP_Stim) { // Show image
        wxBitmap TempBitmap = wxBitmap(*DisplayedImage,24);
        memDC.SelectObject(TempBitmap);
        int xsize = DisplayedImage->GetWidth();
        int ysize = DisplayedImage->GetHeight();
        dc.Clear();
        dc.Blit((sz.GetWidth()-xsize)/2, (sz.GetHeight()-ysize)/2, xsize , ysize, &memDC, 0, 0, wxCOPY, false);
    }
    else if (DisplayState == DISP_StudyInstructions) { // Study instructions
        dc.Clear();
        wxString instructs = _("Indoor or Outdoor?");
        wxSize t_sz = dc.GetTextExtent(instructs);
        dc.DrawText(instructs,
                    wxPoint((sz.GetWidth()-t_sz.GetWidth())/2, (sz.GetHeight()-t_sz.GetHeight())/2 - t_sz.GetHeight()));
        instructs = _("Press spacebar to start");
        t_sz = dc.GetTextExtent(instructs);
        dc.DrawText(instructs,
                    wxPoint((sz.GetWidth()-t_sz.GetWidth())/2, (sz.GetHeight()-t_sz.GetHeight())/2 + t_sz.GetHeight()));
    }
    else if (DisplayState == DISP_TestInstructions) { // Test instructions
        dc.Clear();
        wxString instructs = _("Old, Similar, or New?");
		if (P_2ChoiceTest)
			instructs = _("Old or New?");

        wxSize t_sz = dc.GetTextExtent(instructs);
        dc.DrawText(instructs,
                    wxPoint((sz.GetWidth()-t_sz.GetWidth())/2, (sz.GetHeight()-t_sz.GetHeight())/2 - t_sz.GetHeight()));
        instructs = _("Press spacebar to start");
        t_sz = dc.GetTextExtent(instructs);
        dc.DrawText(instructs,
                    wxPoint((sz.GetWidth()-t_sz.GetWidth())/2, (sz.GetHeight()-t_sz.GetHeight())/2 + t_sz.GetHeight()));
    }
    else if (DisplayState == DISP_Idle) {
        if (Logo && Logo->IsOk()) {
            wxBitmap TempBitmap = wxBitmap(*Logo,24);
            memDC.SelectObject(TempBitmap);
            int xsize = Logo->GetWidth();
            int ysize = Logo->GetHeight();
            dc.Clear();
            dc.Blit((sz.GetWidth()-xsize)/2, (sz.GetHeight()-ysize)/2, xsize , ysize, &memDC, 0, 0, wxCOPY, false);
           
        }
    }
    //  dc.DrawText(wxNow(),wxPoint(10,10));
    if ((P_AllowTouch) && (DisplayState != DISP_Idle)) {
        wxSize WindowSize = GetSize();
        dc.SetPen(*wxBLACK_DASHED_PEN);
		wxSize t_sz;
        if (P_NPossibleResponses == 2) {
            dc.DrawLine(WindowSize.x / 2,WindowSize.y,WindowSize.x / 2,(90 * WindowSize.y) / 100);
			if (P_TouchLabels.Count() == 2) {
				if (Response == RESP_1)
					dc.SetTextForeground(*wxBLUE);
				else
					dc.SetTextForeground(*wxBLACK);
				dc.DrawText(P_TouchLabels[0],
					wxPoint(WindowSize.x / 4 - (dc.GetTextExtent(P_TouchLabels[0]).GetWidth() / 2), (90 * WindowSize.y) / 100));
				if (Response == RESP_2)
					dc.SetTextForeground(*wxBLUE);
				else
					dc.SetTextForeground(*wxBLACK);
				dc.DrawText(P_TouchLabels[1],
					wxPoint(3 * WindowSize.x / 4 - (dc.GetTextExtent(P_TouchLabels[1]).GetWidth() / 2), (90 * WindowSize.y) / 100));
			}
        }
        else if (P_NPossibleResponses == 3) {
            dc.DrawLine(2*WindowSize.x / 3,WindowSize.y,2*WindowSize.x / 3,(90 * WindowSize.y) / 100);
            dc.DrawLine(WindowSize.x / 3,WindowSize.y,WindowSize.x / 3,(90 * WindowSize.y) / 100);
			if (P_TouchLabels.Count() == 3) {
				if (Response == RESP_1)
					dc.SetTextForeground(*wxBLUE);
				else
					dc.SetTextForeground(*wxBLACK);
				dc.DrawText(P_TouchLabels[0],
					wxPoint(WindowSize.x / 6 - (dc.GetTextExtent(P_TouchLabels[0]).GetWidth() / 2), (90 * WindowSize.y) / 100));
				if (Response == RESP_2)
					dc.SetTextForeground(*wxBLUE);
				else
					dc.SetTextForeground(*wxBLACK);
				dc.DrawText(P_TouchLabels[1],
					wxPoint(WindowSize.x / 2 - (dc.GetTextExtent(P_TouchLabels[1]).GetWidth() / 2), (90 * WindowSize.y) / 100));
				if (Response == RESP_3)
					dc.SetTextForeground(*wxBLUE);
				else
					dc.SetTextForeground(*wxBLACK);
				dc.DrawText(P_TouchLabels[2],
					wxPoint(5 * WindowSize.x / 6 - (dc.GetTextExtent(P_TouchLabels[2]).GetWidth() / 2), (90 * WindowSize.y) / 100));
			}
        }
    }
    memDC.SelectObject(wxNullBitmap);
    
}

void c_DisplayCanvas::OnKey(wxKeyEvent &evt) {
    wxUniChar r=evt.GetUnicodeKey();
    Response = 0;
    //   wxMessageBox(wxString::Format("%c %u",(char) r, (unsigned int) r));
    if (r) { // standard key
        if (P_Resp1Keys.Find(r) != wxNOT_FOUND)
            Response = RESP_1;
        else if (P_Resp2Keys.Find(r) != wxNOT_FOUND)
            Response = RESP_2;
        else if (P_Resp3Keys.Find(r) != wxNOT_FOUND)
            Response = RESP_3;
        else if (r == WXK_SPACE) // Don't think these versions are used
            Response = RESP_Start;
        else if (r == WXK_ESCAPE)
            Response = RESP_Break;
/*        else if ((DisplayState == DISP_Idle) && (r==WXK_F10)) {
            if (P_CustomMode)
                P_CustomMode = 0;
            else
                P_CustomMode = 1;
            wxMessageBox(wxString::Format("JS mode set to %d",P_CustomMode));
        }*/
    }
    
    else {
        switch (evt.GetKeyCode()) {
            case WXK_SPACE:
                Response = RESP_Start;
                break;
            case WXK_ESCAPE:
                Response = RESP_Break;
                break;
            case WXK_F10:
                if (DisplayState == DISP_Idle) {
                    if (P_CustomMode)
                        P_CustomMode = 0;
                    else
                        P_CustomMode = 1;
                    wxMessageBox(wxString::Format("JS Mode set to %d - restart to have effect",P_CustomMode));
                }
                break;
        }
    }
    
    if ((DisplayState == DISP_Blank) || (DisplayState == DISP_Stim)) {
        if (Response == RESP_Start) {
            Response = 0;
        }
    }
    if (Response) {
        RT = swatch.Time();
//        MainFrame->SetStatusText(wxString::Format("%d %ld",Response,RT));
    }
    if ( (DisplayState == DISP_Idle) && ( (Response==RESP_1) || (Response==RESP_2) || (Response==RESP_3)) ) {
        MainFrame->SetStatusText(wxString::Format("Resp %d",Response));
        wxTheApp->Yield(true);
        wxMilliSleep(200);
        MainFrame->SetStatusText("");
        Response = RESP_None;
        
    }
}

void c_DisplayCanvas::OnLMouseClick(wxMouseEvent &evt) {
    wxPoint click_location;
    click_location = evt.GetPosition();
    wxSize WindowSize = GetSize();
    Response = 0;
    
	if (click_location.y >= (90 * WindowSize.y / 100)) {
		if (P_NPossibleResponses == 2) {
			if (click_location.x < WindowSize.x / 2)
				Response = RESP_1;
			else
				Response = RESP_2;
		}
		else if (P_NPossibleResponses == 3) {
			if (click_location.x < WindowSize.x / 3)
				Response = RESP_1;
			else if (click_location.x < (2 * WindowSize.x / 3))
				Response = RESP_2;
			else
				Response = RESP_3;
		}
	}
	else if ((DisplayState == DISP_StudyInstructions) || (DisplayState == DISP_TestInstructions))
		Response = RESP_Start;

    if (Response) {
        RT = swatch.Time();
//        MainFrame->SetStatusText(wxString::Format("%d %ld",Response,RT));
    }

    if ( (DisplayState == DISP_Idle) && ( (Response==RESP_1) || (Response==RESP_2) || (Response==RESP_3)) ) {
        MainFrame->SetStatusText(wxString::Format("Resp %d",Response));
        wxTheApp->Yield(true);
        wxMilliSleep(200);
        MainFrame->SetStatusText("");
        Response = RESP_None;
        
    }
    this->Refresh();
    evt.Skip();
    
}


c_DisplayCanvas::~c_DisplayCanvas() {
	if (DisplayedImage) delete DisplayedImage;
}

