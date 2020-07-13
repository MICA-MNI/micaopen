//
//  main.cpp
//  MST
//
//  Created by Craig Stark on 11/11/11.
//  Copyright 2011 Craig Stark. All rights reserved.
//

/* Version history
//
0.1 (11/17/11): - Initial beta
0.2 (11/23/11): - Fixed bug causing stim lists to continually grow with use (leading to
                     multiple presentations)
                - Added summary output for lure bins
0.3 (3/8/12):   - A "self-paced" option is now available.  The ISI will be at least what is
                     specified but will extend forever when this is selected.  So, it's not on the
                     screen any longer, but we can give extra time for people to respond.
                - Response options extended to allow for larger hands.  Now V,C,1=1  B,2=2  N,M,3=3
0.4 (8/6/12):   - Renamed to MST (from MenmonicSim)
                - Summary at the end will correct for no-responses (as well as show rates raw)
0.5 (9/6/12):   - Fixed major bug: The lure bins were not being properly read and applied.
                    Set D's lure bins were being read improperly (Set C's were read in place of
                    Set D) and in both the matching of item to lure bin was off by 1 in the list
                    (0-indexed vs. 1-indexed).  Calculation of the BPS-O metric is unaffected
                    by this bug but any existing data in which the lure bin info is needed (e.g., tracing
                    out a tuning curve for a subject) will need to be recalculated manually as the summary
                    table at the end by lure bin will be incorrect.  The Matlab code is not affected here
                    - only this beta-level stand-alone code has this bug.
0.6 (9/11/12):  - Replaced the SetC bins.txt and SetD bins.txt files with the final (Nov 2009) ones.
                - Reworked the way stimuli were assigned to target, repeat, and lure conditions. Random
                    assignment based on subject ID ensuring that there is an even distribution across 
                    lure bins. (Gone is the multiple-of-6 blocking using 1-64, 65-128, and 129-192 as
                    blocks of stimuli assigned to these conditions).
                - Now able to be run in shorter versions. The default is still 64 stimuli per condition 
                    but as few as 8 are now possible. This is for testing purposes to determine how short
                    the task can go. Eventually, if shorter versions are used so that many runs can be
                    done in an individual, we'll need to ensure that the stimuli don't repeat. This isn't
                    in place yet.
0.62 (10/8/12): - Esc key closes the parameter window.  Can't seem to override this so added a "Show 
                    parameters" entry to the File menu to put it back
                - Mac build set to compile for 32-bit, 10.5 compatible
                - Fixed "Old" | Target count in log file
                - Added # of Lure-NoResp by LureBin output to log file
0.63 (10/9/12): - Disables menu during presentation so can't "start it twice"
                - Fixed SetD/190b.jpg -- was actually a PNG file and caused an odd error about "Unable to
                    set cHRM..."
0.7 (8/22/13):  - Randomization parameter added to dialog to let you control how the randomization of
                    stimuli to Targ/Lure/Foil lists happens.  Old behavior (based on ID) and several fixed
                    "seeds" as options.
                - Internationalization code in place.  Currently, Chinese and Swedish options available.
                    Others just need someone to help translate a few phrases.
                - Can now use subets of shorter lists.  So, if you use 20 items, you have 3 sublist
                    choices and if you use 32 items you have 2 sublist choices. This lets you get more
                    independent runs per participant, so long as you're using a shorter version.
                - On main logo screen you can now test the response buttons by showing you "Resp #" in
                    the status bar briefly after a button is pressed.
0.8  (7/21/14): - Renamed as MST (Mnemonic Similarity Task)
                - Add 40-item version back in per request
                - Added Sets E and F
0.81 (9/18/15): - Added touch-screen response button options
0.82 (3/10/16): - Added French, German, and Spanish translations from Christine Bastin
                - Able to deal with high-DPI monitors better (scaling images on the fly)
0.9 (4/1/16):   - Added Sets 1-6 which are reshuffles of Sets C-H to make 6 matched sets.
                - Reworked the parameter display window in the process.
                - Added Old/New variant for test which computes da for the Target:Foil, Target:Lure, 
                    and Lure:Foil
0.91 (5/24/16): - Custom "JS" mode added (F10 and restart to toggle).  Allows for testing half the
                   items in one session and the other half later
                - Fixed bug where Set C was not available.
                - Fixed bug with 40 item version
0.92 (6/27/16): - Fixed bug in saving / loading custom keys
0.93 (10/6/16): - Added Italian translation from Nicola Cellini
0.94 (3/24/17): - Slight reworking of stimuli in Sets 1-6 to keep within-set overlap low
0.95 (4/3/17):  - Fixed issue whereby the space bar would lead to responses of 11
     (8/9/17):  - Fixed permissions issue in build on Mac
                - Fixed da computations in two-choice version

0.96 (1/11/18): - Ditched the bogus da computation and shifted to accurate d' calculation in two-choice
                - Added 'Scenes C' -- Note the lure bins here are entirely bogus and this is not really for general consumption
 
*/
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
#include <wx/textctrl.h>
#include <wx/config.h>
#include <wx/xlocale.h>
#include <wx/intl.h>
#include "main.h"
#include "parameters.h"

#include <cmath>

extern void PermuteArrayString(wxArrayString &arry);

/*
- X isn't closing things - only File, exit
*/
// Setup some globals
int SetBins[11][N_STIM_PER_LIST];
//int SetDBins[N_STIM_PER_LIST];
wxFileName Resource_path;
//wxString P_OutputDir;
float P_Dur = 2.0;
float P_ISI = 0.5;
int P_Phase = 0; // Study = 0, Test = 1;
int      P_SetIndex = 0; // 0=C, 1=D, 2=E, 3=F, 4=1, 5=2, ...
wxString P_Set = "Set C";
wxString P_SubjID = "999";
wxString P_Resp1Keys = "1VC";
wxString P_Resp2Keys = "2B";
wxString P_Resp3Keys = "3NM";
bool P_FullScreen = false;
bool P_SelfPaced = false;
bool P_AllowTouch = false;
bool P_2ChoiceTest = false;
int P_NStimPerSet = 64;
int P_SubList = 0;
int P_Randomization = 0;
int P_NPossibleResponses = 3;
int P_ScreenDPI = 120;
int P_CustomMode = 0;
float P_ScreenScalingFactor = 1.0;

