import ParSet


if(__name__=="__main__"):
    path='/nfs/dust/cms/user/loemkerj/bachelor/CMSSW_10_2_16/src/UHH2/aQGCVVjjhadronic/SignalRegion'
    
    dim8op=["S0","S1","S2","M0","M1","M2","M3","M4","M5","M7","T0","T1","T2","T5","T6","T7","T8","T9"]
    
    region='SignalRegion'
    channels=['ZZ']
    cuts=['VVRegion','invMAk4sel_1p0'] # second cut is treated as VBF cut
    for channel in channels:
        for cut in cuts:
            for op in dim8op:                
                print('+++++++++++writing RootFiles - %s - %s+++++++++++'%(op,cut))
                current_Set=ParSet.Set(op,channel,cut,region)
                current_Set.CombinedRootFiles(path, cuts[1])
