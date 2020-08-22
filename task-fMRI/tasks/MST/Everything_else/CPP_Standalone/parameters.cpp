//
//  parameters.cpp
//  BPSO
//
//  Created by Craig Stark on 10/30/11.
//  Copyright 2011 Craig Stark. All rights reserved.
//
#include <wx/wx.h>
#include <wx/filefn.h>
#include <wx/dirdlg.h>
#include <wx/radiobox.h>
#include "main.h"
#include "parameters.h"

extern c_DisplayFrame *MainFrame;

wxBEGIN_EVENT_TABLE(ParamDialog, wxDialog)
EVT_SPINCTRLDOUBLE(PARAM_DSPIN, ParamDialog::UpdateDSpinParams)
EVT_CHOICE(PARAM_CHOICE, ParamDialog::UpdateChoiceParams)
EVT_TEXT(PARAM_TEXT,ParamDialog::UpdateTextParams)
EVT_BUTTON(PARAM_DIR,ParamDialog::ChangeDir)
EVT_CHECKBOX(PARAM_FULLSCREEN,ParamDialog::UpdateCheckParams)
EVT_CHECKBOX(PARAM_SELFPACE,ParamDialog::UpdateCheckParams)
EVT_CHECKBOX(PARAM_TOUCH,ParamDialog::UpdateCheckParams)
EVT_CHECKBOX(PARAM_2CHOICETEST,ParamDialog::UpdateCheckParams)
//EVT_RADIOBOX(PARAM_SET, ParamDialog::UpdateRadioParams)
EVT_CHOICE(PARAM_SET, ParamDialog::UpdateChoiceParams)
EVT_RADIOBOX(PARAM_PHASE, ParamDialog::UpdateRadioParams)
//EVT_BUTTON(BUTTON_GO,ParamDialog::OnRun)
//EVT_BUTTON(BUTTON_GO,ParamDialog::OnRun)
wxEND_EVENT_TABLE()

ParamDialog::ParamDialog(wxWindow* parent) : wxDialog(parent, wxID_ANY, "MST Parameters") {
/*	dur = P_Dur;
	isi = P_ISI;
	fullscreen = P_FullScreen;
	subj_id= P_SubjID;
	phase = P_Phase;  // Study
	if (P_Set == "Set D") set = 1;
    else set = 0;  // Set C
  */  
    int i;
    
    //    float m_value;
    // 	wxFloatingPointValidator<float> f_val(2, &m_value, wxNUM_VAL_NO_TRAILING_ZEROES);
	wxBoxSizer *topsizer = new wxBoxSizer(wxVERTICAL);
	wxFlexGridSizer *paramsizer = new wxFlexGridSizer(2);
	
	paramsizer->Add(new wxStaticText(this,wxID_ANY,"ID"),1,wxALL,5);
	paramsizer->Add(ctl_subjid = new wxTextCtrl(this,PARAM_TEXT,P_SubjID),1,wxALL,5);
    
    ctl_dur = new wxSpinCtrlDouble(this,PARAM_DSPIN,wxString::Format("%.3f",P_Dur),
                                   wxDefaultPosition, wxDefaultSize,
                                   wxSP_ARROW_KEYS,0.0, 10.0, P_Dur,0.5);   
	paramsizer->Add(new wxStaticText(this,wxID_ANY,"Dur"),1,wxALL,5);
    paramsizer->Add(ctl_dur,1,wxALL,5);
    
    ctl_isi = new wxSpinCtrlDouble(this,PARAM_DSPIN,wxString::Format("%.3f",P_ISI),
                                   wxDefaultPosition, wxDefaultSize,
                                   wxSP_ARROW_KEYS,0.0, 10.0, P_ISI,0.1);   
	paramsizer->Add(new wxStaticText(this,wxID_ANY,"ISI"),1,wxALL,5);
    paramsizer->Add(ctl_isi,1,wxALL,5);
    wxArrayString nstimchoices;
//    nstimchoices.Add("8"); nstimchoices.Add("10"); nstimchoices.Add("16");
//    nstimchoices.Add("20"); nstimchoices.Add("32"); nstimchoices.Add("40");
    nstimchoices.Add("20 - 1"); nstimchoices.Add("20 - 2"); nstimchoices.Add("20 - 3");
    nstimchoices.Add("32 - 1"); nstimchoices.Add("32 - 2");
    nstimchoices.Add("40");
    nstimchoices.Add("64");
    ctl_nstimper = new wxChoice(this,PARAM_CHOICE,
                                   wxDefaultPosition, wxDefaultSize,
                                   nstimchoices);
    ctl_nstimper->SetSelection(nstimchoices.GetCount()-1);
	paramsizer->Add(new wxStaticText(this,wxID_ANY,"# Per cond"),1,wxALL,5);
    paramsizer->Add(ctl_nstimper,1,wxALL,5);
    
    wxArrayString rndchoices;
    rndchoices.Add("ID #");
    for (i=1; i<=10; i++)
        rndchoices.Add(wxString::Format("%d",i));
    ctl_randomization = new wxChoice(this,PARAM_CHOICE,
                                wxDefaultPosition, wxDefaultSize,
                                rndchoices);
    ctl_randomization->SetSelection(0);
	paramsizer->Add(new wxStaticText(this,wxID_ANY,"Randomization"),1,wxALL,5);
    paramsizer->Add(ctl_randomization,1,wxALL,5);
    
    
    wxArrayString sets;
    sets.Add("Set C    ");
    sets.Add("Set D");
    sets.Add("Set E");
    sets.Add("Set F");
    sets.Add("Set 1");
    sets.Add("Set 2");
    sets.Add("Set 3");
    sets.Add("Set 4");
    sets.Add("Set 5");
    sets.Add("Set 6");
    sets.Add("Set ScC");
//    paramsizer->Add(ctl_set = new wxRadioBox(this,PARAM_SET,"Set",wxDefaultPosition,wxDefaultSize,sets,1),1,wxALL,5);
    paramsizer->Add(ctl_set = new wxChoice(this,PARAM_SET,
                           wxDefaultPosition, wxDefaultSize,
                           sets),1,wxALL,5);
	ctl_set->SetSelection(0);

    paramsizer->Add(ctl_dir = new wxButton(this,PARAM_DIR,_T("Output dir")),
                    1,wxALL,5);

    wxArrayString phases;
    phases.Add("Phase 1    ");
    phases.Add("Phase 2");
    if (P_CustomMode == CUSTOM_JS) {
        phases.Add(" Phase 2A");
        phases.Add(" Phase 2B");
    }
    paramsizer->Add(ctl_phase = new wxRadioBox(this,PARAM_PHASE,"Phase",wxDefaultPosition,wxDefaultSize,phases,1),
                    1,wxALL,5);
    
    
//    paramsizer->Add(ctl_dir = new wxButton(this,PARAM_DIR,_T("Output dir")),
//                    1,wxALL,5);

    //   paramsizer->Add(ctl_fullscreen = new wxCheckBox(this,PARAM_FULLSCREEN,"Fullscreen"),1,wxALL,5);
 //   if (P_FullScreen)
 //       ctl_fullscreen->SetValue(true);
	wxBoxSizer *checksizer = new wxBoxSizer(wxVERTICAL);
    checksizer->Add(ctl_selfpace = new wxCheckBox(this,PARAM_SELFPACE,"Self-paced"),1,wxTOP,10);
    ctl_selfpace->SetValue(P_SelfPaced);

   // paramsizer->AddStretchSpacer();
    checksizer->Add(ctl_touch = new wxCheckBox(this,PARAM_TOUCH,"Enable touch"),1);
    ctl_touch->SetValue(P_AllowTouch);

	checksizer->Add(ctl_2choicetest = new wxCheckBox(this, PARAM_2CHOICETEST, "O/N only"), 1);
	ctl_2choicetest->SetValue(P_2ChoiceTest);
    
    paramsizer->Add(checksizer,1,wxALL,5);

    topsizer->Add(paramsizer);
	SetSizerAndFit(topsizer);
    
}

