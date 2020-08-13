//
//  files.cpp
//  BPSO
//
//  Created by Craig Stark on 11/11/11.
//  Copyright 2011 Craig Stark. All rights reserved.
//

#include <wx/wx.h>
#include <wx/stdpaths.h>
#include <wx/filename.h>
#include <wx/wfstream.h>
#include <wx/txtstrm.h>


#include "main.h"

void PermuteArrayString(wxArrayString &arry) {
    // Randomly permute the lists using a Fisher-yates method
    long i, r_index;
    wxString tmpstr;
    for (i=arry.GetCount()-1; i>0; i--) {
        r_index = rand() % (i+1);
        tmpstr = arry[i];
        arry[i]=arry[r_index];
        arry[r_index]=tmpstr;
    }
}


bool c_DisplayFrame::CheckFiles(wxString SetName) {
    // Checks to make sure there are the right #of images in the image directories
    // Loads the lure bin ratings
    int SetInd=0;

    wxStandardPathsBase& StdPaths = wxStandardPaths::Get(); 
    wxString res_path_str = StdPaths.GetResourcesDir();
    
    Resource_path.AssignDir(res_path_str);
    wxFileName tmp_fname(Resource_path);
    
    if (SetName == "C")
        SetInd = 0;
    else if (SetName == "D")
        SetInd = 1;
    else if (SetName == "E")
        SetInd = 2;
    else if (SetName == "F")
        SetInd = 3;
    else if (SetName == "1")
        SetInd = 4;
    else if (SetName == "2")
        SetInd = 5;
    else if (SetName == "3")
        SetInd = 6;
    else if (SetName == "4")
        SetInd = 7;
    else if (SetName == "5")
        SetInd = 8;
    else if (SetName == "6")
        SetInd = 9;
    else if (SetName == "ScC")
        SetInd = 10;

    // Read in the bins list and check it
    tmp_fname.Assign(Resource_path);
    tmp_fname.SetFullName("Set" + SetName + " bins.txt");
    if (!tmp_fname.IsFileReadable()) {
        wxMessageBox("Cannot read bins for Set " + SetName + "\n" + tmp_fname.GetFullPath());
        return true;
    }
    wxFileInputStream input_s(tmp_fname.GetFullPath());
    if (!input_s.IsOk()) {
        wxMessageBox("Failed to open input stream from\n"+ tmp_fname.GetFullPath());
        return true;
    }
    wxTextInputStream text_s(input_s);
    
    int i;
    wxInt16 i16;
    for (i=0; i<N_STIM_PER_LIST; i++) {
        text_s >> i16; // Should be the stim number
        if (input_s.Eof()) {
            wxMessageBox("Set " + SetName + " bin file too short");
            return true;
        }
        if ((i16 > N_STIM_PER_LIST) || (i16 < 0)) {
            wxMessageBox("Invalid stim value in Set " + SetName + " bin file");
            return true;
        }
        text_s >> i16;  // Should be the bin number
        if (input_s.Eof() && (i<(N_STIM_PER_LIST-1))) {
            wxMessageBox("Set " + SetName + " bin file too short");
            return true;
        }
        if ((i16 > 5) || (i16 < 1)) {
            wxMessageBox("Invalid bin value in Set " + SetName + " bin file");
            return true;
        }
        SetBins[SetInd][i] = (int) i16;
    }
    
    
    // Check that the stimulus directories are there and seem reasonable
    tmp_fname.Assign(Resource_path);
    tmp_fname.AppendDir("Set " + SetName);
    if (!tmp_fname.DirExists()) {
        wxMessageBox("Cannot find Set " + SetName + " stimulus directory\n" + tmp_fname.GetFullPath());
        return true;
    }
    for (i=1; i<=N_STIM_PER_LIST; i++) {
        tmp_fname.SetFullName(wxString::Format("%03da.jpg",i));
        if (!tmp_fname.IsFileReadable()) {
            wxMessageBox(wxString::Format(SetName + ": Cannot find %03da.jpg",i));
            return true;
        }
        tmp_fname.SetFullName(wxString::Format("%03db.jpg",i));
        if (!tmp_fname.IsFileReadable()) {
            wxMessageBox(wxString::Format(SetName + ": Cannot find %03db.jpg",i));
            return true;
        }        
    }
    
    
    if (Logo == NULL) {
        tmp_fname.Assign(Resource_path);
        tmp_fname.SetFullName("MST_Logo.png");
        Logo = new wxImage();
        if (tmp_fname.IsFileReadable()) {  // Load logo if we have it
            Logo->LoadFile(tmp_fname.GetFullPath());
			if (P_ScreenScalingFactor > 1.0) {
				Logo->Rescale((int) (P_ScreenScalingFactor * Logo->GetWidth()), (int) (P_ScreenScalingFactor * Logo->GetHeight()));
			}
		}

    }
    return false;
}