wxArrayString	P_TouchLabels;


wxLanguage		P_Language = wxLANGUAGE_ENGLISH_US; // Initially, it's assumed
wxArrayString P_StudyStim;
wxArrayString P_RepeatStim;
wxArrayString P_LureStim;
wxArrayString P_FoilStim;
wxTextFile *LogFile;
wxImage *Logo = NULL;
c_DisplayFrame *MainFrame;



BEGIN_EVENT_TABLE(c_DisplayFrame, wxWindow)
EVT_MENU(MENU_Quit,  c_DisplayFrame::OnQuit)
EVT_MENU(MENU_About, c_DisplayFrame::OnAbout)
EVT_MENU(MENU_RunFull, c_DisplayFrame::OnRun)
EVT_MENU(MENU_RunWindow, c_DisplayFrame::OnRun)
EVT_MENU(MENU_Help,c_DisplayFrame::OnHelp)
EVT_MENU(BUTTON_GO,c_DisplayFrame::OnRun)
EVT_MENU(MENU_Locale, c_DisplayFrame::OnLocale)
EVT_MENU(MENU_ChangeKeys, c_DisplayFrame::OnChangeKeys)
EVT_MENU(wxID_PROPERTIES, c_DisplayFrame::OnParameters)
//EVT_PAINT(c_DisplayFrame::OnPaint)
//EVT_ERASE_BACKGROUND(c_DisplayFrame::OnErase)

END_EVENT_TABLE()

IMPLEMENT_APP(MyApp)



// 'Main program' equivalent: the program execution "starts" here
bool MyApp::OnInit() {
    if ( !wxApp::OnInit() )
        return false;

    wxImage::AddHandler( new wxJPEGHandler );
    wxImage::AddHandler(new wxPNGHandler);
    
    
    // create the main application window
    MainFrame = new c_DisplayFrame("MST");
    
    MainFrame->Show(true);

    
    MainFrame->PDialog->Show(true);
    MainFrame->PDialog->Raise();
    MainFrame->PDialog->SetPosition(wxPoint(50,50));

    // success: wxApp::OnRun() will be called which will enter the main message
    // loop and the application will run. If we returned false here, the
    // application would exit immediately.
    return true;
}


// frame constructor
c_DisplayFrame::c_DisplayFrame(const wxString& title)
       : wxFrame(NULL, wxID_ANY, title, wxDefaultPosition, wxSize(-1,-1),wxSYSTEM_MENU|wxCAPTION)
{
 
    
    // Load up the prefs
    LoadPrefs();
    
    // Take care of language
    bool res=UserLocale.Init(P_Language);
     // Will need to figure out where this should really be
    wxLocale::AddCatalogLookupPathPrefix(wxStandardPaths::Get().GetResourcesDir());
    res = UserLocale.AddCatalog("MST");   // add my language catalog
    if (!res) wxMessageBox("Problem initializing language files\n"+wxStandardPaths::Get().GetResourcesDir());
     
    if (P_CustomMode == CUSTOM_JS)
        SetTitle("MST-JS");
    
    
 //   DisplayState = 0;
    WindowSize=this->GetSize();
 //   DisplayedImage = new wxImage(WindowSize);

	wxScreenDC sdc;
	P_ScreenDPI = sdc.GetPPI().x;
	if (P_ScreenDPI > 120) {
		P_ScreenScalingFactor = (float) P_ScreenDPI / 120.0;
	}

    HelpWindow = new c_HelpWindow(this);

    // create a menu bar
    wxMenu *fileMenu = new wxMenu;

    // the "About" item should be in the help menu
    wxMenu *helpMenu = new wxMenu;
    helpMenu->Append(MENU_About, _("&About...\tF1"), _("Show about dialog"));
    helpMenu->Append(MENU_Help, _("Help"), _("Show experimenter instructions"));

    fileMenu->Append(wxID_PROPERTIES,_("Show Parameters"));
    fileMenu->Append(MENU_ChangeKeys, _("Change keys"), _("Change response keys"));
    fileMenu->Append(MENU_Locale, _("Change language"), _("Change language"));
    fileMenu->Append(MENU_Quit, _("E&xit\tAlt-X"), _("Quit this program"));
    //fileMenu->AppendCheckItem(wxID_PROPERTIES,"Show Parameters");
    //fileMenu->Check(wxID_PROPERTIES,true);
    
    wxMenu *RunMenu = new wxMenu;
    RunMenu->Append(MENU_RunFull,_("&Run full screen\tAlt-R"), _("Run in full screen mode"));
    RunMenu->Append(MENU_RunWindow,_("Run &windowed\tAlt-W"), _("Run in a window"));
    

    // now append the freshly created menu to the menu bar...
    wxMenuBar *menuBar = new wxMenuBar();
    menuBar->Append(fileMenu, _("&File"));
    menuBar->Append(RunMenu,_("Run"));
    menuBar->Append(helpMenu, _("&Help"));

    // ... and attach this menu bar to the frame
    SetMenuBar(menuBar);

    Canvas = new c_DisplayCanvas(this,(int) (600.0 * P_ScreenScalingFactor),(int) (600.0 * P_ScreenScalingFactor));
    Canvas->SetMinSize(wxSize(500,500));
    Fit();

    // create a status bar just for fun (by default with 1 pane only)
    CreateStatusBar(2);
    SetStatusText(_("Welcome to the MST") + wxString::Format(" %.2f!",VERSION));

    
    Fit();
//    SetBackgroundStyle(wxBG_STYLE_CUSTOM);
    
    // Check all files are OK
    CheckFiles(wxString("C"));
    CheckFiles(wxString("D"));
    CheckFiles(wxString("E"));
    CheckFiles(wxString("F"));
    int i;
    for (i=1; i<=6; i++)
        CheckFiles(wxString::Format("%d",i));
    CheckFiles(wxString("ScC"));
    
    wxStandardPathsBase& StdPaths = wxStandardPaths::Get(); 
    wxSetWorkingDirectory(StdPaths.GetDocumentsDir()); // Set the doc dir to be the default
 
    LogFile = NULL;
    
    PDialog = new ParamDialog(this);
 
}


