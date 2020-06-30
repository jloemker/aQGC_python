from array import array
import os, sys, csv, collections, numpy, math, gc
from ROOT import gROOT, gSystem, gStyle, gPad, TCanvas, TColor, TF1, TFile, TLegend, THStack, TGraph, TMath, kTRUE, kFALSE,TLatex, TPad, TLine
import ROOT as rt

def magnitude(x):
    return int(math.floor(math.log10(x)))

gROOT.SetBatch(True)
gStyle.SetOptStat(0)
gStyle.SetOptFit(0)
gStyle.SetOptTitle(0)

gStyle.SetTextFont(43)

gStyle.SetTitleOffset(0.86,"X")
gStyle.SetTitleOffset(1.6,"Y")
# gStyle.SetPadLeftMargin(0.18)
gStyle.SetPadLeftMargin(0.1)
# gStyle.SetPadBottomMargin(0.15)
gStyle.SetPadBottomMargin(0.12)
gStyle.SetPadTopMargin(0.08)
# gStyle.SetPadRightMargin(0.08)
gStyle.SetPadRightMargin(0.1)
gStyle.SetMarkerSize(0.5)
gStyle.SetHistLineWidth(1)
gStyle.SetTitleSize(0.05, "XYZ")
gStyle.SetLabelSize(0.04, "XYZ")
gStyle.SetNdivisions(506, "XYZ")
gStyle.SetLegendBorderSize(0)