void ParamDialog::ChangeDir(wxCommandEvent& WXUNUSED(evt)) {
    wxDirDialog dd(this, _("Choose output directory"), "",
                      wxDD_DEFAULT_STYLE | wxDD_DIR_MUST_EXIST);
    dd.ShowModal();
    wxSetWorkingDirectory(dd.GetPath());
    
}
void ParamDialog::UpdateDSpinParams(wxSpinDoubleEvent& WXUNUSED(evt)) {
    P_Dur = ctl_dur->GetValue();
    P_ISI = ctl_isi->GetValue();
}

void ParamDialog::UpdateChoiceParams(wxCommandEvent& WXUNUSED(evt)) {
    wxString tmpstr1 = ctl_nstimper->GetStringSelection().BeforeFirst(' ');
    wxString tmpstr2 = ctl_nstimper->GetStringSelection().AfterLast(' ');
    long lval;
    tmpstr1.ToLong(&lval);
    P_NStimPerSet = (int) lval;
    if (tmpstr2.IsEmpty() || (tmpstr1 == tmpstr2)) P_SubList = 0;
    else {
        tmpstr2.ToLong(&lval);
        P_SubList = (int) lval;
    }
    
    P_Randomization = ctl_randomization->GetSelection();
    
    P_Set = ctl_set->GetStringSelection().Trim();
    P_SetIndex = ctl_set->GetSelection();
    
}

void ParamDialog::UpdateTextParams(wxCommandEvent& WXUNUSED(evt)) {
    //wxMessageBox(_T("text") + wxGetCwd());
    P_SubjID = ctl_subjid->GetValue();
}
                                   
void ParamDialog::UpdateCheckParams(wxCommandEvent& WXUNUSED(evt)) {
    //wxMessageBox(_T("text") + wxGetCwd());
    //P_FullScreen = ctl_fullscreen->GetValue();
    P_SelfPaced = ctl_selfpace->GetValue();
    P_AllowTouch = ctl_touch->GetValue();
    P_2ChoiceTest = ctl_2choicetest->GetValue();
}

void ParamDialog::UpdateRadioParams(wxCommandEvent& WXUNUSED(evt)) {
/*    switch (ctl_set->GetSelection()) {
        case 0:
            P_Set = "Set C";
            P_SetIndex = 0;
            break;
        case 1:
            P_Set = "Set D";
            P_SetIndex = 1;
            break;
        case 2:
            P_Set = "Set E";
            P_SetIndex = 2;
            break;
        case 3:
            P_Set = "Set F";
            P_SetIndex = 3;
            break;
        default:
            wxMessageBox("Error - unknown set choice");
            break;
    }*/
    P_Phase=ctl_phase->GetSelection();
}

/*void ParamDialog::OnRun(wxCommandEvent &evt) {
    //evt.Skip();
    
    wxCommandEvent* tmp_evt;
    if (P_FullScreen) tmp_evt= new wxCommandEvent(0,MENU_RunFull);
    else tmp_evt= new wxCommandEvent(0,MENU_RunWindow);
    MainFrame->OnRun(*tmp_evt);
    delete tmp_evt;

}*/

/*bool c_DisplayFrame::GetParameters() {
    PDialog->Show(true);
    PDialog->Raise();
    PDialog->SetPosition(wxPoint(50,50));
    return false;
    
}*/