// event handlers


void c_DisplayFrame::OnParameters(wxCommandEvent &evt) {
    //MainFrame->PDialog->Show(evt.IsChecked());
    MainFrame->PDialog->Show(true);
}

void c_DisplayFrame::OnQuit(wxCommandEvent& WXUNUSED(event)) {
    if (Canvas->DisplayState != DISP_Idle)  // something is active - don't allow
        return;
    
    SavePrefs();
    
    delete PDialog;
    delete Canvas;

    Destroy();
}

void c_DisplayFrame::OnAbout(wxCommandEvent& WXUNUSED(event))
{
    wxMessageBox(wxString::Format
                 (
                    "Welcome to MST version %.2f!\n"
                    "\n"
                    "Copyright 2011-2016 Craig Stark\n"
                    "running under %s with %s.\n"
					"Screen: %d DPI (%.2f)",
                    VERSION,
                    wxGetOsDescription(), wxVERSION_STRING,
					P_ScreenDPI,P_ScreenScalingFactor
                 ),
                 "MST",
                 wxOK | wxICON_INFORMATION,
                 this);
}

void c_DisplayFrame::OnLocale(wxCommandEvent& WXUNUSED(event)) {
    const wxString LangNames[] = {
        "English",
        "Chinese",
        "French",
        "German",
        "Italian",
        "Spanish",
        "Swedish"
    };
    
    int LangIDs[] = {
        wxLANGUAGE_ENGLISH_US,
        wxLANGUAGE_CHINESE,
        wxLANGUAGE_FRENCH,
        wxLANGUAGE_GERMAN,
        wxLANGUAGE_ITALIAN,
        wxLANGUAGE_SPANISH,
        wxLANGUAGE_SWEDISH,
    };
    
    int choice = wxGetSingleChoiceIndex(_("Please choose a language.  If you are changing\nto a different language, you will need to\nrestart"), _("Language"),
										WXSIZEOF(LangNames),LangNames,
										this,-1,-1,true,150,400);
	if (choice == -1) return;
	
	P_Language = (wxLanguage) LangIDs[choice];
    wxMessageBox("Restart the program to make your change");
    
}

void c_DisplayFrame::OnChangeKeys(wxCommandEvent& WXUNUSED(event)) {
    wxString tmpstr;
    tmpstr = wxGetTextFromUser("Enter all keys that can be used for Resp 1 (Old) - e.g., '1XV'","Response 1 options",P_Resp1Keys);
    if (!tmpstr.IsEmpty()) P_Resp1Keys = tmpstr;
    tmpstr = wxGetTextFromUser("Enter all keys that can be used for Resp 2 (Sim) - e.g., '2B'","Response 1 options",P_Resp2Keys);
    if (!tmpstr.IsEmpty()) P_Resp2Keys = tmpstr;
    tmpstr = wxGetTextFromUser("Enter all keys that can be used for Resp 3 (New) - e.g., '3NM'","Response 1 options",P_Resp3Keys);
    if (!tmpstr.IsEmpty()) P_Resp3Keys = tmpstr;
    P_Resp1Keys.MakeUpper();
    P_Resp2Keys.MakeUpper();
    P_Resp3Keys.MakeUpper();
    
}

void c_DisplayFrame::OnRun(wxCommandEvent &evt) {
    bool rval;
    if (evt.GetId() == MENU_RunWindow)
        P_FullScreen = false;
    else
        P_FullScreen = true;
    
    // Verify we're OK on set size.  
    if (P_NStimPerSet < 8) P_NStimPerSet = 8;
    else if (P_NStimPerSet > 64) P_NStimPerSet = 64;
    
    wxSize c_size = Canvas->GetSize(); // Save size
    wxSize f_size = this->GetSize();
    
    GetMenuBar()->Disable();
    Canvas->DisplayState=DISP_Blank; // As long as not "idle" can veto the quit
    if (P_FullScreen) {
        Canvas->SetSize(wxGetDisplaySize());
        GetStatusBar()->Hide();
        ShowFullScreen(P_FullScreen,wxFULLSCREEN_ALL);
    }
    // Setup the log file - should be in the current working dir which should be set in GetParameters();
    LogFile = new wxTextFile(wxString::Format("MSTlog_"+P_SubjID+".txt"));
    if (LogFile->Exists()) LogFile->Open();
    else LogFile->Create();
    LogFile->AddLine(wxString::Format("MST version %.2f",VERSION));
    LogFile->AddLine(wxNow());
    if (P_Phase) {
		if (P_CustomMode == CUSTOM_JS)
			LogFile->AddLine(wxString::Format("Test phase %d",P_Phase - 1));
		else
			LogFile->AddLine("Test phase");
	}
    else
        LogFile->AddLine("Study phase");
	
    LogFile->AddLine("ID: " + P_SubjID);
    LogFile->AddLine("Set: " + P_Set);
    LogFile->AddLine(wxString::Format("     internal index %d",P_SetIndex));
    if (P_Randomization)
        LogFile->AddLine(wxString::Format("Randomization based on seed %d",P_Randomization));
    else
        LogFile->AddLine("Randomization based on ID");
    LogFile->AddLine(wxString::Format("Dur: %.3f, ISI:%.3f, Self-paced:%d, Full-Screen:, nSet size: %d",P_Dur,P_ISI,(int) P_SelfPaced, (int) P_FullScreen, P_NStimPerSet));
    
    // Sets up lists of stimuli for study and test and randomly permutes them
    rval = SetupListsPermuted();

    if (!rval) {
        PDialog->Show(false);
        Canvas->Response = RESP_None;
        Canvas->SetFocus();
        if (P_Phase) 
            ShowTestPhase();
        else
            ShowStudyPhase();
        
		if ((P_CustomMode == CUSTOM_JS) && (P_Phase == 0)) { // auto-advance to Phase2A
			P_Phase = 2; // Phase 2A
			PDialog->ctl_phase->SetSelection(2);
			ShowTestPhase();
		}

        if (P_FullScreen) { // restore
            ShowFullScreen(false);
            Canvas->SetSize(c_size);
            this->SetSize(f_size);
            GetStatusBar()->Show(true);
        }
        
        PDialog->Show(true);
    }
    GetMenuBar()->Enable();
    LogFile->Write();
    LogFile->Close();
    delete LogFile;
    LogFile = NULL;
    
    Canvas->DisplayState = DISP_Idle;
    Canvas->Refresh();

//    wxMessageBox("foo");
}

