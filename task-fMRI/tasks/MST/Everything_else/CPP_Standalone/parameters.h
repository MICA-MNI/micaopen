//
//  parameters.h
//  BPSO
//
//  Created by Craig Stark on 10/30/11.
//  Copyright 2011 Craig Stark. All rights reserved.
//

#ifndef MnemonicSimilarity_parameters_h
#define MnemonicSimilarity_parameters_h

//#include "wx/wx.h"
#include "wx/spinctrl.h"
#include "wx/choice.h"

enum {
    PARAM_DSPIN = wxID_HIGHEST+100,
    PARAM_CHOICE,
    PARAM_TEXT,
    PARAM_SET,
    PARAM_PHASE,
    PARAM_FULLSCREEN,
    PARAM_SELFPACE,
	PARAM_2CHOICETEST,
    PARAM_DIR,
    PARAM_TOUCH,
    BUTTON_GO

};


class ParamDialog : public wxDialog {
public:
	ParamDialog(wxWindow* parent);
	
/*	wxString subj_id;
	float dur, isi;
	int phase;
	int set;
	bool fullscreen;*/
    wxSpinCtrlDouble *ctl_dur;
    wxSpinCtrlDouble *ctl_isi;
    wxChoice *ctl_nstimper;
    wxChoice *ctl_randomization;
    wxTextCtrl *ctl_subjid;
    wxButton *ctl_dir;
    wxChoice *ctl_set;
    wxRadioBox *ctl_phase;
    wxCheckBox *ctl_fullscreen;
    wxCheckBox *ctl_selfpace;
    wxCheckBox *ctl_touch;
	wxCheckBox *ctl_2choicetest;
    
    void UpdateDSpinParams(wxSpinDoubleEvent& evt);
    void UpdateChoiceParams(wxCommandEvent& evt);
    void UpdateTextParams(wxCommandEvent &evt);
    void ChangeDir(wxCommandEvent &evt);
    void UpdateCheckParams(wxCommandEvent &evt);
    void UpdateRadioParams(wxCommandEvent &evt);
   // void OnRun(wxCommandEvent &evt);
    wxDECLARE_EVENT_TABLE();
};




#endif
