from plotter import plotter


if(__name__=='__main__'):

    #plotdir= nocuts,cleaner,AK8N2sel,deltaR48,invMAk8sel,detaAk8sel,softdropAK8sel,tau21sel,VVRegion,AK4N2sel,OpSignsel,detaAk4sel,invMAk4sel_1p0
    #histname= N_pv,pdgID,N_AK*,eta/pT_AK*,eta/pT_AK*_{1,2,12},prodeta_AK4_12,M_jj_AK*,M_jj_AK*_highbin,M_softdrop_{1,2,12},tau_21_{1,2,12},met_over_pt_mjjAK8_{2,4},met_over_sumptAK*_{2,4},met_over_sumptJets_{2,4}
    # *new* : deta_AK*_12,M_AK8{_{1,2,12}}
    
    channel='ZZ'
    #plotter(plotdir,plot,xTitle,logY,channels=['VV'],includeData=False,scaleSignal=0)
    includeData=False
    plots=[         
        ('N_AK4','N_{AK4}',True,[channel],includeData,0.01),
        ('eta_AK4_12','#eta^{two leading AK4}',False,[channel],includeData,0.01),
        ('eta_AK4_1','#eta^{1st AK4}',False,[channel],includeData,0.01),
        ('eta_AK4_2','#eta^{2nd AK4}',False,[channel],includeData,0.01),
        ('eta_AK4','#eta^{AK4}',True,[channel],includeData,0),
        ('deta_AK4_12','#Delta#eta^{two leading AK4}',True,[channel],includeData,0),
        ('pT_AK4_12','p_{T}^{two leading AK4}',True,[channel],includeData,0.01),
        ('pT_AK4_1','p_{T}^{1st AK4}',True,[channel],includeData,0.01),
        ('pT_AK4_2','p_{T}^{2nd AK4}',True,[channel],includeData,0.01),
        ('pT_AK4','p_{T}^{AK4}',True,[channel],includeData,0),
        
        ('N_AK8','N_{AK8}',True,[channel],includeData,0.01),
        ('eta_AK8_12','#eta^{two leading AK8}',False,[channel],includeData,0.01),
        ('eta_AK8_1','#eta^{1st AK8}',False,[channel],includeData,0.01),
        ('eta_AK8_2','#eta^{2nd AK8}',False,[channel],includeData,0.01),
        ('eta_AK8','#eta^{AK8}',True,[channel],includeData,0),
        ('deta_AK8_12','#Delta#eta^{two leading AK8}',True,[channel],includeData,0),
        ('pT_AK8_12','p_{T}^{two leading AK8}',True,[channel],includeData,0.01),
        ('pT_AK8_1','p_{T}^{1st AK8}',True,[channel],includeData,0.01),
        ('pT_AK8_2','p_{T}^{2nd AK8}',True,[channel],includeData,0.01),
        ('pT_AK8','p_{T}^{AK8}',True,[channel],includeData,0),
        ('M_AK8_12','M_{two leading AK8}',True,[channel],includeData,0.01),
        ('M_AK8_1','M_{1st AK8}',True,[channel],includeData,0.01),
        ('M_AK8_2','M_{2nd AK8}',True,[channel],includeData,0.01),
        ('M_AK8','M_{AK8}',True,[channel],includeData,0),

        ('M_jj_AK8','M_{jj-AK8}',True,[channel],includeData,0),
        ('M_jj_AK4','M_{jj-AK4}',True,[channel],includeData,0),
        ('M_softdrop_1','M_{SD 1st AK8}',True,[channel],includeData,0),
        ('M_softdrop_2','M_{SD 2nd AK8}',True,[channel],includeData,0),
        ('M_softdrop_12','M_{SD leading AK8}',True,[channel],includeData,0),
        ('tau21_1','#tau_{2}/#tau_{1} _{1st AK8}',True,[channel],includeData,0),
        ('tau21_2','#tau_{2}/#tau_{1} _{2nd AK8}',True,[channel],includeData,0),
        ('tau21_12','#tau_{2}/#tau_{1} _{two leading AK8}',True,[channel],includeData,0),
        ('met_pt_over_mjjAK8_2','MET/M_{jj-AK8}',True,[channel],includeData,0.01),
        ('met_pt_over_sumptAK8_2','MET/#sum_{AK8} p_{T}',True,[channel],includeData,0.05),
        ('met_pt_over_sumptAK4_2','MET/#sum_{AK4} p_{T}',True,[channel],includeData,0),
        ('met_pt_over_sumptJets_2','MET/#sum_{AK4,8} p_{T}',True,[channel],includeData,0)
        ]

    # cuts = ['nocuts','common','corrections','cleaner','softdropmassCorr','AK4pfidfilter','AK8pfidfilter','AK8N2sel','invMAk8sel','detaAk8sel','preselection','softdropAK8sel','tau21sel','deltaR48','VVRegion','AK4N2sel','OpSignsel','detaAk4sel','invMAk4sel_1p0']
    cuts = ['preselection','softdropAK8sel','tau21sel','deltaR48','VVRegion','AK4N2sel','OpSignsel','detaAk4sel','invMAk4sel_1p0']
    # cuts = ['tau21sel']
    # cuts=['nocuts','cleaner','AK8N2sel']
    # RegionPaths=['SignalRegion/tau21sel_45','SignalRegion/tau21sel_35']#,'HIGHSidebandRegion','HIGHSidebandRegionRmEvent']
    # RegionPaths=['SignalRegion/tau21sel_45']#,'HIGHSidebandRegion','HIGHSidebandRegionRmEvent']
    # RegionPaths=['SignalRegion/tau21sel_45','SignalRegion/tau21sel_45/backup','SignalRegion/tau21sel_35','SignalRegion/tau21sel_35/backup']
    RegionPaths=['SignalRegion']
    # RegionPaths=['PreSelection']
    counter=0
    for Region in RegionPaths:
        for cut in cuts:
            for args in plots:
                print('---------------------------------------------------')
                args=(cut,)+args
                args=args+('/nfs/dust/cms/user/loemkerj/bachelor/CMSSW_10_2_16/src/UHH2/aQGCVVjjhadronic/'+Region,)
                print(plotter(*args))
                counter=counter+1
                print('--------------------------%03i-----------------------'%counter)
                
                