bool c_DisplayFrame::ShowStudyPhase() {
    int trial;
    
    wxFileName tmp_fname(Resource_path);
    
    // Put up indoor / outdoor instructs and wait for OK to start
    P_NPossibleResponses = 2;
	P_TouchLabels.Clear();
	P_TouchLabels.Add(_("Indoor"));
	P_TouchLabels.Add(_("Outdoor"));

    Canvas->DisplayState = DISP_StudyInstructions;
    Canvas->Refresh();
    
    LogFile->AddLine("Study phase started at: " + wxNow());
    LogFile->AddLine("Trial\tResp\tRT\tImg");
    
    
    while (1) { // Loop waiting to start or to bail
        if (Canvas->Response == RESP_Break) {
//            Canvas->DisplayState = DISP_Blank;
//            Canvas->Refresh();
            return true;
        }
        else if (Canvas->Response == RESP_Start) {
            break;
        }
        wxMilliSleep(50);
        wxTheApp->Yield(true);
    }

    for (trial = 0; trial < (int) P_StudyStim.GetCount(); trial++) {
        if (Canvas->Response == RESP_Break)
            return true;
        tmp_fname.Assign(Resource_path);
        tmp_fname.AppendDir(P_Set);
        tmp_fname.SetFullName(P_StudyStim[trial]);

        Canvas->DisplayState=DISP_Stim;
        Canvas->DisplayedImage->LoadFile(tmp_fname.GetFullPath());
		if (P_ScreenScalingFactor > 1.0) {
			Canvas->DisplayedImage->Rescale((int) (P_ScreenScalingFactor * Canvas->DisplayedImage->GetWidth()), 
				(int) (P_ScreenScalingFactor * Canvas->DisplayedImage->GetHeight()));
		}
        Canvas->Response = RESP_None; Canvas->RT=0;
        Canvas->Refresh();
 //       Canvas->Update();
        Canvas->swatch.Start();
        //nloops = (int) (P_Dur * 100);
        while (Canvas->swatch.Time() < (unsigned int) (P_Dur * 1000)) {
            wxTheApp->Yield(true);
            wxMilliSleep(20);
        }
        Canvas->DisplayState=DISP_Blank;
        Canvas->Refresh();
//        Canvas->Update();
        wxTheApp->Yield(true);
        while (P_SelfPaced && !Canvas->Response) { // wait extra time here if self-paced
            wxTheApp->Yield(true);
            wxMilliSleep(20);            
        }

        wxMilliSleep((unsigned int) (P_ISI * 1000));

        LogFile->AddLine(wxString::Format("%d\t%d\t%ld\t",trial+1,Canvas->Response,Canvas->RT)+P_StudyStim[trial]);

    }
 //   delete Canvas->DisplayedImage;
 //   Canvas->DisplayedImage = NULL;
    
    return false;
}