def plotter(plotdir,plot,xTitle,logY,channels=['VV'],includeData=False,scaleSignal=0,UserRange=[None,None,None,None],initPath=''):

   # channelTex={'WPWP':'W^{+}W^{+}', 'WPWM':'W^{+}W^{-}','WMWM':'W^{-}W^{-}','WPZ':'W^{+}Z','WMZ':'W^{-}Z','ZZ':'ZZ'}
    channelTex={'ZZ':'ZZ'}
   # plotstyle=[(1,1),(1,2),(2,1),(2,2),(4,1),(4,2)]
    plotstyle=[(1,1)]
    #             0              1                       2                        3             4              5             6
   # Backgrounds=['QCD',     'WJetsToQQ_HT600ToInf', 'ZJetsToQQ_HT600ToInf',     'TT',         'WW',          'WZ',         'ZZ']
   # BGColors=   [rt.kAzure+7,   rt.kRed-4,              rt.kOrange-2,            rt.kGreen+2,  rt.kOrange+7,  rt.kBlue+1,   rt.kMagenta+2]
   # BGTeX=      ['QCD',        'W+JetsToQQ',           'Z+JetsToQQ',             'TTbar'],      'WW',          'WZ',         'ZZ']
    #stackOrder= [4,5,6,2,1,3,0]
    Backgrounds=['QCD']# 'WJetsToQQ_HT600ToInf', 'ZJetsToQQ_HT600ToInf', 'ZZ']  'TT',         'WW',          'WZ',         'ZZ']
    BGColors=   [rt.kAzure+7]#,              rt.kOrange-2,            rt.kGreen+2],  rt.kOrange+7,  rt.kBlue+1,   rt.kMagenta+2]
    BGTeX=      ['QCD']#

    stackOrder=[0]

    PreSelection=['nocuts',
                  'common',
                  'corrections',
                  'cleaner',
                  'softdropmassCorr',
                  'AK4pfidfilter',
                  'AK8pfidfilter',
                  'invMAk8sel',
                  'detaAk8sel',
                  'AK8N2sel'
    ]
    Selection=['preselection',
               'softdropAK8sel',
               'tau21sel',
               'deltaR48',
               'VVRegion',
               'AK4N2sel',
               'OpSignsel',
               'detaAk4sel',
               'invMAk4sel_1p0'
    ]

    cutnames=['cleaner','AK8N2sel','invMAk8sel','detaAk8sel','softdropAK8sel','tau21sel','AK4cleaner','AK4N2sel','OpSignsel','detaAk4sel','invMAk4sel_1p0']

    cuts={'cleaner':'#splitline{p_{T-AK8} > 200 GeV, |#eta_{AK8}| < 2.5}{p_{T-AK4} > 30 GeV, |#eta_{AK4}| < 5.0}',
          'AK8N2sel':'N_{AK8} #geq 2',
          'invMAk8sel':'M_{jj-AK8} > 1050 GeV',
          'detaAk8sel':'|#Delta#eta_{jj-AK8}|<1.3',
          'softdropAK8sel':'65 GeV <M_{SD}< 105 GeV',
          'tau21sel':'0 #leq #tau_{2}/#tau_{1}<0.45',
          # 'AK4cleaner':'p_{T-AK4} > 30 GeV, |#eta_{AK4}| < 5.0',
          'AK4cleaner':'',
          'AK4N2sel':'N_{AK4} #geq 2',
          'OpSignsel':'#eta_{1-AK4} #eta_{2-AK4} < 0',
          'detaAk4sel':'|#Delta#eta_{jj-AK4}| > 3.0',
          'invMAk4sel_1p0':'M_{jj-AK4} > 1.0 TeV'}
    
    VV=('VV' in channels)
    seperate=(not VV)
    if VV:
        #channels=["WPWP","WPWM","WMWM","WPZ","WMZ","ZZ"]
        channels=["ZZ"]

    plottitle=plotdir+'_'+plot

    lumi=36.814
    xLabelSize=18.
    yLabelSize=18.
    xTitleSize=20.
    yTitleSize=22.
    xTitleOffset=4.
    yTitleOffset=1.3

    printout=False
    Portrait=True
    cutname=False        
    ratio=includeData

    if('highbin' in plot):
        binning='dijetbinning'
    else:
        binning='default'

    if(Portrait):
        canvX=600
        canvY=600
    else:
        canvX=900
        canvY=675


    if(plotdir in PreSelection):
        region='PreSelection'
        initPath=''
        referenceHistPath = 'detaAk8sel/N_pv'
        if(PreSelection.index(plotdir)<4 and ('softdrop' in plot)):
            return 'SofdropMass not filled yet!'
    else:
        region='SignalRegion'
        referenceHistPath = 'tau21sel/N_pv'
    referenceHistPath=plotdir+'/'+plot

    if(initPath==''):
        path='/nfs/dust/cms/user/loemkerj/bachelor/CMSSW_10_2_16/src/UHH2/aQGCVVjjhadronic/%s'%region
    else:
        path=initPath
    outputPath=path.replace('/nfs/dust/cms/user/loemkerj/bachelor/CMSSW_10_2_16/src/UHH2/aQGCVVjjhadronic/SignalRegion','plots/')
    if(plotdir in PreSelection):
        CutNumber=PreSelection.index(plotdir)
    else:
        CutNumber=Selection.index(plotdir)
    outputPath=outputPath+'/%02i_%s'%(CutNumber,plotdir)+'/'
    if(printout):
        print('InputPath:',path)
        print('OutputPath:',outputPath)
    #check if OutputPath exists - and if not create it!
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
    # path='/home/albrec/Master/signal/'
    scaleVV=(scaleSignal!=0)
    VVScale=scaleSignal

    if(UserRange[2] == None or UserRange[3]== None):
        YRangeUser=False
        Ymin=UserRange[2]
        Ymax=UserRange[3]
    else:
        YRangeUser=True
        Ymin=UserRange[2]
        Ymax=UserRange[3]

    if(UserRange[0] == None or UserRange[1] == None):
        XRangeUser=False
        Xmin=UserRange[0]
        Xmax=UserRange[1]
    else:
        XRangeUser=True
        Xmin=UserRange[0]
        Xmax=UserRange[1]

    # YRangeUser=False
    # Ymin=0.11
    # Ymax=9*10**3

    # XRangeUser=False
    # Xmin=0
    # Xmax=6000.

    gROOT.ProcessLine( "gErrorIgnoreLevel = 2001;")
    SFiles=[]
    for i in range(len(channels)):
        SFiles.append(TFile(path+"/uhh2.AnalysisModuleRunner.MC.MC_aQGC_%sjj_hadronic_2016v3.root"%channels[i]))
 #uhh2.AnalysisModuleRunner.MC.MC_aQGC_ZZjj_hadronic_2016v3.root
    ##Open Files to get BackgroundHist:
    BFiles=[]
    for i in range(len(Backgrounds)):
        BFiles.append(TFile(path+"/uhh2.AnalysisModuleRunner.MC.MC_%s.root"%Backgrounds[i]))

    #Open File to get DataHist:
   # DataFile = TFile(path+"/uhh2.AnalysisModuleRunner.Data.DATA.root")

    # gROOT.ProcessLine( "gErrorIgnoreLevel = 0;")


    if(includeData):
        #calculate QCDscale with Integrals from the following Histogram:
        # referenceHistPath = 'tau21sel/N_AK4'
        # referenceHistPath = 'detaAk8sel/N_pv'
        # referenceHistPath = 'tau21sel/met_pt_over_sumptAK8_2'
        QCDscale = float(DataFile.Get(referenceHistPath).Integral())
        QCDNorm=1
        for i in range(len(BFiles)):
            if('QCD' in BFiles[i].GetName()):
                QCDNorm=float(BFiles[i].Get(referenceHistPath).Integral())
            else:
                QCDscale-=float(BFiles[i].Get(referenceHistPath).Integral())
        QCDscale/=QCDNorm
    else:
        QCDscale = 1.0
    if(printout):
        print('using QCDscale:',QCDscale)

    SHists=[]
    for i in range(len(channels)):
        SHists.append(SFiles[i].Get(plotdir+'/'+plot))

    BHists=[]
    for i in range(len(BFiles)):
        BHists.append(BFiles[i].Get(plotdir+'/'+plot))
        if('QCD' in BFiles[i].GetName()):
            BHists[-1].Scale(QCDscale)

    if(includeData):
        DataHist=DataFile.Get(plotdir+'/'+plot)
    
    if(binning=='dijetbinning'):
        fitbinning=array('d')
        binwidth=200
        NBins=(14000/binwidth) - ( (1040/binwidth)+1 )
        NBins=int(NBins)
        for i in range(NBins+1):
            fitbinning.append(1050+i*binwidth)
            
        for i in range(len(channels)):
            SHists[i]=SHists[i].Rebin(NBins,"new binning",fitbinning)
        for i in range(len(Backgrounds)):
            BHists[i]=BHists[i].Rebin(NBins,"new binning",fitbinning)

        if(includeData):
            DataHist=DataHist.Rebin(NBins,"new binning",fitbinning)

        
    canv = TCanvas(plottitle,plottitle,canvX,canvY)

    yplot=0.7
    yratio=0.3
    ymax=1.0
    xmax=1.0
    xmin=0.0
    if(ratio):
        plotpad=TPad("plotpad","Plot",xmin,ymax-yplot,xmax,ymax)
        ratiopad=TPad("ratiopad","Ratio",xmin,ymax-yplot-yratio,xmax,ymax-yplot)
    else:
        plotpad=TPad("plotpad","Plot",xmin,ymax-yplot-yratio,xmax,ymax)

    plotpad.SetTopMargin(0.08)
    plotpad.SetLeftMargin(0.1)
    plotpad.SetRightMargin(0.05)
    plotpad.SetTicks()
    plotpad.Draw()

    if(ratio):
        plotpad.SetBottomMargin(0.016)
        ratiopad.SetTopMargin(0.016)
        ratiopad.SetBottomMargin(0.35)
        ratiopad.SetLeftMargin(0.1)
        ratiopad.SetRightMargin(0.05)
        ratiopad.SetTicks()
        ratiopad.Draw()
    else:
        plotpad.SetBottomMargin(0.1)
        
    if(logY):
        plotpad.SetLogy()
        canv.SetLogy()
    if('-logX' in xTitle):
        plotpad.SetLogx()
        if(ratio):
            ratiopad.SetLogx()
        canv.SetLogx()
        
    drawOptions="HE"

    stack=THStack(plottitle,plottitle)

    BHist=THStack(plottitle,plottitle)


    # for i in range(len(Backgrounds)):
    for i in stackOrder:
       # BHists[i].SetFillColor(BGColors[i])
        BHists[i].SetLineColor(BGColors[i])
        BHist.Add(BHists[i],'Hist')

    BHist.SetTitle(plottitle)

    BHistErr=BHists[0].Clone()
    for i in range(1,len(Backgrounds)):
        BHistErr.Add(BHists[i])

    BHistErr.SetFillStyle(3204)
    BHistErr.SetFillColor(rt.kGray+2)
    BHistErr.SetLineColor(1)

    BGMax=BHist.GetMaximum()
    SIGMax=0
    #if(VV):       #new
    #    SIGMax=VVsum.GetMaximum()
    #else:
    for i in range(len(channels)):
        tmpmax=SHists[i].GetMaximum()
        if(tmpmax>SIGMax):
            SIGMax=tmpmax
    if(scaleVV):
        SIGMax=SIGMax*VVScale        
    if(logY):
        MAX=0.9*float(10**(magnitude(max(BGMax,SIGMax))+1))
        MIN=float(10**(magnitude(max(BGMax,SIGMax))-5))
        MIN+=float(10**(magnitude(MIN)))
        legendMIN=math.log(max(BGMax,SIGMax))/math.log(MAX)
    else:
        MAX=(1.0/0.8)*max(BGMax,SIGMax)
        legendMIN=0.7
        MIN=0.
    legendMIN=(legendMIN*0.7)+0.3-0.016

    legend = TLegend(0.5,0.75,0.85,0.89)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.02)
    legend.SetMargin(0.4)
    legend.SetNColumns(2)
    legend.SetColumnSeparation(0.3)

    if(includeData):
        DataHist.SetMarkerStyle(8)
        DataHist.SetLineColor(1)
        DataHist.SetTitle(plottitle)

    if VV:
        for i in range(len(channels)):
            if(i==0):
                VVsum=SHists[i].Clone()
            else:
                VVsum.Add(SHists[i])
        legentry='VVjj'
        if(scaleVV):
            VVsum.Scale(VVScale)
            legentry+=' *%0.f'%VVScale
        VVsum.SetLineColor(1)
        VVsum.SetLineStyle(plotstyle[0][1])
        VVsum.SetLineWidth(2)
        legend.AddEntry(VVsum,legentry)
    else:
        for i in range(len(channels)):
            SHists[i].SetLineColor(plotstyle[i][0])
            SHists[i].SetLineStyle(plotstyle[i][1])
            SHists[i].SetLineWidth(2)
            legentry="%sjj"%channelTex[channels[i]]
            if(scaleVV):
                SHists[i].Scale(VVScale)
                legentry+=' *%.2E'%VVScale
            legend.AddEntry(SHists[i],legentry)

    for i in stackOrder:
        legend.AddEntry(BHists[i],BGTeX[i],"f")
    legend.AddEntry(BHistErr,"stat. Uncertainty","f")

    if(includeData):
        legend.AddEntry(DataHist,"Data","lep")

    canv.SetTitle(plottitle)


    BHistErr.GetYaxis().SetTitle('Events')
    BHistErr.GetYaxis().SetRangeUser(MIN,MAX)
    BHistErr.GetYaxis().SetTitleFont(43)
    BHistErr.GetYaxis().SetTitleSize(yTitleSize)
    BHistErr.GetYaxis().SetTitleOffset(yTitleOffset)
    BHistErr.GetYaxis().SetLabelFont(43)
    BHistErr.GetYaxis().SetLabelSize(yLabelSize)
    if(ratio):
        BHistErr.GetXaxis().SetTitleSize(0.0)
        BHistErr.GetXaxis().SetLabelSize(0.0)
    else:
        BHistErr.GetXaxis().SetTitle(xTitle)
        BHistErr.GetXaxis().SetTitleFont(43)
        BHistErr.GetXaxis().SetTitleSize(xTitleSize)
        # BHistErr.GetXaxis().SetTitleOffset(xTitleOffset)
        BHistErr.GetXaxis().SetTitleOffset(1.2)
        BHistErr.GetXaxis().SetLabelFont(43)
        BHistErr.GetXaxis().SetLabelSize(xLabelSize)
        # BHistErr.GetXaxis().SetTickLength(0.08)
        # BHistErr.GetXaxis().SetNdivisions(506)

    if(YRangeUser):
        BHistErr.GetYaxis().SetRangeUser(Ymin,Ymax)
    if(XRangeUser):
        BHistErr.GetXaxis().SetRangeUser(Xmin,Xmax)

    plotpad.cd()

    BHistErr.Draw("E2")
    BHist.Draw("HistSAME")
    BHistErr.Draw("E2SAME")

    if(VV):
        VVsum.Draw("SAME"+drawOptions)
    elif('-noSig' not in xTitle):
        for i in range(len(channels)):
            SHists[i].Draw("SAME"+drawOptions)

    if(includeData):
        DataHist.Draw("APE1SAME")

    plotpad.RedrawAxis()
    if(ratio):
        ratiopad.cd()

        if(includeData):
            ratioHist=DataHist.Clone()
        else:
            ratioHist=BHistErr.Clone()
        ratioHist.SetLineColor(rt.kBlack)
        # ratioHist.Sumw2()
        ratioHist.SetStats(0)
        ratioHist.Divide(BHistErr)
        ratioHist.SetMarkerStyle(21)
        ratioHist.SetMarkerSize(0.7)

        #Yaxis
        ratioHist.GetYaxis().SetRangeUser(0.3,1.7)
        ratioHist.GetYaxis().SetTitle("Data/BG")
        ratioHist.GetYaxis().CenterTitle()
        ratioHist.GetYaxis().SetTitleFont(43)
        ratioHist.GetYaxis().SetTitleSize(yTitleSize)
        ratioHist.GetYaxis().SetTitleOffset(yTitleOffset)
        ratioHist.GetYaxis().SetLabelFont(43)
        ratioHist.GetYaxis().SetLabelSize(yLabelSize)
        ratioHist.GetYaxis().SetNdivisions(506)
        #Xaxis
        ratioHist.GetXaxis().SetTitle(xTitle)
        ratioHist.GetXaxis().SetTitleFont(43)
        ratioHist.GetXaxis().SetTitleSize(xTitleSize)
        ratioHist.GetXaxis().SetTitleOffset(xTitleOffset)
        ratioHist.GetXaxis().SetLabelFont(43)
        ratioHist.GetXaxis().SetLabelSize(xLabelSize)
        ratioHist.GetXaxis().SetTickLength(0.08)
        ratioHist.GetXaxis().SetNdivisions(506)

        # if(YRangeUser):
        #     ratioHist.GetYaxis().SetRangeUser(Ymin,Ymax)
        if(XRangeUser):
            ratioHist.GetXaxis().SetRangeUser(Xmin,Xmax)
            ratioXMin=Xmin
            ratioXMax=Xmax
        else:
            ratioXMin=ratioHist.GetXaxis().GetXmin()
            ratioXMax=ratioHist.GetXaxis().GetXmax()
        ratioHist.Draw("ep")



        zeropercent=TLine(ratioXMin,1,ratioXMax,1)
        zeropercent.Draw()
        plus10percent=TLine(ratioXMin,1.1,ratioXMax,1.1)
        plus10percent.SetLineStyle(rt.kDashed)
        plus10percent.Draw()
        minus10percent=TLine(ratioXMin,0.9,ratioXMax,0.9)
        minus10percent.SetLineStyle(rt.kDashed)
        minus10percent.Draw()

    canv.cd()
    gPad.RedrawAxis()
    legend.Draw()

    latex=TLatex()
    latex.SetNDC(kTRUE)
    latex.SetTextSize(20)
    latex.DrawLatex(0.69,0.953,"%.2f fb^{-1} (13 TeV)"%lumi)
    latex.DrawLatex(0.1,0.953,"private work")

    lastcut='nocuts'
    for cut in cutnames:
        if cut in plotdir:
            lastcut=cut

    if(not (lastcut=='nocuts') and cutname):
        # latex.SetTextSize(0.03)
        latex.SetTextSize(15)
        for l in range(cutnames.index(lastcut)+1):
            latex.DrawLatex(0.12,0.8-l*0.04,cuts[cutnames[l]])

    canv.Update()
    canv.Print(outputPath+'/%s_%s.pdf'%(plotdir,plot))
    #prevents memory leak in Canvas Creation/Deletion
    #see: https://root.cern.ch/root/roottalk/roottalk04/2484.html
    gSystem.ProcessEvents()
    if(ratio):
        del ratiopad
    del plotpad,canv
    # gc.collect()
    return 'done!'
if(__name__=='__main__'):
    plotdir='invMAk4sel_1p0'
    plot='M_jj_AK8'
    xTitle='Mjj [GeV]'
    logY=True
    plotter('invMAk4sel_1p0', 'M_jj_AK8', 'Mjj [GeV]', True)
#this works! Nice -> results in /plot directory :) ggf. lables checken wegen CR..aber kommt der glaube ich ganz gut nahe