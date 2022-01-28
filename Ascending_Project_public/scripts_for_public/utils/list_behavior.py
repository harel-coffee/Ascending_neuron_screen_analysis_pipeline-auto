##behavior
behaviors=[
'forward_walking',
'backward_walking',
'pushing',
'rest',
'eye_grooming',
'antennal_grooming',
'foreleg_grooming',
'hindleg_grooming',
'abdominal_grooming',
'proboscis_extension',
'CO2_puff'
]





## Joint_pos =  Leg + joint + joint_angle, for example, LF_leg coxa x
list_legs=[
'LF_leg',
'LM_leg',
'LH_leg',
'RF_leg',
'RM_leg',
'Rh_leg'
]

list_joint=[
'coxa',
'femur',
'tibia',
'tarsus',
'claw'
]

list_xyz=['x','y','z']



## Joint_angle = Leg + joint_angle, for example, LF_leg yaw
joint_angle=[
'yaw',
'pitch',
'roll',
'th_fe',
'th_ti',
'roll_tr',
'th_ta',
]


list_ball_rotation=[
'Pitch',
'Roll',
'Yaw',
]


leg_order_Victor = [
'RH_leg','RM_leg','RF_leg',
'LH_leg','LM_leg','LF_leg'
]


leg_order_Florian=[
'LF_leg', 'LM_leg', 'LH_leg',
'RF_leg', 'RM_leg', 'RH_leg',
]

joint_order = ['Coxa','Femur','Tibia','Tarsus','Claw']
joint_order_rev = ['Claw','Tarsus','Tibia','Femur','Coxa']


# leg_pairs_order=['Front legs','Middle legs','Hind legs']
leg_pairs_order=[
'Left front leg - Right front leg',
'Left front leg - Right middle leg',
'Left front leg - Right hind leg',
'Left front leg - Left middle leg',
'Left front leg - Left hind leg',
'Left middle leg - Right front leg',
'Left middle leg - Right middle leg',
'Left middle leg - Right hind leg',
'Left middle leg - Left hind leg',
'Left hind leg - Right front leg',
'Left hind leg - Right middle leg',
'Left hind leg - Right hind leg'
]


legs_order=['Left front leg','Left middle leg','Left hind leg','Right front leg','Right middle leg','Right hind leg']
jangles_order_Florian=[
'Angle.LF_leg.yaw', # ThC yaw
'Angle.LF_leg.pitch', # ThC pitch
'Angle.LF_leg.roll', # ThC roll
'Angle.LF_leg.th_fe', # CTr pitch
'Angle.LF_leg.th_ti', # FTi pitch
'Angle.LF_leg.roll_tr', # CTr roll
'Angle.LF_leg.th_ta', #TiTa pitch
'Angle.LM_leg.yaw',
'Angle.LM_leg.pitch',
'Angle.LM_leg.roll',
'Angle.LM_leg.th_fe',
'Angle.LM_leg.th_ti',
'Angle.LM_leg.roll_tr',
'Angle.LM_leg.th_ta',
'Angle.LH_leg.yaw',
'Angle.LH_leg.pitch',
'Angle.LH_leg.roll',
'Angle.LH_leg.th_fe',
'Angle.LH_leg.th_ti',
'Angle.LH_leg.roll_tr',
'Angle.LH_leg.th_ta',
'Angle.RF_leg.yaw',
'Angle.RF_leg.pitch',
'Angle.RF_leg.roll',
'Angle.RF_leg.th_fe',
'Angle.RF_leg.th_ti',
'Angle.RF_leg.roll_tr',
'Angle.RF_leg.th_ta',
'Angle.RM_leg.yaw',
'Angle.RM_leg.pitch',
'Angle.RM_leg.roll',
'Angle.RM_leg.th_fe',
'Angle.RM_leg.th_ti',
'Angle.RM_leg.roll_tr',
'Angle.RM_leg.th_ta',
'Angle.RH_leg.yaw',
'Angle.RH_leg.pitch',
'Angle.RH_leg.roll',
'Angle.RH_leg.th_fe',
'Angle.RH_leg.th_ti',
'Angle.RH_leg.roll_tr',
'Angle.RH_leg.th_ta',
]

jangles_order_NeuroMechFly=[
'LF ThC yaw', # ThC yaw
'LF ThC pitch', # ThC pitch
'LF ThC roll', # ThC roll
'LF CTr pitch', # CTr pitch
'LF FTi pitch', # FTi pitch
'LF CTr roll', # CTr roll
'LF TiTa pitch', #TiTa pitch
'LM ThC yaw', 
'LM ThC pitch', 
'LM ThC roll', 
'LM CTr pitch', 
'LM FTi pitch', 
'LM CTr roll', 
'LM TiTa pitch', 
'LH ThC yaw', 
'LH ThC pitch', 
'LH ThC roll', 
'LH CTr pitch', 
'LH FTi pitch', 
'LH CTr roll', 
'LH TiTa pitch', 
'RF ThC yaw', 
'RF ThC pitch', 
'RF ThC roll', 
'RF CTr pitch', 
'RF FTi pitch', 
'RF CTr roll', 
'RF TiTa pitch', 
'RM ThC yaw', 
'RM ThC pitch', 
'RM ThC roll', 
'RM CTr pitch', 
'RM FTi pitch', 
'RM CTr roll', 
'RM TiTa pitch', 
'RH ThC yaw', 
'RH ThC pitch', 
'RH ThC roll', 
'RH CTr pitch', 
'RH FTi pitch', 
'RH CTr roll', 
'RH TiTa pitch', 
]




all_brain_areas=[
'LOP',
'GOR',
'SIP',
'VES',
'GA',
'IPS',
'ATL',
'EPA',
'LAL',
'RUB',
'AME',
'ME',
'ICL',
'PRW',
'SCL',
'CAN',
'IB',
'CRE',
'FLA',
'SPS',
'LO',
'NO',
'CA',
'PB',
'ROB',
'BU',
'PED',
'LH',
"αL",
"α'L",
"βL",
"β'L",
'γL',
'AL',
'FB',
'EB',
'AOTU',
'SMP',
'SLP',
'PLP',
'PVLP',
'SAD',
'AMMC',
'WED',
'GNG',
'AVLP',
]