bool c_DisplayFrame::ShowTestPhase() {
    int trial;
    
    wxFileName tmp_fname(Resource_path);
    
    // Setup touch labels
	if (P_2ChoiceTest) {
		P_NPossibleResponses = 2;
		P_TouchLabels.Clear();
		P_TouchLabels.Add(_("Old"));
		P_TouchLabels.Add(_("New"));
	}
	else {
		P_NPossibleResponses = 3;
		P_TouchLabels.Clear();
		P_TouchLabels.Add(_("Old"));
		P_TouchLabels.Add(_("Similar"));
		P_TouchLabels.Add(_("New"));
	}

	// Get instructions up
    Canvas->DisplayState = DISP_TestInstructions;
    Canvas->Refresh();
    
    
	if (P_2ChoiceTest)
		LogFile->AddLine("O/N Test phase started at: " + wxNow());
	else
		LogFile->AddLine("O/S/N Test phase started at: " + wxNow());
    LogFile->AddLine("Trial\tImg\tCond\tLBin\tResp\tAcc\tRT");
    
    
    while (1) { // Loop waiting to start or to bail
        if (Canvas->Response == RESP_Break) {
            Canvas->DisplayState = DISP_Blank;
            Canvas->Refresh();
            return true;
        }
        else if (Canvas->Response == RESP_Start) {
            break;
        }
        wxMilliSleep(50);
        wxTheApp->Yield(true);
    }
    
    int total_trials = (int) (P_RepeatStim.GetCount() + P_LureStim.GetCount() + P_FoilStim.GetCount());
    wxArrayString TrialOrder;
    TrialOrder.Add("T",P_RepeatStim.GetCount());
    TrialOrder.Add("L",P_LureStim.GetCount());
    TrialOrder.Add("F",P_FoilStim.GetCount());
    PermuteArrayString(TrialOrder);
    wxString logline;
    
    int R_cnt, L_cnt, F_cnt;
    R_cnt = L_cnt = F_cnt = 0;
    int LureBin, correct, N_correct;
    
    int LO, LS, LN;  // Accumulators for responses for lure-old, lure-sim, lure-new ...
    int TO, TS, TN;
    int FO, FS, FN;
    LO = LS = LN = TO = TS = TN = FO = FS = FN = N_correct = 0;
    int LOBin[5] = {0,0,0,0,0};
    int LSBin[5] = {0,0,0,0,0};
    int LNBin[5] = {0,0,0,0,0};
    int LNoRespBin[5] = {0,0,0,0,0};
    
    int start_trial = 0;
    int end_trial = total_trials;
    if (P_CustomMode == CUSTOM_JS) {
        if (P_Phase == 2) { // phase 2A
            total_trials = total_trials / 2;
            start_trial = 0;
            end_trial = total_trials;
        }
        else if (P_Phase == 3) { // phase 2B
            total_trials = total_trials / 2;
            start_trial = total_trials;
            end_trial = total_trials * 2;
			for (trial=0; trial<total_trials; trial++) {  // Increment the counters to pick up where we left off
                if (TrialOrder[trial] == "T")
                    R_cnt++;
                else if (TrialOrder[trial] == "L")
                    L_cnt++;
                else if (TrialOrder[trial] == "F")
                    F_cnt++;
            }

        }
    }
   
    for (trial = start_trial; trial < end_trial; trial++) {  // Main trial loop
        if (Canvas->Response == RESP_Break) {
            LogFile->AddLine("***** RUN ABORTED WITH ESC KEY ******");
            break;
        }
        logline = wxString::Format("%d\t",trial+1);
        
        // Figure name of image and setup logging of early bits
        tmp_fname.Assign(Resource_path);
        tmp_fname.AppendDir(P_Set);
        LureBin = 0;
        if (TrialOrder[trial] == "T") {
            tmp_fname.SetFullName(P_RepeatStim[R_cnt]);
            R_cnt++;
        }
        else if  (TrialOrder[trial] == "L") {
            tmp_fname.SetFullName(P_LureStim[L_cnt]);
            long lval;
            tmp_fname.GetName().ToLong(&lval);  // extract the number portion of the filename
            if ((lval < 1) || (lval > N_STIM_PER_LIST)) {
                LogFile->AddLine("ERROR - bad lure bin!!!");
            }
            else {
                LureBin = SetBins[P_SetIndex][lval-1];
                L_cnt++;
            }
        }
        else if (TrialOrder[trial] == "F") {
            tmp_fname.SetFullName(P_FoilStim[F_cnt]);
            F_cnt++;
        }
        else {  // Bad trial type -- we'll bail as something is really amok
            wxMessageBox("Error - unknown trial type");
            return true;
        }
        logline = logline + tmp_fname.GetName() + "\t" + TrialOrder[trial] + wxString::Format("\t%d\t",LureBin);
        
        // Display the image and gather response (resp and RT actually done in "canvas" in the background keyboard handler)
        Canvas->DisplayState=DISP_Stim;
        Canvas->DisplayedImage->LoadFile(tmp_fname.GetFullPath());
		if (P_ScreenScalingFactor > 1.0) {
			Canvas->DisplayedImage->Rescale((int) (P_ScreenScalingFactor * Canvas->DisplayedImage->GetWidth()), 
				(int) (P_ScreenScalingFactor * Canvas->DisplayedImage->GetHeight()));
		}
        Canvas->Response = RESP_None; Canvas->RT=0;
        Canvas->Refresh();
        Canvas->swatch.Start();
        while (Canvas->swatch.Time() < (unsigned int) (P_Dur * 1000)) {
            wxTheApp->Yield(true);
            wxMilliSleep(20);
        }
        Canvas->DisplayState=DISP_Blank;
        Canvas->Refresh();
        wxTheApp->Yield(true);
        
        while (P_SelfPaced && !Canvas->Response) { // wait extra time here if self-paced
            wxTheApp->Yield(true);
            wxMilliSleep(20);            
        }

        // Score the response
        correct = 0;
		if (P_2ChoiceTest) {
			switch (Canvas->Response) {
			case RESP_1: // Said old
				if (TrialOrder[trial] == "T") { TO++; correct = 1; }
				else if (TrialOrder[trial] == "L") { LO++; LOBin[LureBin - 1]++; }
				else { FO++; }
				break;
			case RESP_2: // Response 2 and 3 will code as "new"
			case RESP_3: // 
				if (TrialOrder[trial] == "T") { TN++; }
				else if (TrialOrder[trial] == "L") { LN++; LNBin[LureBin - 1]++; correct = 1; }
				else { FN++; correct = 1; }
				break;
			default:
				Canvas->RT = 0;
				if (TrialOrder[trial] == "L") { LNoRespBin[LureBin - 1]++; }
			}

		}
		else {
			switch (Canvas->Response) {
			case RESP_1: // Said old
				if (TrialOrder[trial] == "T") { TO++; correct = 1; }
				else if (TrialOrder[trial] == "L") { LO++; LOBin[LureBin - 1]++; }
				else { FO++; }
				break;
			case RESP_2: // Said similar
				if (TrialOrder[trial] == "T") { TS++; }
				else if (TrialOrder[trial] == "L") { LS++; correct = 1; LSBin[LureBin - 1]++; }
				else { FS++; }
				break;
			case RESP_3: // Said new
				if (TrialOrder[trial] == "T") { TN++; }
				else if (TrialOrder[trial] == "L") { LN++; LNBin[LureBin - 1]++; }
				else { FN++; correct = 1; }
				break;
			default:
				Canvas->RT = 0;
				if (TrialOrder[trial] == "L") { LNoRespBin[LureBin - 1]++; }
			}
		}
        if (correct) N_correct++;
        logline = logline + wxString::Format("%d\t%d\t%ld",Canvas->Response, correct, Canvas->RT);
        LogFile->AddLine(logline);
        LogFile->Write(); // dump to file / clear cache
        
        wxMilliSleep((unsigned int) (P_ISI * 1000));
    }
    int total_T = TO + TN + TS;
    int total_L = LO + LN + LS;
    int total_F = FO + FN + FS;
    LogFile->AddLine(wxString::Format("\n\nSummary for %d correct responses\nCorrected rates (Raw rates, raw counts)",N_correct));
    LogFile->AddLine(wxString::Format("Old|Target\t%.2f (%.2f %d)",(float) TO / total_T, (float) TO / P_NStimPerSet,TO));
	if (!P_2ChoiceTest)
		LogFile->AddLine(wxString::Format("Similar|Target\t%.2f (%.2f %d)",(float) TS / total_T, (float) TS / P_NStimPerSet,TS));
    LogFile->AddLine(wxString::Format("New|Target\t%.2f (%.2f %d)",(float) TN / total_T, (float) TN / P_NStimPerSet,TN));
    
    LogFile->AddLine(wxString::Format("Old|Lure\t%.2f (%.2f %d)",(float) LO / total_L, (float) LO / P_NStimPerSet,LO));
	if (!P_2ChoiceTest)
		LogFile->AddLine(wxString::Format("Similar|Lure\t%.2f (%.2f %d)",(float) LS / total_L,(float) LS / P_NStimPerSet,LS));
    LogFile->AddLine(wxString::Format("New|Lure\t%.2f (%.2f %d)",(float) LN / total_L,(float) LN / P_NStimPerSet,LN));

    LogFile->AddLine(wxString::Format("Old|Foil\t%.2f (%.2f %d)",(float) FO / total_F,(float) FO / P_NStimPerSet,FO));
	if (!P_2ChoiceTest)
		LogFile->AddLine(wxString::Format("Similar|Foil\t%.2f (%.2f %d)",(float) FS / total_F,(float) FS / P_NStimPerSet,FS));
    LogFile->AddLine(wxString::Format("New|Foil\t%.2f (%.2f %d)",(float) FN / total_F,(float) FN / P_NStimPerSet,FN));
    LogFile->AddLine("Note, | means 'given', so Old | Lure means they said 'old' to a lure");
    LogFile->AddLine("Raw rates are out of the total number of trials for that type, corrected for no-responses.");
    
    LogFile->AddLine("\nLure Bin Statistics (raw counts)");
	if (!P_2ChoiceTest) {
		LogFile->AddLine("L1O\tL1S\tL1N\tL2O\tL2S\tL2N\tL3O\tL3S\tL3N\tL4O\tL4S\tL4N\tL5O\tL5S\tL5N\tLNR");
		LogFile->AddLine(wxString::Format("%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d",
			LOBin[0], LSBin[0], LNBin[0],
			LOBin[1], LSBin[1], LNBin[1],
			LOBin[2], LSBin[2], LNBin[2],
			LOBin[3], LSBin[3], LNBin[3],
			LOBin[4], LSBin[4], LNBin[4]));
	}
	else {
		LogFile->AddLine("L1O\tL1N\tL2O\tL2N\tL3O\tL3N\tL4O\tL4N\tL5O\tL5N\tLNR");
		LogFile->AddLine(wxString::Format("%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d",
			LOBin[0], LNBin[0],
			LOBin[1], LNBin[1],
			LOBin[2], LNBin[2],
			LOBin[3], LNBin[3],
			LOBin[4], LNBin[4]));

	}
 
	LogFile->AddLine(("L1-NR\tL2-NR\tL3-NR\tL4-NR\tL5-NR"));
    LogFile->AddLine(wxString::Format("%d\t%d\t%d\t%d\t%d",
                                      LNoRespBin[0],LNoRespBin[1],LNoRespBin[2],LNoRespBin[3],LNoRespBin[4]));
    
    LogFile->AddLine(wxString::Format("\nResponse totals (out of %d expected)\n",N_STIM_PER_SET));
    LogFile->AddLine(wxString::Format("Target: %d\nLure: %d\nFoil: %d\n",total_T, total_L, total_F));
    
    float pc = 0.0;
    if (N_correct) pc = (float) N_correct / (float) (total_T + total_L + total_F) * 100.0;
    LogFile->AddLine(wxString::Format("\nPercent correct (corrected): %.2f",pc));
    LogFile->AddLine(wxString::Format("\nPercent correct (raw): %.2f",(float) N_correct / (float) (3*P_NStimPerSet) * 100.0));
	float bmetric = 0.0;
	if (!P_2ChoiceTest) {
		if (N_correct && !P_2ChoiceTest) bmetric = ((float)(LS) / (float)total_L) - ((float)(FS) / (float)total_F);
		bmetric = bmetric * 100.0;
		LogFile->AddLine(wxString::Format("Bias metric (S|L-S|F): %.2f", bmetric));
	}
	else {
		float pOT, pOL, pOF;
        pOT = pOL = pOF = 0.0;
		// Calc the p("Old"|TrialType) values
		if (TO)
			pOT = (float)TO / (float)total_T;
        else
            pOT = 0.5 / (float) P_NStimPerSet;
		if (LO)
			pOL = (float)LO / (float)total_L;
        else
            pOL = 0.5 / (float) P_NStimPerSet;
		if (FO)
			pOF = (float)FO / (float)total_F;
        else
            pOF = 0.5 / (float) P_NStimPerSet;

		// Calc d' values
		float dpTF, dpTL, dpLF;
		dpTF = NormalCDFInverse(pOT) - NormalCDFInverse(pOF) ;
		dpTL = NormalCDFInverse(pOT) - NormalCDFInverse(pOL);
		dpLF = NormalCDFInverse(pOL) - NormalCDFInverse(pOF);

		LogFile->AddLine(wxString::Format("d' Target:Foil %.2f (pOT=%.2f, pOF=%.2f)", dpTF,pOT,pOF));
		LogFile->AddLine(wxString::Format("d' Target:Lure %.2f (pOT=%.2f, pOL=%.2f)", dpTL,pOT,pOL));
		LogFile->AddLine(wxString::Format("d' Lure:Foil %.2f (pOL=%.2f, pOF=%.2f)", dpLF,pOL,pOF));
	}
    LogFile->Write(); 
    
    //wxMessageBox(wxString::Format("Subject Code: C%dS%d",(int) (pc * 100), (int) (bmetric*100)));
    SetStatusText(wxString::Format("Code: C%dS%d",(int) pc, (int) bmetric));
    return false;
}


