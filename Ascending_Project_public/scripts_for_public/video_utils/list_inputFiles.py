


#(2P_date, 2P_genotype, 2P_fly, 2P_recroding, 2P_representative_frame, 2P_trim_start_time (s), 2P_trim_end_time (s), CC_fluorescein_recording, confocal_data, confocal_genotype, confocal_fly)

#todo: check which 2P recording, cc512, confocal images are representative, 

trace_intvl=150



## ANs with activity:
experiments_Activity=[
##trim based on selected time (s), period = 150 s
('20180720',    'MAN-tdTomGC6fopt', 'fly2', '005', 211, 95,95+trace_intvl, 'cc512_000', '20171208', 'MAN-GFP', '1'), 
('20181202', 'R70H06-tdTomGC6fopt', 'fly1', '002', 333, 40,40+trace_intvl, 'cc512_000', '20181105', 'R70H06-GFP', '3'), 
('20181128', 'R30A08-tdTomGC6fopt', 'fly2', '001', 235, 0,0+trace_intvl, 'cc512_000', '20181027', 'R30A08-GFP', '1'),  
('20181230', 'R36G04-tdTomGC6fopt', 'fly1', '003', 380, 5,5+trace_intvl, 'cc512_001', '20181117', 'R36G04-GFP', '1'),  
('20181125', 'R85A11-tdTomGC6fopt', 'fly1', '002', 463, 80,80+trace_intvl, 'cc512_000', '20181117', 'R85A11-GFP', '2'),  
('20190220', 'SS25469-tdTomGC6fopt', 'fly1', '006', 31, 0,0+trace_intvl, 'cc512_006', '20190416', 'SS25469-smFP', '2'),  
('20190311', 'SS27485-tdTomGC6fopt', 'fly2', '004', 646, 10,10+trace_intvl, 'cc512_001', '20190416', 'SS27485-smFP', '3'),  
('20190326', 'SS28596-tdTomGC6fopt', 'fly2', '008', 626, 98,98+trace_intvl, 'cc512_001', '20190425', 'SS28596-smFP', '3'),  
('20190318', 'SS29621-tdTomGC6fopt', 'fly1', '006', 654, 80,80+trace_intvl, 'cc512_000', '20190425', 'SS29621-smFP', '1'),  
('20190328', 'SS29893-tdTomGC6fopt', 'fly3', '001', 262, 0,0+trace_intvl, 'cc512_000', '20190524', 'SS29893-smFP', '1'), 
('20190415', 'SS29633-tdTomGC6fopt', 'fly1', '005', 534, 5,5+trace_intvl, 'cc512_001', '20190506', 'SS29633-smFP', '2'),  
('20190405', 'SS30303-tdTomGC6fopt', 'fly2', '005', 842, 85,85+trace_intvl, 'cc512_002', '20190513', 'SS30303-smFP', '2'),  
('20190412', 'SS31232-tdTomGC6fopt', 'fly3', '001', 341, 5,5+trace_intvl, 'cc512_003', '20190513', 'SS31232-smFP', '2'),  
('20190408', 'SS31219-tdTomGC6fopt', 'fly1', '002', 147, 10,10+trace_intvl, 'cc512_004', '20190805', 'SS31219-smFP', '2'),  
('20190410', 'SS31456-tdTomGC6fopt', 'fly1', '006', 441, 0,0+trace_intvl, 'cc512_002', '20190506', 'SS31456-smFP', '1'), 
('20190417', 'SS31480-tdTomGC6fopt', 'fly1', '001', 441, 10,10+trace_intvl, 'cc512_002', '20190506', 'SS31480-smFP', '2'),  
('20190522', 'SS34574-tdTomGC6fopt', 'fly2', '001', 323, 95,95+trace_intvl, 'cc512_002', '20190524', 'SS34574-smFP', '1'),  
('20190517', 'SS36112-tdTomGC6fopt', 'fly1', '007', 1061, 50,90+trace_intvl, 'cc512_000', '20190524', 'SS36112-smFP', '1'),  
('20190516', 'SS36118-tdTomGC6fopt', 'fly4', '003', 261, 90,90+trace_intvl, 'cc512_000', '20190702', 'SS36118-smFP', '1'),  
('20190521', 'SS36131-tdTomGC6fopt', 'fly1', '001', 588, 148,148+trace_intvl, 'cc512_002', '20190621', 'SS36131-smFP', '1'),  
('20190531', 'SS38592-tdTomGC6fopt', 'fly3', '004', 748 ,80,80+trace_intvl, 'cc512_001', '20190517', 'SS38592-smFP', '2'),  
('20190606', 'SS38624-tdTomGC6fopt', 'fly3', '003', 365, 5,5+trace_intvl, 'cc512_001', '20190524', 'SS38624-smFP', '1'),  
('20190604', 'SS38631-tdTomGC6fopt', 'fly2', '004', 450, 20,20+trace_intvl, 'cc512_002', '20190517', 'SS38631-smFP', '2'), 
('20190629', 'SS41815-tdTomGC6fopt', 'fly1', '002', 585, 0,0+trace_intvl, 'cc512_001', '20190604', 'SS41815-smFP', '3'),  
('20190624', 'SS41822-tdTomGC6fopt', 'fly2', '002', 145, 50,90+trace_intvl, 'cc512_001', '20190621', 'SS41822-smFP', '2'),  
('20190615', 'SS40134-tdTomGC6fopt', 'fly1', '001', 75, 10,10+trace_intvl, 'cc512_000', '20190520', 'SS40134-smFP', '2'),  
('20190621', 'SS40619-tdTomGC6fopt', 'fly1', '002', 339, 95,95+trace_intvl, 'cc512_002', '20190621', 'SS40619-smFP', '2'),  
('20190619', 'SS41605-tdTomGC6fopt', 'fly3', '003', 288, 90,90+trace_intvl, 'cc512_004', '20190821', 'SS41605-smFP', '5'),  
('20190701', 'SS42008-tdTomGC6fopt', 'fly4', '003', 397, 0,0+trace_intvl, 'cc512_002', '20190604', 'SS42008-smFP', '3'), 
('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '011', 9, 8,8+trace_intvl, 'cc512_001', '20190624', 'SS42740-smFP', '1'),  
('20190723', 'SS45363-tdTomGC6fopt', 'fly1', '013', 355, 20,20+trace_intvl, 'cc512_003', '20190611', 'SS45363-smFP', '2'),  
('20190704', 'SS42749-tdTomGC6fopt', 'fly1', '002', 112, 80,80+trace_intvl, 'cc512_002', '20190805', 'SS42749-smFP', '3'),  
('20191001', 'SS49172-tdTomGC6fopt', 'fly1', '001', 441 ,80,80+trace_intvl, 'cc512_001', '20190805', 'SS49172-smFP', '2'),  
('20190904', 'SS51017-tdTomGC6fopt', 'fly3', '008', 330, 40,65+trace_intvl, 'cc512_001', '20190805', 'SS51017-smFP', '2'),  
('20190924', 'SS51021-tdTomGC6fopt', 'fly1', '004', 277, 12,75+trace_intvl, 'cc512_003', '20190624', 'SS51021-smFP', '2'), 
('20190906', 'SS51029-tdTomGC6fopt', 'fly4', '006', 526, 75,75+trace_intvl, 'cc512_001', '20190702', 'SS51029-smFP', '2'),  
('20190910', 'SS51038-tdTomGC6fopt', 'fly1', '005', 678, 10,50+trace_intvl, 'cc512_001', '20190624', 'SS51038-smFP', '1'), 
('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '004', 270, 0,0+trace_intvl, 'cc512_002', '20190702', 'SS51046-smFP', '2'),  
('20190918', 'SS52147-tdTomGC6fopt', 'fly1', '003', 925, 50,90+trace_intvl, 'cc512_002', '20190822', 'SS52147-smFP', '3'), 
('20180822', 'SS25451-tdTomGC6fopt', 'fly4', '012', 379, 55,55+trace_intvl, 'cc512_000', '20190406', 'SS25451-smFP', '1'),  
('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '003', 131, 0,0+trace_intvl, 'cc512_004', '20190425', 'SS29579-smFP', '3'),  
('20190610', 'SS40489-tdTomGC6fopt', 'fly3', '004', 983, 50,90+trace_intvl, 'cc512_001', 'redo', 'redo', '1'), #trim based on selected time (s), period = 150 s # missed file
('20190625', 'SS41806-tdTomGC6fopt', 'fly4', '007', 520, 80,80+trace_intvl, 'cc512_002', '20190604', 'SS41806-smFP', '1'),  
('20190717', 'SS44270-tdTomGC6fopt', 'fly1', '004', 641, 50,80+trace_intvl, 'cc512_003', '20190611', 'SS44270-smFP', '2'),  #change representative recording
('20190719', 'SS45605-tdTomGC6fopt', 'fly1', '003', 303, 30,30+trace_intvl, 'cc512_001', '20190830', 'SS45605-smFP', '4'), 
('20190712', 'SS43652-tdTomGC6fopt', 'fly2', '002', 507, 40,40+trace_intvl, 'cc512_001', '20190821', 'SS43652-smFP', '3'), 
('20190730', 'SS46233-tdTomGC6fopt', 'fly2', '005', 671, 40,50+trace_intvl, 'cc512_001_from_fly1', '20190610', 'SS46233-smFP', '2'), 

]

## AN with irregular activity:
experimens_irregular_activity=[
('20190105', 'R39G01-tdTomGC6fopt', 'fly1', '003', 563, 0,0+trace_intvl, 'cc512_000', '20180507', 'R39G01-GFP', '1'),  
('20190118', 'R69H10-tdTomGC6fopt', 'fly2', '001', 459, 90,90+trace_intvl, 'cc512_000', '20181105', 'R69H10-GFP', '2'),  
('20181227', 'R87H02-tdTomGC6fopt', 'fly3', '004', 242, 30,90+trace_intvl, 'cc512_000', '20180504', 'R87H02-GFP', '1'),  
]

## AN without significant activity:
experiments_NoActivity=[
('20181130', 'R38F09-tdTomGC6fopt', 'fly1', '005', 48, 10,10+trace_intvl, 'cc512_000', '20190216', 'R38F09-nGFP-T2A-mko-caax', '4'),  
('20180902', 'SS46269-tdTomGC6fopt', 'fly1', '005', 0,10+trace_intvl, 'cc512_000', '20190410', 'SS46269-smFP', '2'),  
('20180821', 'SS25470-tdTomGC6fopt', 'fly1', '002', 0,10+trace_intvl, 'cc512_000', '20190410', 'SS25470-smFP', '2'),  
('20190227', 'SS25478-tdTomGC6fopt', 'fly2', '002', 0,10+trace_intvl, 'cc512_006', '20190416', 'SS25478-smFP', '3'),  
('20190321', 'SS28382-tdTomGC6fopt', 'fly2', '003', 0,10+trace_intvl, 'cc512_001', '20190425', 'SS28382-smFP', '1'), 
('20190319', 'SS29574-tdTomGC6fopt', 'fly1', '001', 470, 40,40+trace_intvl, 'cc512_001', '20190425', 'SS29574-smFP', '1'),  
('20190507', 'SS31899-tdTomGC6fopt', 'fly3', '002', 0,10+trace_intvl, 'cc512_004', '20190513', 'SS31899-smFP', '1'),  
('20190523', 'SS33380-tdTomGC6fopt', 'fly1', '003', 0,10+trace_intvl, 'cc512_001', '20190513', 'SS33380-smFP', '2'),  
('20190510', 'SS33433-tdTomGC6fopt', 'fly1', '004', 775, 15,15+trace_intvl, 'cc512_003', '20190513', 'SS33433-smFP', '2'),  
('20190529', 'SS38012-tdTomGC6fopt', 'fly2', '003', 0,10+trace_intvl, 'cc512_002', '20190604', 'SS38012-smFP', '4'),  
('20190601', 'SS38386-tdTomGC6fopt', 'fly2', '003', 0,10+trace_intvl, 'cc512_001', '20190517', 'SS38386-smFP', '1'),  
('20190611', 'SS38687-tdTomGC6fopt', 'fly3', '002', 0,10+trace_intvl, 'cc512_003', '20190621', 'SS38687-smFP', '2'),  
('20190807', 'SS46290-tdTomGC6fopt', 'fly1', '002', 0,10+trace_intvl, 'cc512_003', '20190610', 'SS46290-smFP', '2'), 

('20190808', 'SS46300-tdTomGC6fopt', 'fly2', '002', 0,10+trace_intvl, 'cc512_002', '20190621', 'SS46300-smFP', '2'),  
('20190819', 'SS48406-tdTomGC6fopt', 'fly2', '002', 0,10+trace_intvl, 'cc512_002', '20190610', 'SS48406-smFP', '2'),  
('20190812', 'SS48409-tdTomGC6fopt', 'fly2', '001', 452, 50,50+trace_intvl, 'cc512_002', '20190610', 'SS48409-smFP', '1'),  
('20190815', 'SS49982-tdTomGC6fopt', 'fly3', '002', 0,10+trace_intvl, 'cc512_002', '20190805', 'SS49982-smFP', '1'),  
('20190816', 'SS50004-tdTomGC6fopt', 'fly3', '001', 303, 97,97+trace_intvl, 'cc512_002', '20190621', 'SS50004-smFP', '2'),  
('20190902', 'SS50013-tdTomGC6fopt', 'fly1', '003', 0,10+trace_intvl, 'cc512_004', '20190805', 'SS50013-smFP', '2'),  
('20190905', 'SS50652-tdTomGC6fopt', 'fly3', '002', 0,10+trace_intvl, 'cc512_002', '20190710', 'SS50652-smFP', '2'),  
]


## AN population:
experiemnts_populationANs=[
('20190115', 'R85A02-tdTomGC6fopt', 'fly4', '002', 0,10+trace_intvl, 'cc512_001', '20180514', 'R85A02-GFP', '1'),  
('20181221', 'R76B10-tdTomGC6fopt', 'fly2', '002', 0,10+trace_intvl, 'cc512_000', '20180514', 'R76B10-GFP', '3'),  
('20190109', 'R31C06-tdTomGC6fopt', 'fly1', '004', 0,10+trace_intvl, 'cc512_000', '20180507', 'R31C06-GFP', '1'),  
('20190111', 'R66C01-tdTomGC6fopt', 'fly1', '003', 0,10+trace_intvl, 'cc512_000', '20180504', 'R66C01-GFP', '2'), 
('20190116', 'R13G06-tdTomGC6fopt', 'fly1', '005', 0,10+trace_intvl, 'cc512_001', '20180514', 'R13G06-GFP', '1'),  
]

# suppfig_experiments_NotOnBall:
experiments_NotonBall=[
('20190506', 'SS32365-tdTomGC6fopt', 'fly1', '008', 233, 0,0+trace_intvl, 'cc512_003', '20190513', 'SS32365-smFP', '2'), # not on ball
('20190522', 'SS34574-tdTomGC6fopt', 'fly2', '006', 602, 80,80+trace_intvl, 'cc512_002', '20190524', 'SS34574-smFP', '1'), # not on ball
('20190531', 'SS38592-tdTomGC6fopt', 'fly3', '006', 500, 0,0+trace_intvl, 'cc512_002', '20190517', 'SS38631-smFP', '2'), # Not on ball
# ('20190604', 'SS38631-tdTomGC6fopt', 'fly2', '002', 739, 80,80+trace_intvl, 'cc512_002', '20190517', 'SS38631-smFP', '2'), # Not on ball
# ('20190604', 'SS38631-tdTomGC6fopt', 'fly2', '005', 739, 80,80+trace_intvl, 'cc512_002', '20190517', 'SS38631-smFP', '2'), # Not on ball
('20190604', 'SS38631-tdTomGC6fopt', 'fly2', '008', 739, 80,80+trace_intvl, 'cc512_002', '20190517', 'SS38631-smFP', '2'), # Not on ball
# ('20190610', 'SS40489-tdTomGC6fopt', 'fly3', '006'),
# ('20190615', 'SS40134-tdTomGC6fopt', 'fly1', '008'),
# ('20190619', 'SS41605-tdTomGC6fopt', 'fly3', '007'),
# ('20190704', 'SS42749-tdTomGC6fopt', 'fly1', '004'),
('20190712', 'SS43652-tdTomGC6fopt', 'fly2', '003', 100, 10,10+trace_intvl, 'cc512_001', '20190821', 'SS43652-smFP', '3'), # Not on ball
('20190904', 'SS51017-tdTomGC6fopt', 'fly3', '002', 0,10+trace_intvl, 'cc512_001', '20190805', 'SS51017-smFP', '2'),  # Not on ball
# ('20190904', 'SS51017-tdTomGC6fopt', 'fly3', '006'), 
('20190904', 'SS51017-tdTomGC6fopt', 'fly3', '007', 0,10+trace_intvl, 'cc512_001', '20190805', 'SS51017-smFP', '2'),  # Not on ball
('20190924', 'SS51021-tdTomGC6fopt', 'fly1', '003', 655, 12,12+trace_intvl, 'cc512_003', '20190624', 'SS51021-smFP', '2'), # not on ball

]




# Total should be 55 lines
suppfig_experiments=experiments_Activity+experimens_irregular_activity
print('len suppfig_experiments', len(suppfig_experiments))






