bool c_DisplayFrame::SetupListsPermuted() {
    // Assumes CheckFiles() has been run so we have the bin numbers for each stimulus
    // Also should by now know which set we're running
    
    if ((P_Set != "Set C") && (P_Set != "Set D") && (P_Set != "Set E") && (P_Set != "Set F")
        && (P_Set != "Set 1") && (P_Set != "Set 2") && (P_Set != "Set 3") && (P_Set != "Set 4")
        && (P_Set != "Set 5") && (P_Set != "Set 6") && (P_Set != "Set ScC")) {
        wxMessageBox("Unknown set - badness has happened..." + P_Set + ".");
        return true;
    }
    
    int i;

    // Clean out existing lists
    if (P_StudyStim.GetCount()) P_StudyStim.Empty();
    if (P_RepeatStim.GetCount()) P_RepeatStim.Empty();
    if (P_LureStim.GetCount()) P_LureStim.Empty();
    if (P_FoilStim.GetCount()) P_FoilStim.Empty();
    
    // Set the random seed so that every time we call this for this Subject we get the same setup
    if (P_Randomization) // We have some seed...
        srand((unsigned int) P_Randomization);
    else { // Using ID number
        long idnum;
        if (P_SubjID.ToLong(&idnum))  // if there is a # in the ID, use it
            srand((unsigned int) idnum);
        else {
            if (P_SubjID.Length() >= 3)
                idnum = (long) P_SubjID[0] + (long) P_SubjID[1] + (long) P_SubjID[0];
            else
                idnum = (long) P_SubjID[0];
            srand((unsigned int) idnum);
        }
        
    }

    
    // Figure out which lures are in which bins and make arrays of each.  Do this on all possible stim.
    // For now, we'll leave off the "b.jpg" bit
    wxArrayString Lure1, Lure2, Lure3, Lure4, Lure5;
    for (i=1; i<=N_STIM_PER_LIST; i++) {
        switch (SetBins[P_SetIndex][i-1]) {
            case 1:
                Lure1.Add(wxString::Format("%03d",i)); break;
            case 2:
                Lure2.Add(wxString::Format("%03d",i)); break;
            case 3:
                Lure3.Add(wxString::Format("%03d",i)); break;
            case 4:
                Lure4.Add(wxString::Format("%03d",i)); break;
            case 5:
                Lure5.Add(wxString::Format("%03d",i)); break;
            default:
                wxMessageBox("Unknown lure bin - badness...");
                return true;
        }
    }
    
    PermuteArrayString(Lure1);  // Randomly order these
    PermuteArrayString(Lure2);
    PermuteArrayString(Lure3);
    PermuteArrayString(Lure4);
    PermuteArrayString(Lure5);
    
    // Setup the Lures to evenly use lure bins 1-5.  Do this for the max of 64 we can use
    int l1ctr, l2ctr, l3ctr, l4ctr, l5ctr;
    l1ctr = l2ctr = l3ctr = l4ctr = l5ctr = 0;
    for (i=1; i<=N_STIM_PER_SET; i++) {
        switch ((i % 5) + 1) {
            case 1: 
                P_LureStim.Add(Lure1[l1ctr++]); break;
            case 2: 
                P_LureStim.Add(Lure2[l2ctr++]); break;
            case 3: 
                P_LureStim.Add(Lure3[l3ctr++]); break;
            case 4: 
                P_LureStim.Add(Lure4[l4ctr++]); break;
            case 5: 
                P_LureStim.Add(Lure5[l5ctr++]); break;
                
        }
    }
    
    // Figure out the remaining stimuli to make the Repeats and Foils
    wxArrayString NonLures;
    for (i=1; i<=N_STIM_PER_LIST; i++) {
        if (P_LureStim.Index(wxString::Format("%03d",i)) == wxNOT_FOUND) {
            NonLures.Add(wxString::Format("%03d",i));
        }
    }
    
    // Randomize the non-lure (repeat/foil) list
    PermuteArrayString(NonLures);
    
    // Assign the targets and foils -- again to the full 64-item strength (we'll trim later)
    int ctr=0;
    for (i=0; i<N_STIM_PER_SET; i++) {
        P_RepeatStim.Add(NonLures[ctr++]);
        P_FoilStim.Add(NonLures[ctr++]);
    }
    
    // At this point, we've assigned stimuli to lure, repeat, and foil lists in full 64-length
    // sets.  Cut these down now to the size we're using and to the starting point we're using
    
    if (P_NStimPerSet == 32) {
        if (P_SubList == 1) {  // Cut off last bits
            P_RepeatStim.RemoveAt(P_NStimPerSet,N_STIM_PER_SET-P_NStimPerSet);
            P_FoilStim.RemoveAt(P_NStimPerSet,N_STIM_PER_SET-P_NStimPerSet);
            P_LureStim.RemoveAt(P_NStimPerSet,N_STIM_PER_SET-P_NStimPerSet);
        }
        else {  // Cut off front bits
            P_RepeatStim.RemoveAt(0,N_STIM_PER_SET-P_NStimPerSet);
            P_FoilStim.RemoveAt(0,N_STIM_PER_SET-P_NStimPerSet);
            P_LureStim.RemoveAt(0,N_STIM_PER_SET-P_NStimPerSet);
       }
    }
    else if (P_NStimPerSet == 20) {
        if (P_SubList == 1) {  // Cut off last bits
            P_RepeatStim.RemoveAt(P_NStimPerSet,N_STIM_PER_SET-P_NStimPerSet);
            P_FoilStim.RemoveAt(P_NStimPerSet,N_STIM_PER_SET-P_NStimPerSet);
            P_LureStim.RemoveAt(P_NStimPerSet,N_STIM_PER_SET-P_NStimPerSet);
        }
        else if (P_SubList == 3) {  // Cut off front bits
            P_RepeatStim.RemoveAt(0,N_STIM_PER_SET-P_NStimPerSet);
            P_FoilStim.RemoveAt(0,N_STIM_PER_SET-P_NStimPerSet);
            P_LureStim.RemoveAt(0,N_STIM_PER_SET-P_NStimPerSet);
        }
        else { // Cut out the middle
            P_RepeatStim.RemoveAt(0,P_NStimPerSet);
            P_RepeatStim.RemoveAt(P_NStimPerSet,N_STIM_PER_SET-P_NStimPerSet-P_NStimPerSet);
            P_FoilStim.RemoveAt(0,P_NStimPerSet);
            P_FoilStim.RemoveAt(P_NStimPerSet,N_STIM_PER_SET-P_NStimPerSet-P_NStimPerSet);
            P_LureStim.RemoveAt(0,P_NStimPerSet);
            P_LureStim.RemoveAt(P_NStimPerSet,N_STIM_PER_SET-P_NStimPerSet-P_NStimPerSet);
        }
    }
	else if (P_NStimPerSet == 40) {
        P_RepeatStim.RemoveAt(P_NStimPerSet,N_STIM_PER_SET-P_NStimPerSet);
        P_FoilStim.RemoveAt(P_NStimPerSet,N_STIM_PER_SET-P_NStimPerSet);
        P_LureStim.RemoveAt(P_NStimPerSet,N_STIM_PER_SET-P_NStimPerSet);
	}

    // Shuffle the lure list - still in L1, L2, L3, L4, L5 order at this point
    PermuteArrayString(P_LureStim);

    
    
    // Create the study list
    for (i=0; i<P_NStimPerSet; i++) {
        P_StudyStim.Add(P_RepeatStim[i] + wxString("a.jpg"));
        P_StudyStim.Add(P_LureStim[i] + wxString("a.jpg"));        
    }
    PermuteArrayString(P_StudyStim);
    
    // Finish up the test stim names
    for (i=0; i<P_NStimPerSet; i++) {
        P_LureStim[i]=P_LureStim[i] + wxString("b.jpg");
        P_RepeatStim[i]=P_RepeatStim[i] + wxString("a.jpg");
        P_FoilStim[i]=P_FoilStim[i] + wxString("a.jpg");
    }

        
    if (LogFile) { 
        LogFile->AddLine(wxString::Format("Study items (%lu)",P_StudyStim.GetCount()));
        for (i=0; i<P_NStimPerSet*2; i+=2)
            LogFile->AddLine(P_StudyStim[i] + "\t" + P_StudyStim[i+1]);
        
        LogFile->AddLine("Test items");
		LogFile->AddLine("Repeat\tLure\tFoil");
        for (i=0; i<P_NStimPerSet; i++)
            LogFile->AddLine(P_RepeatStim[i] + "\t" + P_LureStim[i] + "\t" + P_FoilStim[i]);
    }
    return false;
}