c_HelpWindow::c_HelpWindow(wxWindow *parent)
: wxFrame(parent, wxID_ANY, "Experimenter instructions", wxDefaultPosition, wxSize(-1,-1)) {

    wxBoxSizer *topsizer = new wxBoxSizer(wxVERTICAL);
    maintext = new wxTextCtrl(this,wxID_ANY, "Welcome to the MST\n\n",wxDefaultPosition,
                                          wxSize(700,400),wxTE_MULTILINE|wxTE_READONLY|wxTE_RICH);
    
    (*maintext) << "The experiment consists of two phases: 1) an incidental study phase and 2) an explicit test phase. Each participant must get both and you should ideally run them without shutting MST down between phases (see Participant IDs and Randomization below).  At the end of the test phase, you'll get a score for the participant in the form of a cryptic code in the status bar (intentionally cryptic) along with a log file.  The code is C#S# with the #s being the percent correct and the bias metric.\n\n";
    maintext->SetDefaultStyle(wxTextAttr(*wxBLUE));
    (*maintext) << "Parameters\n";
    maintext->SetDefaultStyle(wxTextAttr(*wxBLACK));
    (*maintext) << "- ID: Participant identifier.  This should be a number or should start with a number if you know what's good for you (see below on Participant IDs and Randomization).  But, it can be any text if you like living on the wild side.  This is used to assign which stimuli go to a participant (again, see below) and is part of the log file name (see Output dir).\n";
    (*maintext) << "- Dur: Duration of presentation of images (default is 2 seconds)\n";
    (*maintext) << "- ISI: Inter-stimulus-interval or blank screen between images (default is 0.5 seconds)\n";
    (*maintext) << "- # Per cond: # of stimuli per T/F/L condition (default and max is 64, min is 8)\n";
    (*maintext) << "- Set C/D/E/F: Which of 4 independent, stimulus sets should we use? (no, there aren't A and B): Note - C/D are matched and E/F are matched\n";
    (*maintext) << "- Set 1-6: These are reshuffles of Sets C-H to make 6 independent, matched sets.  Of course, they are not independent of Sets C-H (G and H were not publicly released).\n";
    (*maintext) << "- Phase 1 vs Phase 2: Phase 1 (incidental study) or 2 (explicit old/similar/new test)?\n"; 
    (*maintext) << "- Output dir: By default, plain text log files (see below) are generated in 'My Documents' on Windows or 'Documents' on a Mac.  This button will let you select an alternate output location.\n";
    (*maintext) << "- Self-paced: If checked, the stimulus will still appear for the time given in Dur, but participatnts will have as much time as they like to make the actual response (albeit to a potentially blank screen).\n";
    (*maintext) << "- Enable touch: If checked, touch-zones on the bottom of the screen will appear to allow for touches (or mouse clicks) rather than key presses.\n";

    
    maintext->SetDefaultStyle(wxTextAttr(*wxBLUE));
    (*maintext) << "\nParticipant IDs and Randomization\n";
    maintext->SetDefaultStyle(wxTextAttr(*wxBLACK));
   // (*maintext) << "MST will assign which of the " << N_STIM_PER_SET << " stimuli go to which conditions (target, lure, foil) based on the Subject ID if this is (or starts with) a number.  So, if you use a number here, you can run the study (Phase 1) and the test (Phase 2) on separate days, sessions, computers, etc.  (Technically, there are 6 combinations and it's done as the ID number modulo 6).  If MST can't find a number in there, it generates a random one.  This is fine, so long as you don't need to recreate the same exact study scenario.\n";
    (*maintext) << "MST will assign the " << N_STIM_PER_LIST << " stimuli from a set to the conditions (target, lure, foil) and determine the randomization of the trial order based on the subject ID.  If this is a number (or starts with a number) it will use this as the random number seed.  So, if you use a number here, you can run the study (Phase 1) and the test (Phase 2) on separate days, sessions, computers, etc. and be assured to get the same stimulus set assignments.  If it doesn't have a number, MST uses the first three (or 1 if there aren't at least 3) characters to generate the random seed.\n";
    (*maintext) << "\nDuring the randomization of stimuli to condition, MST ensures an even distribution of lure bins (or as best as it can, given the 5 bins of lures).  All stimulus pairs can be target pairs, lure paris, or foils.  But, only the 'a' versions are shown at study and only the 'b' versions are shown as lures.\n";
    
    maintext->SetDefaultStyle(wxTextAttr(*wxBLUE));
    (*maintext) << "\nLog files\n";
    maintext->SetDefaultStyle(wxTextAttr(*wxBLACK));
    (*maintext) << "MST creates simple text files with copious amounts of information in them.  If the log file already exists, it will simply append the new information, so you needn't fear losing data.  All parameters are logged along with which stimuli are assigned to which conditons and when anything was run.  For the study and test phases, there are tab-separated tables for easy import into a spreadsheet.\n";
    (*maintext) << "\nAt the end of the test phase, a summary table is written with the rates and raw counts for each of the 9 possible response-category pairings.  You will see things like New|Target.  The | here means 'given' so this would indicate the rate at which the participant said new to the target (repeated) stimuli (aka these are false alarms).\n";
    (*maintext) << "\nFinally, there is a percent correct and a bias metric score (probability of calling lure items similar minus the probability of calling new items similar).\n";
    
    maintext->SetDefaultStyle(wxTextAttr(*wxBLUE));
    (*maintext) << "\nStimulus timing\n";
    maintext->SetDefaultStyle(wxTextAttr(*wxBLACK));
    (*maintext) << "Please note there that timing here is going to be approximate, both in terms of the stimlus presentation time and in terms of the reaction times.  Don't expect that just because there may be 192 test trials of 2.5 seconds each that it will take exactly 8 minutes.  It will take a bit longer.  For behavioral work this is nothing for any concern and is common in most software.  If you need high precision for things like use inside scanners, use the MATLAB version.  RTs will be somewhat quantized for a given trial, but this should not significantly affect the average RT across many trials.\n";

	maintext->SetDefaultStyle(wxTextAttr(*wxBLUE));
    (*maintext) << "\nMisc\n";
    maintext->SetDefaultStyle(wxTextAttr(*wxBLACK));
    (*maintext) << "- To test out your responses, on the intial screen where it has the logo, just press your keys and you'll see what was picked up in the status bar\n";
	(*maintext) << "- Sets C and D are well matched to each other as are E and F, but the E&F group is a bit easier than the C&D set.  We have conversion tools to map these scores onto C&D scores.";
    (*maintext) << "- Sets 1-6 combine the stimuli from Sets C-F and add in the unreleased G&H sets, shuffling these based on testing here to create 6 matched sets.  Given the ability to run sublists (e.g., 32 per condition) this gives the option for many test-retest sessions with unique stimuli (12 if you use 32 per, 18 if you use 20 per, etc).";
	
	topsizer->Add(maintext,1,wxALL | wxEXPAND,5);
    maintext->SetMinSize(wxSize(300,200));
    maintext->SetInitialSize(wxSize(700,400));
    SetSizerAndFit(topsizer);
    maintext->SetInsertionPoint(0); // scroll to top
    Show(false);

}

