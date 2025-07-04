from mwscript_parser import parser
from cfg_builder import build_cfg
from analysis_pass import evaluate_cfg_cost
from tes3_file import extract_scripts_from_plugin

script = '''begin TTD_WindowScript

if ( doOnce == 0 )
		if ( GetJournalIndex "ttd_orcmason" == 180 )
			If ( getdistance player ) < 500
					playgroup "idle2" 1
					set DoOnce to 1
					return
			endif
		endif
	endif
elseif DoOnce == 1
	playgroup "idle3" 0
	if Timer < 5
		Set Timer to timer + Getsecondspassed
	else
		disable
		journal ttd_orcmason 181
	return
	endif
endif


end'''

debug = True

if debug:

    ast = parser.parse(script)
    #print(ast)
    if ast:
        cfg = build_cfg(ast)

        if cfg:
            #for block in cfg.blocks:
            #    print(block)

            result = evaluate_cfg_cost(cfg, ast)
            if result:
                print(result)
            else:
                print("no result")
        else:
            print("no cfg")
    else:
        print("no ast")

else:
    scripts = extract_scripts_from_plugin('TTD_UnderMassersGaze_EXPORT.esp')
    #print("scripts found:" + str(len(scripts)))
    for scpt in scripts:
        print(len(scpt))
        print(scpt[0 : 20])
        ast = parser.parse(scpt)
        if ast:
            cfg = build_cfg(ast)
            if cfg:
                #for block in cfg.blocks:
                #    print(block)

                print(len(cfg.blocks))

                #result = evaluate_cfg_cost(cfg, ast)
                #print(result)

#            else:
#                print("no cfg")
#        else:
#            print("no ast")


    
