"""
Diff with another specified branch.

Author: Fionn Ziegler

"""
from cvsgui.Macro import *
from cvsgui.CvsEntry import *
from cvsgui.Persistent import *
from cvsgui.ColorConsole import *
from cvsgui.MenuMgr import *
import cvsgui.App, os.path, string
import datetime
import time
import csv


class AITenderDiff(Macro):
	def __init__(self):
		Macro.__init__(self, "", MACRO_SELECTION,
			0, "Merge to other Branch")
                self.console = ColorConsole()

	def OnCmdUI(self, cmdui):
		# enable only if one or more cvs files are selected
		sel = cvsgui.App.GetSelection()
		isGood = len(sel) >= 1
		
		cmdui.Enable(isGood)
		if isGood:
			cmdui.SetText("Merge '%s' files" % len(sel))
		else:
			cmdui.SetText("Please select file(s)")

	def Run(self):
                self.startPatch()
                
        def startPatch(self, template=''):
                self.files = App.GetSelection()
                count = 1
                lastBranch = Persistent("PY_BRANCH", "eTenderSuite_TRUNK, eTenderSuite_5_8", 1)
                
                answer, branch_input = App.CvsPrompt(str(lastBranch), 'Question',
                                   'Enter the name(s) of the branch(es) to diff the ' \
                                  +'current selection to (Comma separated).',
                                   alertTitle='Copy to branch/trunk')
                lastBranch << branch_input

                branches = csv.reader([branch_input], skipinitialspace=True)
                for branch in branches:
                        for b in branch:
                                if answer=='IDOK':
                                        for entry in self.files:
                                            if entry.IsFile():
                                                self.loggreen ("------------------------------------------------------- %s / %s (%s) -----------------------------------------------------------------------" %(count,len(self.files), entry.GetName()))
                                                if os.path.exists(entry.GetFullName()):
                                                        self.diffFile(entry, b)
                                                else:
                                                        self.logerror("source file does not exist")
                                                count +=1

  
        def diffFile(self, filetopatch, branch):
                self.loggreen("%s to branch %s" % (filetopatch.GetName(), branch))
             
                
                path=filetopatch.GetFullName()
                index = path.find("eTenderSuite")
                if index == -1:
                        msg = "Wrong file: %s cancel?" % filetopatch
                        title = "Cancel?"
                        if cvsgui.App.CvsAlert('Question', msg, 'Yes', 'No', '', '', title) != 'IDOK':
                                return
                        
                endindex = path.find("\\",index+1,len(path))
                oldetenderSuit = path[index:endindex]
                newpath= path.replace(oldetenderSuit,branch)

                if os.path.exists(newpath):
                                #diff
                        p_extdiff = Persistent('P_Extdiff', '', 0)
                        extdiff = str(p_extdiff)
                        args = ['"%s"' % newpath, '"%s"' % path]
                        args.insert(0, '"%s"' % extdiff)
                                
                        self.loggreen("try diff %s : %s -------> %s" % (extdiff, path, newpath))

                        if extdiff <> '' and os.path.exists(extdiff):
                               os.spawnl(os.P_NOWAIT, extdiff, *args)
                               time.sleep(0.5)

                        else:
                                self.logerror("External diff tool not found: %s" %extdiff)        
        
                else:
                        self.logerror("Other file does not exist: %s" %newpath)        
                                        
                        

        def logerror(self,message):
                self.console << kRed << message << '\n' << kBold
                
        def loggreen(self,message):
                self.console << kGreen << message << '\n' << kBold

AITenderDiff()