void c_DisplayFrame::OnHelp(wxCommandEvent& WXUNUSED(evt)) {
    HelpWindow->Show(true);
    HelpWindow->maintext->ShowPosition(1);
}

bool c_DisplayFrame::SavePrefs() {
    wxConfig *config = new wxConfig("MST");
	config->SetPath("/Preferences");

    config->Write("Language",(long) P_Language);
    config->Write("NStimPerSet",(long) P_NStimPerSet);
    config->Write("Dur",(double) P_Dur);
    config->Write("ISI",(double) P_ISI);
    config->Write("SelfPaced",P_SelfPaced);
	config->Write("AllowTouch", P_AllowTouch);
	config->Write("TwoChoiceTest", P_2ChoiceTest);
    config->Write("Randomization",P_Randomization);
    config->Write("Resp1Keys",P_Resp1Keys);
    config->Write("Resp2Keys",P_Resp2Keys);
    config->Write("Resp3Keys",P_Resp3Keys);
    config->Write("CustomMode",P_CustomMode);
    
    delete config;
    
    return false;
}

bool c_DisplayFrame::LoadPrefs() {
    long lval;
    double dval;
    bool bval;
    
    wxConfig *config = new wxConfig("MST");
	lval = 0;
    dval = 0.0;

	config->SetPath("/Preferences");
    
    lval = (long) P_Language;
    config->Read("Language",&lval);
    P_Language = (wxLanguage) lval;
    if ((P_Language == wxLANGUAGE_ENGLISH) || (P_Language == wxLANGUAGE_DEFAULT) ||
        (P_Language == wxLANGUAGE_UNKNOWN))
        P_Language = wxLANGUAGE_ENGLISH_US;
    
    lval = (long) P_NStimPerSet;
    config->Read("NStimPerSet",&lval);
    P_NStimPerSet = (int) lval;
    
    dval = (double) P_Dur;
    config->Read("Dur",&dval);
    P_Dur = (float) dval;
    
    dval = (double) P_ISI;
    config->Read("ISI",&dval);
    P_ISI = (float) dval;
    
    bval = P_SelfPaced;
    config->Read("SelfPaced",&bval);
    P_SelfPaced = bval;

	bval = P_AllowTouch;
	config->Read("AllowTouch", &bval);
	P_AllowTouch = bval;

	bval = P_2ChoiceTest;
	config->Read("TwoChoiceTest", &bval);
	P_2ChoiceTest = bval;

    config->Read("Resp1Keys",&P_Resp1Keys);
    config->Read("Resp2Keys",&P_Resp2Keys);
    config->Read("Resp3Keys",&P_Resp3Keys);
    
    lval = P_CustomMode;
    config->Read("CustomMode",&lval);
    P_CustomMode = lval;
    
	delete config;

    return false;
}

