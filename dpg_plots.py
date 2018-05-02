from plotter import plotter


if(__name__=='__main__'):
    
    #plots=[('rootdir','histname','XaxisTitle',logY),...]
    channel='VV'

    plots=[#('AK8_softdropAK8sel','tau21','#tau_{2}/#tau_{1}',True,[channel]),
           # ('detaAk8sel','M_softdrop_1','M_{SD, leading AK8} [GeV/c^{2}]',True,[channel]),
           ('nocuts','pT_AK8_1','p_{T}^{leading AK8} [GeV/c]',True,[channel],True,0),
           ('nocuts','pT_AK4_1','p_{T}^{leading AK4} [GeV/c]',True,[channel],True,0),
           ('nocuts','eta_AK8_1','#eta^{leading AK8}',False,[channel],True,0),
           ('nocuts','eta_AK4_1','#eta^{leading AK4}',False,[channel],True,0),
           ('nocuts','M_jj_AK8','M_{jj-AK8} [GeV/c^{2}]',True,[channel],True,0),
           ('nocuts','M_jj_AK4','M_{jj-AK4} [GeV/c^{2}]',True,[channel],True,0)
           ]
    for args in plots:
        plotter(*args)
