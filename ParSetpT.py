from array import array
import sys,csv,collections,numpy
from ROOT import gROOT, gStyle, gPad,TCanvas, TColor, TF1, TFile, TLegend, THStack, TGraph, TMath, kTRUE, kFALSE
from ROOT import RooRealVar, RooDataHist, RooPlot, RooGaussian, RooAbsData, RooFit, RooArgList,RooCBShape,RooVoigtian,RooBreitWigner,RooFFTConvPdf,RooLandau,RooBifurGauss,RooPolynomial,RooChebychev
import ROOT as rt
from RooFitHist import RooFitHist

#change to pT


# if(sys.version_info[0] != 3):
#     raise BaseException("You should run this with python 3")

#corresponding reweightingrange will be taken from first in list
channelgroups={'VV':["WPWP","WPWM","WMWM","WPZ","WMZ","ZZ"],
          'ssWW':["WPWP","WMWM"],
          'WW':["WPWP","WPWM","WMWM"],
          'WZ':["WPZ","WMZ"]}

gROOT.Reset()

sets=collections.OrderedDict()

class Set:
    def __init__(self, dim8op,channelname,Cut,region,jR=8):#maybe it's meant to use the /SignalRegion?hmm
        self.UHH2_Output = "/nfs/dust/cms/user/loemkerj/bachelor/CMSSW_10_2_16/src/UHH2/aQGCVVjjhadronic"
        gROOT.SetBatch(True)
        self.channel=channelname
        tosum=[]
        if (channelname in channelgroups):
            tosum=channelgroups[channelname]
        else:
            tosum.append(channelname)

        with open('range_short_positive.csv','rb') as csvfile:
            setreader=csv.DictReader(csvfile,delimiter=";")
            for row in setreader:
                sets.update({row['parameter']:[
                            int(row['Npoints']),
                            float(row['start']),
                            float(row['stepsize'])
                            ]})

        self.OpName=dim8op
        self.LastCut=Cut
        self.jetRadius=int(jR)
        print('Channel:',self.channel,'- Cut:',self.LastCut)

        rootdir_suffixe={"WPWP":"WPWPRange",
            "WPWM":"WPWPRange",
            "WMWM":"WPMZRange",
            "WPZ":"ZRange",
            "WMZ":"ZRange",
            "ZZ":"ZRange"}

        ################################################################################################################################
        
        ##Open Files to get SignalHists:
        gROOT.ProcessLine( "gErrorIgnoreLevel = 2001;")
        self.SFiles=[]

        for i in range(len(tosum)):
            self.SFiles.append(TFile(self.UHH2_Output + "/%s/uhh2.AnalysisModuleRunner.MC.MC_aQGC_%sjj_hadronic_2016v3.root"%(region,tosum[i])))

        ##Open File to get BackgroundHist:
        self.BFile = TFile(self.UHH2_Output + "/%s/uhh2.AnalysisModuleRunner.MC.MC_QCD.root"%region)
        
        gROOT.ProcessLine( "gErrorIgnoreLevel = 0;")

        ##Generate Names for Hists-,Filenames etc. from ReweightingRange
        self.SHistNames=[]
        fillHistNames(self.SHistNames,self.OpName)
 
        self.SHists=[]        
               
        #TODO: dirty fix for problem with histnaming (MjjHists Directoy in 1.5TeV MassSideband is missing an _allcuts in its name
        tmpCut=self.LastCut
        if('_allcuts' in tmpCut):
            tmpCut=tmpCut[:len(tmpCut)-len('_allcuts')]
        
        
        for i in range(len(tosum)):
            if(self.channel in channelgroups):
                rootdir_suffix=rootdir_suffixe[channelgroups[self.channel][i]]
            else:
                rootdir_suffix=rootdir_suffixe[self.channel]
            
            SHistDir=self.SFiles[i].GetDirectory('Kin_AK8')
            SHistkeys=SHistDir.GetListOfKeys()
            j=0
            for key in SHistkeys:
                # if( ('"M_jj_AK%i"'%self.jetRadius) in str(key)):
                #     self.RefHist=key.ReadObj()
                if ( (dim8op not in str(key)) or (('AK%i'%self.jetRadius) not in str(key))): 
                    continue
                if(i==0):
                    self.SHists.append(key.ReadObj())
                else:
                    self.SHists[j].Add(key.ReadObj())
                    j+=1
            if(i==0):                               #pT_AK8_12_T9_2p50
                self.RefHist=self.SFiles[i].Get('%s/pT_AK%i_12'%(self.LastCut,self.jetRadius))
            else:
                self.RefHist.Add(self.SFiles[i].Get('%s/pT_AK%i_12'%(self.LastCut,self.jetRadius)))
            
        # SHistDir=self.SFile.GetDirectory('MjjHists_%s_%s'%(tmpCut,Ranges[self.channel]))
        # SHistkeys=SHistDir.GetListOfKeys()

        # for key in SHistkeys:
        #     # if( ('"M_jj_AK%i"'%self.jetRadius) in str(key)):
        #     #     self.RefHist=key.ReadObj()
        #     if ( (dim8op not in str(key)) or (('AK%i'%self.jetRadius) not in str(key))): 
        #         continue
        #     self.SHists.append(key.ReadObj())

        # self.RefHist=self.SFile.Get('%s/M_jj_AK%i_highbin'%(self.LastCut,self.jetRadius))

        self.BHist=self.BFile.Get('%s/pT_AK%i_12'%(self.LastCut,self.jetRadius))
        # self.sidebandDataFile=TFile(self.UHH2_Output + '/SidebandRegion/uhh2.AnalysisModuleRunner.Data.DATA.root')
        # self.sidebandDataHist=self.sidebandDataFile.Get('%s/M_jj_AK%i_highbin'%(self.LastCut,self.jetRadius))
        ##################################################################################################################################


        #Rebin Stuff
        #dijet binning (not equidistant)
        boundaries=[1, 3, 6, 10, 16, 23, 31, 40, 50, 61, 74, 88, 103, 119, 137, 156, 176, 197, 220, 244, 270, 296, 325, 354, 386, 419, 453, 489, 526, 565, 606, 649, 693, 740, 788, 838, 890, 944, 1000, 1058, 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687, 1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337, 4509, 4686, 4869, 5058, 5253, 5455, 5663, 5877, 6099, 6328, 6564, 6808, 7060, 7320, 7589, 7866, 8152, 8447, 8752, 9067, 9391, 9726, 10072, 10430, 10798, 11179, 11571, 11977, 12395, 12827, 13272, 13732, 14000]

        self.dijetbinning = array( 'd' )
        for i in range(1,len(boundaries)):
            self.dijetbinning.append(boundaries[i])

    def CombinedRootFiles(self,path='',VBF_cut='Kin_AK8'):
        pT_suffix = '_pT'
        VBF=(self.LastCut==VBF_cut)
        if(VBF):
            name_suffix='_afterVBFsel'
        else:
            name_suffix=''

        for i in range(len(self.SHists)):         
           filename=self.getFileName(i)
           if(VBF):
               oFile= TFile(path+"/%s_pT.root"%filename,"UPDATE");
               # file= TFile(path+"/%s_SignalInjection.root"%filename,"UPDATE");
               # file= TFile(path+"/%s_SidebandData.root"%filename,"UPDATE");
           else:
               oFile= TFile(path+"/%s_pT.root"%filename,"RECREATE");
               # file= TFile(path+"/%s_SignalInjection.root"%filename,"RECREATE");
               # file= TFile(path+"/%s_SidebandData.root"%filename,"RECREATE");
           if(not oFile.IsOpen()):
               print("Error: Could not open File No. %i"%i)

           # r_newbinning=range(0,14000,100)
           # d_newbinning=array('d')
           # for b in r_newbinning:
           #     d_newbinning.append(b)
           # radion=self.SHists[i].Rebin(len(d_newbinning)-1,"new binning",d_newbinning) 
           # qcd_data=self.BHist.Rebin(len(d_newbinning)-1,"new binning",d_newbinning) 
           # radion.Write('radion_invMass'+name_suffix)
           # qcd_data.Write('qcd_invMass'+name_suffix)
           # qcd_data.Write('data_invMass'+name_suffix)

           #With SidebandData
           # signalHist=self.SHists[i]
           # backgroundHist=self.BHist
           # sidebandDataHist=self.sidebandDataHist
           # signalHist.Write('radion_invMass'+name_suffix)
           # backgroundHist.Write('qcd_invMass'+name_suffix)
           # sidebandDataHist.Write('data_invMass'+name_suffix)

           import numpy as np
           binning = np.linspace(0,8000,8001)
           signalHist=self.SHists[i].Rebin(len(binning)-1, '', binning)
           backgroundHist=self.BHist.Rebin(len(binning)-1, '', binning)
           # #For SignalInjectionTest #try this -> sig+bg shapes to pseudo sig+bg points
           #signalHist=self.SHists[i] 
           #backgroundHist=self.BHist
           fakedataHist=backgroundHist.Clone()
           fakedataHist.Add(signalHist)
           signalHist.Write('radion_pT'+name_suffix)
           backgroundHist.Write('qcd_pT'+name_suffix)
           fakedataHist.Write('data_pT'+name_suffix)

           #Standard (with Background as FakeData)-> sig +bg shape  to bg(pseudodata)points
           #self.SHists[i].Write('radion_invMass'+name_suffix)
           #self.BHist.Write('qcd_invMass'+name_suffix)
           #self.BHist.Write('data_invMass'+name_suffix)
           update_progress(i+1,len(self.SHists))
           oFile.Close()

    def RooFitSig(self,path=''):
        #new binning from 1050GeV to 14000GeV in 10GeV steps:
        #old binning is in 1GeV steps so NBins:14000 but len(bins):14001 upper boundary of last bin has to be included in rebinning array
        refhist=self.RefHist
        RooFitHist(self.RefHist,'%s_%s_refhist'%(self.channel,self.LastCut),path)
            
    def RooFitSignal(self,path=''):
        
        i = (len(self.SHists)/2)+3
        # for i in range(len(self.SHists)):
            # chi2s.append(self.SHists[i].GetName()+'- chi2:'+str(RooFitHist(self.SHists[i],"%s_%s_%s"%(self.channel,self.LastCut,self.getPointName(i)),path))+'  N_raw: '+str(self.SHists[i].GetEntries()))
        binI=self.SHists[i].GetMaximumBin()
        if(self.SHists[i].GetBinContent(binI)==0):
            x=0
        else:
            # x=self.SHists[i].GetSumOfWeights()
            x=self.SHists[i].GetStdDevError()
            # x=self.SHists[i].GetBinError(binI)/self.SHists[i].GetBinContent(binI)
        
        chi2s=(RooFitHist(self.SHists[i],"%s_%s_%s"%(self.channel,self.OpName,self.getPointName(i)),path),x)

        print('=========================================')
        print(self.channel,self.OpName)
        return chi2s
        # for chi2 in chi2s:
        #     print(chi2)
        # ri=raw_input("Press Enter to continue")
        
    def exportPlot(self,logY=True,path="./output/pT_plots",rebin=True):

        plottitle="transverse momentum of AK%i Jets (%s-Operator) in %s - %s"%(self.jetRadius,self.OpName,self.channel,self.LastCut)
        canv = TCanvas(plottitle,plottitle,600,600)
        
        #turning off the standard Statistic-Box
        gStyle.SetOptStat(0)
        gStyle.SetOptStat(0)

        legend = TLegend(0.5,0.7,0.9,0.9)
        
        drawOptions="Hist"
        if(logY):
            canv.SetLogy()
            
        stack=THStack(plottitle,plottitle)
            
        if(rebin):
            BGHist=self.BHist.Rebin(len(self.dijetbinning)-1,"new binning",self.dijetbinning)
        else:
            BGHist=self.BHist

        #Cosmetics:
        BGHist.SetFillColor(867)
        BGHist.SetLineColor(867)
        
        BGHist.SetTitle(plottitle)
        BGHist.GetXaxis().SetTitle('pT_{leading-AK8} [GeV/c^{2}]')
        BGHist.GetYaxis().SetTitle('Events')
        BGHist.GetXaxis().SetRangeUser(0,9000)
        BGHist.GetYaxis().SetRangeUser(10**(-5),10**2)
        BGHist.GetYaxis().SetTitleOffset(1.3)

        legend.AddEntry(BGHist,"QCD","f")

        BGHistErr=BGHist.Clone()
        BGHistErr.SetFillColor(rt.kGray+2)
        BGHistErr.SetFillStyle(3204)
        BGHistErr.Draw('E2')
        BGHist.Draw("SAME"+drawOptions)
        BGHistErr.Draw('E2SAME')

        stack=THStack('stack',plottitle)
        # stack.Add(BGHist)
        
        histcounter=1
        
        #number of Parameters to plot:        
        n=6
        med=(sets[self.OpName][0]-1)/2 -1

        for i in range(n):
            index= i * med/n
            if(rebin):
                hist=self.SHists[index].Rebin(len(self.dijetbinning)-1,"new binning",self.dijetbinning)
            else:
                hist=self.SHists[index]
            # hist.Add(BGHist)    
            hist.SetLineColor(histcounter)
            hist.SetMarkerStyle(8)
            hist.SetMarkerSize(0.6)
            hist.SetMarkerColor(histcounter)
            # hist.Draw("SAME"+drawOptions)
            stack.Add(hist)
            legend.AddEntry(hist,"%sjj (%s=%.1fTeV^{-4})"%(self.channel,self.OpName,self.getPoint(index)))#maybe to -6?
            histcounter+=1
        canv.SetTitle(plottitle)
        # stack.Draw('nostack'+drawOptions)
        # stack.GetXaxis().SetRangeUser(0,9000)
        # stack.Draw('nostack'+drawOptions)
        # stack.Draw('nostackep'+SAME)
        # stack.GetXaxis().SetRangeUser(0,9000)
        stack.Draw('nostackep'+'SAME')
        
        legend.Draw()
        gPad.RedrawAxis()
        canv.Update()
        canv.Print("%s/%s_AK%i_%s.eps"%(path,self.channel,self.jetRadius,self.OpName))
        del stack

    def testSensitivity(self,plot=False,path="./output/pT_plots"):
        if(self.jetRadius!=8):
            print('to calculate estimates of Limits use AK8 Jets!')
            return -1

        Nbins = self.BHist.GetNbinsX()
        bin=0
        BSum=0
        SSums=[]
        for hist in self.SHists:
            SSums.append(0)
        for i in list(reversed(range(Nbins))):
            if(BSum>=10):
                break
            # if(i==8183):
            #     continue
            BSum+=self.BHist.GetBinContent(i)
            
            for j in range(0,len(self.SHists)):
                SSums[j]+=self.SHists[j].GetBinContent(i)
            bin=i
        print('BSum=',BSum,' -> bin:',bin,';BinCenter:',self.BHist.GetBinCenter(bin))

        lower_limit_index= -1
        upper_limit_index= -1

        expectedLimit_S=7.5312
        # if(self.LastCut=='detaAk4sel'):
        #     expectedLimit_S=7.5938 #for B=10.1607131213
        # elif(self.LastCut=='invMAk4sel_1p5_allcuts'):
        #     expectedLimit_S=7.7188 #for B=10.6225637197
        # elif(self.LastCut=='invMAk4sel_2p0_allcuts'):
        #     expectedLimit_S=7.5312 #for B=10.0067629367
        # else:
        #     expectedLimit_S=1000 


        for i in range(0,len(SSums)):           
            print(self.getPoint(i),'-',SSums[i])
            if(lower_limit_index==-1):
                if( SSums[i]<=expectedLimit_S):
                    lower_limit_index=i
            elif(upper_limit_index==-1):
                if( SSums[i]>=expectedLimit_S):
                    upper_limit_index=i-1

        self.limitCalc_succeeded=(lower_limit_index!=-1 and upper_limit_index!=-1)
        
        lower_limit=approxLimit(expectedLimit_S,self.getPoint(lower_limit_index-1),SSums[lower_limit_index-1],self.getPoint(lower_limit_index),SSums[lower_limit_index])
        upper_limit=approxLimit(expectedLimit_S,self.getPoint(upper_limit_index),SSums[upper_limit_index],self.getPoint(upper_limit_index+1),SSums[upper_limit_index+1])

        self.Limits=(lower_limit,upper_limit)


        #Plot SSums and 'calculated limits'
        plot1=TCanvas('parameterIntegral','EventYields for Parameter %s (%s)'%(self.OpName,self.channel),600,600)
        plot1.SetLogy()
        limit_legend = TLegend(0.6,0.12,0.9,0.3)

        x, y = array( 'd' ), array( 'd' )
        for i in range(0,len(SSums)):
            x.append(self.getPoint(i))
            y.append(SSums[i])
        graph=TGraph(len(SSums),x,y)
        graph.SetLineColor( 2 )
        graph.SetLineWidth( 2 )
        graph.SetMarkerColor( 1 )
        graph.SetMarkerStyle( 3 )
        graph.SetTitle('EventYields for Parameter F_{%s}'%self.OpName)
        graph.GetXaxis().SetTitle('F_{%s}/#Lambda^{4} [TeV^{-4}]'%self.OpName)
        graph.GetYaxis().SetTitle('S')
        graph.Draw( 'AP' )
        limit_legend.AddEntry(graph,"S (for B=%.2f)"%BSum,'p')


        #plot Line at expectedLimit_S for the given B
        slimit=TGraph()
        slimit.SetPoint(0,self.getPoint(0),expectedLimit_S)
        slimit.SetPoint(1,self.getPoint(sets[self.OpName][0]-1),expectedLimit_S)
        slimit.SetLineWidth(2)
        slimit.SetLineStyle(2)
        slimit.Draw("LSAME")
        
        if(self.limitCalc_succeeded):
            #plot the first points where S<...
            llimit=TGraph()
            llimit.SetPoint(0,self.getPoint(lower_limit_index),0)
            llimit.SetPoint(1,self.getPoint(lower_limit_index),100)
            llimit.SetLineWidth(2)
            llimit.SetLineStyle(2)
            llimit.Draw("LSAME")

            ulimit=TGraph()
            ulimit.SetPoint(0,self.getPoint(upper_limit_index),0)
            ulimit.SetPoint(1,self.getPoint(upper_limit_index),100)
            ulimit.SetLineWidth(2)
            ulimit.SetLineStyle(2)
            ulimit.Draw("LSAME")
        
            limit_legend.AddEntry(ulimit,'first points where S<%.2f'%expectedLimit_S,'l')

            #plot the interpolated Limits
            llimit_interpolated=TGraph()
            llimit_interpolated.SetPoint(0,self.Limits[0],0)
            llimit_interpolated.SetPoint(1,self.Limits[0],100)
            llimit_interpolated.SetLineWidth(2)
            llimit_interpolated.SetLineStyle(2)
            llimit_interpolated.SetLineColor(4)
            llimit_interpolated.Draw("LSAME")

            ulimit_interpolated=TGraph()
            ulimit_interpolated.SetPoint(0,self.Limits[1],0)
            ulimit_interpolated.SetPoint(1,self.Limits[1],100)
            ulimit_interpolated.SetLineWidth(2)
            ulimit_interpolated.SetLineStyle(2)
            ulimit_interpolated.SetLineColor(4)
            ulimit_interpolated.Draw("LSAME")

            limit_legend.AddEntry(ulimit_interpolated,'interpolated limits','l')


        #Plot the best Limits from CMS/ATLAS
        llimit_best=TGraph()
        ulimit_best=TGraph()
        with open('best_limits_ssWW.csv','rb') as limitcsv:
            limitreader=csv.DictReader(limitcsv)
            for row in limitreader:
                if(row['parameter']==self.OpName):
                    llimit_best.SetPoint(0,float(row['mob']),0)
                    llimit_best.SetPoint(1,float(row['mob']),100)
                    ulimit_best.SetPoint(0,float(row['pob']),0)
                    ulimit_best.SetPoint(1,float(row['pob']),100)
        llimit_best.SetLineWidth(2)
        llimit_best.SetLineStyle(2)
        llimit_best.SetLineColor(2)
        llimit_best.Draw("LSAME")
        ulimit_best.SetLineWidth(2)
        ulimit_best.SetLineStyle(2)
        ulimit_best.SetLineColor(2)
        ulimit_best.Draw("LSAME")
        
        limit_legend.AddEntry(ulimit_best,'ssWW Limits (SMP-17-004)','l')
        
        limit_legend.Draw()

        plot1.Update()
        plot1.GetFrame().SetBorderSize( 12 )
        plot1.Modified()
        plot1.Update()        
        if(plot):
            plot1.Print('%s/SPlot_%s_%s_%s.eps'%(path,self.channel,self.OpName,self.LastCut))
        

    def getPoint(self,i):
        return sets[self.OpName][1]+i*sets[self.OpName][2]
        
    def getPointName(self,i):
        name="pT_AK8_12_%s_"%self.OpName

        parameter=100*sets[self.OpName][1]+i*100*sets[self.OpName][2]
        if(parameter>=0):
            name+="%ip%02i"%(parameter/100,parameter%100)
        else:
            name+="m%ip%02i"%(-parameter/100,-parameter%100)
        return name

    def getFileName(self,i):
        name="%s_%s_"%(self.channel,self.OpName)

        parameter=100*sets[self.OpName][1]+i*100*sets[self.OpName][2]
        if(parameter>=0):
            name+="%ip%02i"%(parameter/100,parameter%100)
        else:
            name+="m%ip%02i"%(-parameter/100,-parameter%100)
        return name
        
def approxLimit(S,X1,Y1,X2,Y2):
    m=(Y2-Y1)/(X2-X1)
    if(m==0):
        return 0
    b=(Y1*X2-Y2*X1)/(X2-X1)
    return (S-b)/m

def getParName(OpName,startx, increment, i):
    name="pT_AK8_12_%s_"%OpName
    parameter=100*startx+i*100*increment
    if(parameter>=0):
        name+="%ip%02i"%(parameter/100,parameter%100)
    else:
        name+="m%ip%02i"%(-parameter/100,-parameter%100)
    return name

def fillHistNames(HistNames,OpName):
    for i in range(sets[OpName][0]):
        HistNames.append(getParName(OpName,sets[OpName][1],sets[OpName][2],i))


def update_progress(iteration,complete):
    barLength = 30
    status = ""
    progress=float(iteration)/float(complete)
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rFiles processed: %i/%i [%s] %s"%(int(iteration),int(complete),"#"*block+"-"*(barLength-block),status) 
    sys.stdout.write(text)
    sys.stdout.flush()