double RationalApproximation(double t) {
    // https://www.johndcook.com/blog/normal_cdf_inverse/
    // Abramowitz and Stegun formula 26.2.23.
    // The absolute value of the error should be less than 4.5 e-4.
    double c[] = {2.515517, 0.802853, 0.010328};
    double d[] = {1.432788, 0.189269, 0.001308};
    return t - ((c[2]*t + c[1])*t + c[0]) /
    (((d[2]*t + d[1])*t + d[0])*t + 1.0);
}

double NormalCDFInverse(double p) {
    // https://www.johndcook.com/blog/normal_cdf_inverse/
    if (p <= 0.0 || p >= 1.0) {
        return 0.0;
    }
    
    // See article above for explanation of this section.
    if (p < 0.5)
    {
        // F^-1(p) = - G^-1(p)
        return -RationalApproximation( sqrt(-2.0*log(p)) );
    }
    else
    {
        // F^-1(p) = G^-1(1-p)
        return RationalApproximation( sqrt(-2.0*log(1-p)) );
    }
}

double phi(double x) {
    // constants
    double a1 =  0.254829592;
    double a2 = -0.284496736;
    double a3 =  1.421413741;
    double a4 = -1.453152027;
    double a5 =  1.061405429;
    double p  =  0.3275911;
    
    // Save the sign of x
    int sign = 1;
    if (x < 0)
        sign = -1;
    x = fabs(x)/sqrt(2.0);
    
    // A&S formula 7.1.26
    double t = 1.0/(1.0 + p*x);
    double y = 1.0 - (((((a5*t + a4)*t) + a3)*t + a2)*t + a1)*t*exp(-x*x);
    
    return 0.5*(1.0 + sign*y);
}
