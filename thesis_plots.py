import sys
from plotter import plotter

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
    text = "\rPlots processed: %i/%i [%s] %s"%(int(iteration),int(complete),"#"*block+"-"*(barLength-block),status) 
    sys.stdout.write(text)
    sys.stdout.flush()


if(__name__=='__main__'):

    #plotdir= nocuts,cleaner,AK8N2sel,deltaR48,invMAk8sel,detaAk8sel,softdropAK8sel,tau21sel,VVRegion,AK4N2sel,OpSignsel,detaAk4sel,invMAk4sel_1p0
    #histname= N_pv,pdgID,N_AK*,eta/pT_AK*,eta/pT_AK*_{1,2,12},prodeta_AK4_12,M_jj_AK*,M_jj_AK*_highbin,M_softdrop_{1,2,12},tau_21_{1,2,12},met_over_pt_mjjAK8_{2,4},met_over_sumptAK*_{2,4},met_over_sumptJets_{2,4}
    # *new* : deta_AK*_12,M_AK8{_{1,2,12}}
    
    channel='ZZ'
    #plotter(plotdir,plot,xTitle,logY,channels=['VV'],includeData=False,scaleSignal=0,UserRange=[XMin,XMax,YMin,YMax])
    includeData=False
    defaultRange=[None,None,None,None]
    plots=[         
        ('N_pv','N_{PV}',True,[channel],includeData,0.01,defaultRange),

        ('N_AK4','N_{AK4}',True,[channel],includeData,0.01,defaultRange),
        ('eta_AK4_12','#eta^{two leading AK4}',False,[channel],includeData,0.01,defaultRange),
        ('eta_AK4_1','#eta^{1st AK4}',False,[channel],includeData,0.01,defaultRange),
        ('eta_AK4_2','#eta^{2nd AK4}',False,[channel],includeData,0.01,defaultRange),
        # ('eta_AK4','#eta^{AK4}',True,[channel],includeData,0,defaultRange),
        ('deta_AK4_12','#eta^{1st AK4} #cdot #eta^{2nd AK4}',True,[channel],includeData,0,defaultRange),
        ('prodeta_AK4_12','#Delta#eta^{two leading AK4}',True,[channel],includeData,0,defaultRange),
        ('pT_AK4_12','p_{T}^{two leading AK4}',True,[channel],includeData,0.01,defaultRange),
        ('pT_AK4_1','p_{T}^{1st AK4}',True,[channel],includeData,0.01,defaultRange),
        ('pT_AK4_2','p_{T}^{2nd AK4}',True,[channel],includeData,0.01,defaultRange),
        # ('pT_AK4','p_{T}^{AK4}',True,[channel],includeData,0,defaultRange),
        
        ('N_AK8','N_{AK8}',True,[channel],includeData,0.01,defaultRange),
        ('eta_AK8_12','#eta^{two leading AK8}',True,[channel],includeData,10,[-2.5,2.5,None,None]),
        # ('eta_AK8_12','#eta^{two leading AK8}',True,[channel],includeData,0.01,defaultRange),
        ('eta_AK8_1','#eta^{1st AK8}',True,[channel],includeData,0.01,defaultRange),
        ('eta_AK8_2','#eta^{2nd AK8}',True,[channel],includeData,0.01,defaultRange),
        # ('eta_AK8','#eta^{AK8}',True,[channel],includeData,0,defaultRange),
        ('deta_AK8_12','#Delta#eta^{two leading AK8}',True,[channel],includeData,0,defaultRange),
        ('pT_AK8_12','p_{T}^{two leading AK8}',True,[channel],includeData,10,[200,2000,None,None]),
        # ('pT_AK8_12','p_{T}^{two leading AK8}',True,[channel],includeData,0.01,defaultRange),
        ('pT_AK8_1','p_{T}^{1st AK8}',True,[channel],includeData,0.01,defaultRange),
        ('pT_AK8_2','p_{T}^{2nd AK8}',True,[channel],includeData,0.01,defaultRange),
        # ('pT_AK8','p_{T}^{AK8}',True,[channel],includeData,0,defaultRange),
        ('M_AK8_12','M_{two leading AK8}',True,[channel],includeData,0.01,defaultRange),
        ('M_AK8_1','M_{1st AK8}',True,[channel],includeData,0.01,defaultRange),
        ('M_AK8_2','M_{2nd AK8}',True,[channel],includeData,0.01,defaultRange),
        # ('M_AK8','M_{AK8}',True,[channel],includeData,0,defaultRange),

        # ('M_jj_AK8_highbin','M_{jj-AK8}',True,[channel],False,0.01,[900,4500,None,None])
        ('M_jj_AK8','M_{jj-AK8}',True,[channel],False,0.01,[900,4500,None,None]),
        # ('M_jj_AK8','M_{jj-AK8}',True,[channel],False,0.01,[900,4500,10**(-1),10**(2)]),
        # ('M_jj_AK8','M_{jj-AK8} -noSig',True,[channel],False,0,[900,3000,1.1*10**(-3),10**2]),
        ('M_jj_AK4','M_{jj-AK4}',True,[channel],includeData,0,defaultRange),
        ('M_softdrop_1','M_{SD 1st AK8}',True,[channel],includeData,0,defaultRange),
        ('M_softdrop_2','M_{SD 2nd AK8}',True,[channel],includeData,0,defaultRange),
        ('M_softdrop_12','M_{SD leading AK8}',True,[channel],includeData,0,defaultRange),
        ('tau21_1','#tau_{2}/#tau_{1} _{1st AK8}',True,[channel],includeData,0,defaultRange),
        ('tau21_2','#tau_{2}/#tau_{1} _{2nd AK8}',True,[channel],includeData,0,defaultRange),
        # ('tau21_12','#tau_{2}/#tau_{1} _{two leading AK8}',True,[channel],includeData,0,[None,None,10,10**6]),
        ('tau21_12','#tau_{2}/#tau_{1} _{two leading AK8}',True,[channel],includeData,0,defaultRange),
        # ('met_pt_over_mjjAK8_2','MET/M_{jj-AK8}',True,[channel],includeData,0.01,defaultRange),
        # ('met_pt_over_sumptAK8_2','MET/#sum_{AK8} p_{T}',True,[channel],includeData,0.05,defaultRange),
        # ('met_pt_over_sumptAK4_2','MET/#sum_{AK4} p_{T}',True,[channel],includeData,0,defaultRange),
        # ('met_pt_over_sumptJets_2','MET/#sum_{AK4,8} p_{T}',True,[channel],includeData,0,defaultRange)
        ]

    # cuts = ['nocuts','common','corrections','cleaner','softdropmassCorr','AK4pfidfilter','AK8pfidfilter','AK8N2sel','invMAk8sel','detaAk8sel','preselection','softdropAK8sel','tau21sel','deltaR48','VVRegion','AK4N2sel','OpSignsel','detaAk4sel','invMAk4sel_1p0']
    # cuts = ['detaAk8sel','invMAk4sel_1p0']
    # cuts = ['cleaner','softdropmassCorr','invMAk8sel','detaAk8sel','AK8N2sel','preselection','softdropAK8sel','tau21sel','deltaR48','VVRegion','AK4N2sel','OpSignsel','detaAk4sel','invMAk4sel_1p0']
    # cuts = ['invMAk8sel','detaAk8sel','AK8N2sel','preselection','softdropAK8sel','tau21sel','deltaR48','VVRegion','AK4N2sel','OpSignsel','detaAk4sel','invMAk4sel_1p0']
    cuts = ['invMAk8sel','detaAk8sel','AK8N2sel','softdropAK8sel','tau21sel','deltaR48','VVRegion','AK4N2sel','OpSignsel','detaAk4sel','invMAk4sel_1p0']
    # cuts = ['AK8N2sel','softdropAK8sel']
    RegionPaths=['SignalRegion']
    # RegionPaths=['SignalRegion']
    # RegionPaths=['PreSelection']
    NPlots=len(plots)*len(cuts)*len(RegionPaths)
    counter=1
    for Region in RegionPaths:
        for cut in cuts:
            for args in plots:
                # print('---------------------------------------------------')
                args=(cut,)+args
                args=args+('/nfs/dust/cms/user/loemkerj/bachelor/CMSSW_10_2_16/src/UHH2/aQGCVVjjhadronic/'+Region,)
                plotter(*args)
                update_progress(counter,NPlots)
                counter=counter+1
                # print('--------------------------%03i-----------------------'%counter)
                
                
