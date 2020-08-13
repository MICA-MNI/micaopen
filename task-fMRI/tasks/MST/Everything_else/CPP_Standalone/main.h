//
//  main.h
//  BPSO
//
//  Created by Craig Stark on 11/11/11.
//  Copyright 2011 Craig Stark. All rights reserved.
//

#include <wx/filename.h>
#include <wx/textfile.h>
#include <wx/stopwatch.h>

#define N_STIM_PER_LIST 192
#define N_STIM_PER_SET 64
#define VERSION 0.96

extern int SetBins[11][N_STIM_PER_LIST];
//extern int SetDBins[N_STIM_PER_LIST];

extern wxFileName Resource_path;
//extern wxString P_OutputDir;
extern float P_Dur;
extern float P_ISI;
extern int P_Phase;
extern int P_SetIndex;
extern bool P_FullScreen;
extern bool P_SelfPaced;
extern bool P_AllowTouch;
extern bool P_2ChoiceTest;
extern int P_NStimPerSet;
extern int P_NPossibleResponses;
extern int P_SubList;
extern int P_Randomization;
extern int P_ScreenDPI;
extern int P_CustomMode;
extern float P_ScreenScalingFactor;
extern wxString P_Set;
extern wxString P_SubjID;
extern wxString P_Resp1Keys;
extern wxString P_Resp2Keys;
extern wxString P_Resp3Keys;
extern wxArrayString P_StudyStim;
extern wxArrayString P_RepeatStim;
extern wxArrayString P_LureStim;
extern wxArrayString P_FoilStim;
extern wxArrayString P_TouchLabels;
extern wxTextFile *LogFile;
extern wxImage *Logo;
extern wxLanguage P_Language;

#ifndef MnemonicSimilarity_main_h
#define MnemonicSimilarity_main_h

double phi(double x);
double NormalCDFInverse(double p);
double RationalApproximation(double t);

class ParamDialog;

// Define a new application type, each program should derive a class from wxApp
class MyApp : public wxApp {
public:
    virtual bool OnInit();
};

class c_DisplayCanvas: public wxWindow {
public:
    c_DisplayCanvas(wxWindow *parent, int xsize, int ysize);
    ~c_DisplayCanvas(void);
    wxImage *DisplayedImage;
    int DisplayState; //0=blank, 1=image, 2=Study instructs
    int Response;
    long RT;
    wxStopWatch swatch;

private:
    void OnPaint(wxPaintEvent &evt);
    void OnKey(wxKeyEvent &evt);
    void OnLMouseClick(wxMouseEvent &evt);
    DECLARE_EVENT_TABLE()
        
};

class c_HelpWindow : public wxFrame {
public:
    // ctor(s)
    c_HelpWindow(wxWindow *parent);
    wxTextCtrl *maintext;
};

// Define a new frame type: this is going to be our main frame
class c_DisplayFrame : public wxFrame {
public:
    // ctor(s)
    c_DisplayFrame(const wxString& title);
    
    // event handlers (these functions should _not_ be virtual)
    void OnQuit(wxCommandEvent& event);
    void OnAbout(wxCommandEvent& event);
//    bool GetParameters();
    void OnRun(wxCommandEvent& evt);
    void OnHelp(wxCommandEvent& evt);
    void OnParameters(wxCommandEvent& evt);
    void OnLocale(wxCommandEvent& evt);
    void OnChangeKeys(wxCommandEvent& evt);

    c_DisplayCanvas *Canvas;
    c_HelpWindow *HelpWindow;
    ParamDialog *PDialog;
    
private:
    bool CheckFiles(wxString SetName);
//    bool SetupLists();
    bool SetupListsPermuted();
    bool ShowStudyPhase();
    bool ShowTestPhase();
    bool SavePrefs();
    bool LoadPrefs();
    wxSize WindowSize;
    wxLocale UserLocale;
    
    // any class wishing to process wxWidgets events must use this macro
    DECLARE_EVENT_TABLE()
};




// IDs for the controls and the menu commands
enum
{
    // menu items
    MENU_Quit = wxID_EXIT,
    MENU_About = wxID_ABOUT,
    MENU_Help = wxID_HELP,
    MENU_RunFull = wxID_HIGHEST+1,
    MENU_RunWindow,
    MENU_Locale,
    MENU_ChangeKeys
    
};

enum {
    RESP_None = 0,
    RESP_1 = 1,
    RESP_2,
    RESP_3,
    RESP_Break=10,
    RESP_Start
};

enum {
    DISP_Idle = 0,
    DISP_Blank,
    DISP_Stim,
    DISP_StudyInstructions,
    DISP_TestInstructions
};

enum {
    CUSTOM_NONE =0,
    CUSTOM_JS
};
#endif
