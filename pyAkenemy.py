################################################################################################################################################################################################################################################
# IMPORT
################################################################################################################################################################################################################################################

import json
import re
import glob

################################################################################################################################################################################################################################################
# JSON
################################################################################################################################################################################################################################################

json_Database       =   json.loads(open("json/gamedata/zh_CN/gamedata/levels/enemydata/enemy_database.json").read())
json_DatabaseEN     =   json.loads(open("json/gamedata/en_US/gamedata/levels/enemydata/enemy_database.json").read())

json_Handbook       =   json.loads(open("json/gamedata/zh_CN/gamedata/excel/enemy_handbook_table.json").read())
json_HandbookEN     =   json.loads(open("json/gamedata/en_US/gamedata/excel/enemy_handbook_table.json").read())

json_activity       =   json.loads(open("json/gamedata/zh_CN/gamedata/excel/activity_table.json").read())
json_activityEN     =   json.loads(open("json/gamedata/en_US/gamedata/excel/activity_table.json").read())

json_CC             =   json.loads(open("json/gamedata/zh_CN/gamedata/excel/crisis_table.json").read())
json_CC2            =   json.loads(open("json/gamedata/zh_CN/gamedata/excel/crisis_v2_table.json").read())
json_CCEN           =   json.loads(open("json/gamedata/en_US/gamedata/excel/crisis_table.json").read())
json_CC2EN          =   json.loads(open("json/gamedata/en_US/gamedata/excel/crisis_v2_table.json").read())

json_IS0            =   json.loads(open("json/gamedata/zh_CN/gamedata/excel/roguelike_table.json").read())
json_IS             =   json.loads(open("json/gamedata/zh_CN/gamedata/excel/roguelike_topic_table.json").read())
json_ISEN0          =   json.loads(open("json/gamedata/en_US/gamedata/excel/roguelike_table.json").read())
json_ISEN           =   json.loads(open("json/gamedata/en_US/gamedata/excel/roguelike_topic_table.json").read())

json_SSS            =   json.loads(open("json/gamedata/zh_CN/gamedata/excel/climb_tower_table.json").read())
json_SSSEN          =   json.loads(open("json/gamedata/en_US/gamedata/excel/climb_tower_table.json").read())

json_stage          =   json.loads(open("json/gamedata/zh_CN/gamedata/excel/stage_table.json").read())
json_stageEN        =   json.loads(open("json/gamedata/en_US/gamedata/excel/stage_table.json").read())

json_zone           =   json.loads(open("json/gamedata/zh_CN/gamedata/excel/zone_table.json").read())
json_zoneEN         =   json.loads(open("json/gamedata/en_US/gamedata/excel/zone_table.json").read())

Fillerjson          =   json.loads(open("json/Filler.json").read())

################################################################################################################################################################################################################################################
# STAT GRADER
################################################################################################################################################################################################################################################
#   statgrade={"attack":{},"def":{},"magicRes":{},"maxHP":{},"moveSpeed":{},"attackSpeed":{},"enemyDamageRes":{},"enemyRes":{}}
#
#   for statclass in json_HandbookEN["levelInfoList"]:
#       for stat in statclass.keys():
#           if stat != "classLevel":
#               statgrade[stat][statclass["classLevel"]]=statclass[stat]["max"] if stat == "attackSpeed" else statclass[stat]["min"]
#
#   print(statgrade)
#

STAT = {
            'attack'            : {'SS': 5000.0, 'S+': 3000.0, 'S': 2000.0, 'A+': 1500.0, 'A': 1000.0, 'B+': 700.0, 'B': 500.0, 'C': 300.0, 'D': 200.0, 'E': 0.0}, 
            'def'               : {'SS': 5000.0, 'S+': 3000.0, 'S': 2000.0, 'A+': 1200.0, 'A': 1000.0, 'B+': 800.0, 'B': 500.0, 'C': 200.0, 'D': 100.0, 'E': 0.0}, 
            'magicRes'          : {'SS': 90.0, 'S+': 80.0, 'S': 70.0, 'A+': 60.0, 'A': 50.0, 'B+': 30.0, 'B': 20.0, 'C': 10.0, 'D': 1.0, 'E': 0.0}, 
            'maxHP'             : {'SS': 500000.0, 'S+': 250000.0, 'S': 100000.0, 'A+': 25000.0, 'A': 12000.0, 'B+': 8000.0, 'B': 5000.0, 'C': 3500.0, 'D': 1000.0, 'E': 0.0}, 
            'moveSpeed'         : {'SS': 2.0, 'S+': 1.8, 'S': 1.5, 'A+': 1.2, 'A': 1.0, 'B+': 0.9, 'B': 0.7, 'C': 0.5, 'D': 0.3, 'E': 0.0}, 
            'attackSpeed'       : {'SS': 0.5, 'S+': 0.8, 'S': 1.0, 'A+': 1.2, 'A': 1.7, 'B+': 2.6, 'B': 3.5, 'C': 5.0, 'D': 6.9, 'E': -1.0}, 
            'enemyDamageRes'    : {'SS': 90.0, 'S+': 80.0, 'S': 70.0, 'A+': 60.0, 'A': 50.0, 'B+': 30.0, 'B': 20.0, 'C': 10.0, 'D': 1.0, 'E': 0.0}, 
            'enemyRes'          : {'SS': 90.0, 'S+': 80.0, 'S': 70.0, 'A+': 60.0, 'A': 50.0, 'B+': 30.0, 'B': 20.0, 'C': 10.0, 'D': 1.0, 'E': 0.0}
            }
################################################################################################################################################################################################################################################
# Enemies Database Query ??
################################################################################################################################################################################################################################################
querydatabase={}
querydatabaseEN={}

for enemy in json_Database["enemies"]:
    querydatabase[enemy["Key"]]=enemy["Value"]
for enemy in json_DatabaseEN["enemies"]:
    querydatabaseEN[enemy["Key"]]=enemy["Value"]

################################################################################################################################################################################################################################################
# Test Area
################################################################################################################################################################################################################################################
enemy_database={}
enemy_abilitiesdatabase={}
errortest=0

enemy_damageType=[]
enemyTag=[]
enemymotion=[]
enemyapplyWay=[]
'''
for enemy in json_Handbook["enemyData"]:
    ## Handbook Test
    if json_Handbook["enemyData"][enemy]["hideInHandbook"] :
        continue
    else :
        database = querydatabaseEN if enemy in querydatabaseEN.keys() else querydatabase
        handbook = json_HandbookEN["enemyData"] if enemy in json_HandbookEN["enemyData"].keys() else json_Handbook["enemyData"]

    abilitiescheck = {
                        "abilityList"         : len(handbook[enemy]["abilityList"]),
                        "talentBlackboard"    : database[enemy][0]["enemyData"]["talentBlackboard"],
                        "skills"              : database[enemy][0]["enemyData"]["skills"],
                        "spData"              : database[enemy][0]["enemyData"]["spData"],
                        "all"                 : len(handbook[enemy]["abilityList"]) or database[enemy][0]["enemyData"]["talentBlackboard"] or database[enemy][0]["enemyData"]["skills"] or database[enemy][0]["enemyData"]["spData"]
                    }
    
    ## Data Test
    if (" & ").join(handbook[enemy]["damageType"]) not in enemy_damageType :enemy_damageType.append((" & ").join(handbook[enemy]["damageType"]))
    if str(handbook[enemy]["enemyTags"]) not in enemyTag :enemyTag.append(str(handbook[enemy]["enemyTags"]))
    if database[enemy][0]["enemyData"]["motion"]["m_value"] not in enemymotion : enemymotion.append(database[enemy][0]["enemyData"]["motion"]["m_value"])
    if database[enemy][0]["enemyData"]["applyWay"]["m_value"] not in enemyapplyWay : enemyapplyWay.append(database[enemy][0]["enemyData"]["applyWay"]["m_value"])

    ## Data Handle
    enemy_database[enemy]=  {
                                "enemyId"           : handbook[enemy]["enemyId"],
                                "name"              : handbook[enemy]["name"],
                                "enemyIndex"        : handbook[enemy]["enemyIndex"],
                                "sortId"            : handbook[enemy]["sortId"],
                                "enemyLevel"        : handbook[enemy]["enemyLevel"],
                                "description"       : handbook[enemy]["description" ],
                                "abilityList"       : handbook[enemy]["abilityList"],
                                "linkEnemies"       : handbook[enemy]["linkEnemies"],
                                "damageType"        : handbook[enemy]["damageType"],
                                
                                "applyWay"          : database[enemy][0]["enemyData"]["applyWay"]["m_value"],
                                "motion"            : database[enemy][0]["enemyData"]["motion"]["m_value"],
                                "enemyTags"         : database[enemy][0]["enemyData"]["enemyTags"]["m_value"],
                                "lifePointReduce"   : database[enemy][0]["enemyData"]["lifePointReduce"]["m_value"],
                                "rangeRadius"       : database[enemy][0]["enemyData"]["rangeRadius"]["m_value"],
                                "attributes"        : []
                            }

    if abilitiescheck["all"] :
        enemy_abilitiesdatabase[enemy]={
                                            "abilityList"       : handbook[enemy]["abilityList"],
                                            "talentBlackboard"  : [] if abilitiescheck["talentBlackboard"] else None ,
                                            "skills"            : [] if abilitiescheck["skills"] else None,
                                            "spData"            : [] if abilitiescheck["spData"] else None
                                        }

    for level in range(len(database[enemy])):
        levelattributes={}
        for stat in database[enemy][level]["enemyData"]["attributes"].keys():
            if database[enemy][level]["enemyData"]["attributes"][stat]["m_defined"] and database[enemy][level]["enemyData"]["attributes"][stat]["m_value"]!=database[enemy][0]["enemyData"]["attributes"][stat]["m_value"]:
                levelattributes[stat]=database[enemy][level]["enemyData"]["attributes"][stat]["m_value"]
            else:
                levelattributes[stat]=database[enemy][0]["enemyData"]["attributes"][stat]["m_value"]
        enemy_database[enemy]["attributes"].append(levelattributes)
        
        if abilitiescheck["talentBlackboard"]   : enemy_abilitiesdatabase[enemy]["talentBlackboard"].append(database[enemy][level]["enemyData"]["talentBlackboard"] if database[enemy][level]["enemyData"]["talentBlackboard"] else database[enemy][0]["enemyData"]["talentBlackboard"])
        if abilitiescheck["skills"]             : enemy_abilitiesdatabase[enemy]["skills"].append(database[enemy][level]["enemyData"]["skills"] if database[enemy][level]["enemyData"]["skills"] else database[enemy][0]["enemyData"]["skills"])
        if abilitiescheck["spData"]             : enemy_abilitiesdatabase[enemy]["spData"].append(database[enemy][level]["enemyData"]["spData"] if database[enemy][level]["enemyData"]["spData"] else database[enemy][0]["enemyData"]["spData"])

    ## New Error Check
    if len(database[enemy]) >1:
        for key in ["applyWay","motion","enemyTags","lifePointReduce","rangeRadius"]:
            if database[enemy][1]["enemyData"][key]["m_defined"] and database[enemy][0]["enemyData"][key]["m_value"] != database[enemy][1]["enemyData"][key]["m_value"]:
                print(enemy,"has {key} Level Conflict")
                errortest+=1
                if errortest==1 : print("\n#########################################################\n###################     Error Test    ###################\n#########################################################")
            
    if len(database[enemy]) >1 and abilitiescheck["all"]:
        if database[enemy][0]["enemyData"]["spData"] != database[enemy][1]["enemyData"]["spData"] and database[enemy][0]["enemyData"]["spData"] and database[enemy][1]["enemyData"]["spData"]:
            print(enemy,"has spData Level Conflict")
            errortest+=1
            if errortest==1 : print("\n#########################################################\n###################     Error Test    ###################\n#########################################################")

    if len(handbook[enemy]["linkEnemies"]):
        linkenemies=[]
        for link in handbook[enemy]["linkEnemies"]:
            if link in handbook.keys(): linkenemies.append(link)
        #print(enemy,len(linkenemies),linkenemies)
        
### print Data test

print("\n#########################################################\n###################     Data Test     ###################\n#########################################################")
print("\nDamage Type = ",enemy_damageType)
print("Enemy Tags (Handbook \"enemyTags\") = ",enemyTag)
print("Enemy Motion = ",enemymotion)
print("Enemy Attack Type = ",enemyapplyWay)
print("\n")

dumpling=json.dumps(enemy_database,indent=4, ensure_ascii=False)
with open("test/enemy_database_stat.json",'w') as JSON :
    JSON.write(dumpling)

dumpling=json.dumps(enemy_abilitiesdatabase,indent=4, ensure_ascii=False)
with open("test/enemy_database_abilities.json",'w') as JSON :
    JSON.write(dumpling)'''

'''
##########################################
##############   HANDBOOK   ##############
##########################################
    "abilityList"       : List          //  [
                                                {
                                                    "text": "Does not deduct Life Points when ...",
                                                    "textFormat": "NORMAL"  ==> ["NORMAL","TITLE",SILENCE]
                                                }
                                            ]
    
##########################################
#### DATABASE  [Level0, Level1, ...]  ####
##########################################
    note : "talentBlackboard", "skills", "spData" below Have to write date by hand (new json) with "abilityList" in HANDBOOK
    "talentBlackboard"  : List of Dict  //  [
                                                {
                                                    "key": "selfbuff.attack_speed",
                                                    "value": 40.0,
                                                    "valueStr": null
                                                }
                                            ]
    "skills"            : List of Dict  //  [
                                                {
                                                    "prefabKey": "BringDown",
                                                    "priority": 0,
                                                    "cooldown": 10000.0,
                                                    "initCooldown": 7.0,
                                                    "spCost": 0,
                                                    "blackboard": [
                                                        {
                                                            "key": "def",
                                                            "value": -0.5,
                                                            "valueStr": null
                                                        },
                                                        {
                                                            "key": "magic_resistance",
                                                            "value": -0.5,
                                                            "valueStr": null
                                                        }
                                                    ]
                                                }
                                            ]
    "spData":           : Dict          //  {
                                                "spType": "INCREASE_WHEN_ATTACK",
                                                "maxSp": 3,
                                                "initSp": 0,
                                                "increment": 1.0
                                            }
'''

################################################################################################################################################################################################################################################
# Stage collection
################################################################################################################################################################################################################################################
stage_collection={"stage":{},"zone":{},"enemy":{}} #,"ignore":{}

## stage_table || All Event / Weekly stage / Annihilation
for stage in json_stage["stages"]:
    # ignore Challenge and Story
    if stage.find("#f#")==-1 and stage.find("st_")==-1 and stage.find("_st")==-1 and stage.find("easy")==-1 and stage.find("tough")==-1 and json_stage["stages"][stage]["levelId"].find("Activities/ACT21side/Mission/")==-1 and stage.find("act4d0")==-1 and not re.search(r"lt_.+_ex", stage) and not re.search(r"bossrush_[^0]", stage):
        if json_stage["stages"][stage]["levelId"].find("/")!=-1:
            if json_stage["stages"][stage]["levelId"].split("/")[1] in ["Main","Training","Hard"]:
                stagezone = json_stage["stages"][stage]["zoneId"]
            elif json_stage["stages"][stage]["levelId"].split("/")[1] in ["Weekly","Promote"]:
                stagezone = "Supply"
            elif json_stage["stages"][stage]["levelId"].split("/")[1] in ["Legion"]:
                stagezone = json_stage["stages"][stage]["levelId"].split("/")[2]
            else:
                stagezone = json_stage["stages"][stage]["levelId"].split("/")[1]
        elif json_stage["stages"][stage]["levelId"].split("\\")[1]:
            stagezone = json_stage["stages"][stage]["levelId"].split("\\")[1]
        
        # add Stagezone
        if not stagezone in stage_collection["zone"].keys(): stage_collection["zone"][stagezone]=[]
        
        stagecode = (json_stageEN["stages"][stage]["name"] if stage in json_stageEN["stages"].keys() else json_stage["stages"][stage]["name"]) if json_stage["stages"][stage]["stageType"] == "CAMPAIGN" else json_stage["stages"][stage]["code"]
        stage_collection["zone"][stagezone].append(stagecode)
        
        stage_collection["stage"][json_stage["stages"][stage]["stageId"]] ={
                                                "stageId"   :   json_stage["stages"][stage]["stageId"],
                                                "levelId"   :   json_stage["stages"][stage]["levelId"],
                                                "zoneId"    :   json_stage["stages"][stage]["zoneId"],
                                                "code"      :   stagecode,
                                                "Event"     :   stagezone
        }
        
        stageforenemylist=json.loads(open("json/gamedata/zh_CN/gamedata/levels/"+json_stage["stages"][stage]["levelId"].lower()+".json").read())
        for enemy in stageforenemylist["enemyDbRefs"]:
            enemyid = enemy["id"]
            if enemy["overwrittenData"]: enemyid = enemy["overwrittenData"]["prefabKey"]["m_value"] if enemy["overwrittenData"]["prefabKey"]["m_defined"] else enemy["id"]
            if enemyid not in stage_collection["enemy"].keys() : stage_collection["enemy"][enemyid]={"Filtered":[],"Appearance":{}}
            if re.search(r"LT..", stagezone):
                if "Legion" not in stage_collection["enemy"][enemyid]["Filtered"]:
                    stage_collection["enemy"][enemyid]["Filtered"].append("Legion")
                    stage_collection["enemy"][enemyid]["Appearance"]["Legion"]={}
                if stagezone not in stage_collection["enemy"][enemyid]["Appearance"]["Legion"] : 
                    stage_collection["enemy"][enemyid]["Appearance"]["Legion"][stagezone]=[]
                if stagecode not in stage_collection["enemy"][enemyid]["Appearance"]["Legion"][stagezone] : stage_collection["enemy"][enemyid]["Appearance"]["Legion"][stagezone].append(stagecode)
            else:
                if stagezone not in stage_collection["enemy"][enemyid]["Filtered"] : 
                    stage_collection["enemy"][enemyid]["Filtered"].append(stagezone)
                    stage_collection["enemy"][enemyid]["Appearance"][stagezone]=[]
                if stage not in stage_collection["enemy"][enemyid]["Appearance"][stagezone] : stage_collection["enemy"][enemyid]["Appearance"][stagezone].append(stagecode)
    #else:
        #stage_collection["ignore"][json_stage["stages"][stage]["stageId"]] ={
                                                #"stageId"   :   json_stage["stages"][stage]["stageId"],
                                                #"levelId"   :   json_stage["stages"][stage]["levelId"],
                                                #"zoneId"    :   json_stage["stages"][stage]["zoneId"],
                                                #"code"      :   json_stage["stages"][stage]["code"]
        #}

## CC : Contingency Contract (危机合约)

CC1 = glob.glob("json/gamedata/zh_CN/gamedata/levels/obt/rune/*")
CC2 = glob.glob("json/gamedata/zh_CN/gamedata/levels/obt/crisis/v2/*")
POT = glob.glob("json/gamedata/zh_CN/gamedata/levels/activities/act38rune/*")

### CC Beta (act5d1) & CC Season 1 (crisis_table)
for cc in range(len(json_CC["seasonInfo"])+1):
    ccnum = str(cc-1) if cc-1 >= 10 else "0"+str(cc-1)
    CCZone = f"CC#{ccnum}" if cc>0 else "CC#Beta"
    stagenum = str(cc+1) if cc+1 >= 10 else "0"+str(cc+1)
    CCStage = [stage for stage in CC1 if re.search(rf"{stagenum}-.+\.json",stage)]+(["json/gamedata/zh_CN/gamedata/levels/obt/rune\\"+rotatestage for rotatestage in Fillerjson["CCRotate"][CCZone]] if CCZone in Fillerjson["CCRotate"].keys() else [])
    stage_collection["zone"][CCZone]=[]
    for stagepath in CCStage:
        stagecode =  Fillerjson["stages"][stagepath.split("\\")[-1]] if re.search(rf"{stagenum}-.+\.json",stagepath) else Fillerjson["stages"][stagepath.split("\\")[-1]].split(" (Main)")[0]
        stageforenemylist=json.loads(open(stagepath).read())
        for enemy in stageforenemylist["enemyDbRefs"]:
            enemyid = enemy["id"]
            if enemy["overwrittenData"]: enemyid = enemy["overwrittenData"]["prefabKey"]["m_value"] if enemy["overwrittenData"]["prefabKey"]["m_defined"] else enemy["id"]
            if enemyid not in stage_collection["enemy"].keys() : stage_collection["enemy"][enemyid]={"Filtered":[],"Appearance":{}}
            if CCZone not in stage_collection["enemy"][enemyid]["Filtered"] :
                stage_collection["enemy"][enemyid]["Filtered"].append(CCZone)
                stage_collection["enemy"][enemyid]["Appearance"][CCZone]=[]
            if stagecode not in stage_collection["enemy"][enemyid]["Appearance"][CCZone] : stage_collection["enemy"][enemyid]["Appearance"][CCZone].append(stagecode)

            stage_collection["stage"][stagepath.split("\\")[-1].split(".")[0].split("level_")[-1]] ={
                                                                                    "stageId"   :   stagepath.split("\\")[-1].split(".")[0].split("level_")[-1],
                                                                                    "levelId"   :   stagepath,
                                                                                    "zoneId"    :   CCZone,
                                                                                    "code"      :   stagecode,
                                                                                    "Event"     :   CCZone
                                                                                }
            if stagecode not in stage_collection["zone"][CCZone]:
                stage_collection["zone"][CCZone].append(stagecode)

### POT (act38rune)
stage_collection["zone"]["POT"]=[]
for stagepath in POT:
    stagecode =  Fillerjson["stages"][stagepath.split("\\")[-1]]
    stageforenemylist=json.loads(open(stagepath).read())
    for enemy in stageforenemylist["enemyDbRefs"]:
        enemyid = enemy["id"]
        if enemy["overwrittenData"]: enemyid = enemy["overwrittenData"]["prefabKey"]["m_value"] if enemy["overwrittenData"]["prefabKey"]["m_defined"] else enemy["id"]
        if enemyid not in stage_collection["enemy"].keys() : stage_collection["enemy"][enemyid]={"Filtered":[],"Appearance":{}}
        if "POT" not in stage_collection["enemy"][enemyid]["Filtered"] :
            stage_collection["enemy"][enemyid]["Filtered"].append("POT")
            stage_collection["enemy"][enemyid]["Appearance"]["POT"]=[]
        if stagecode not in stage_collection["enemy"][enemyid]["Appearance"]["POT"] : stage_collection["enemy"][enemyid]["Appearance"]["POT"].append(stagecode)

        stage_collection["stage"][stagepath.split("\\")[-1].split(".")[0].split("level_")[-1]] ={
                                                                                "stageId"   :   stagepath.split("\\")[-1].split(".")[0].split("level_")[-1],
                                                                                "levelId"   :   stagepath,
                                                                                "zoneId"    :   "POT",
                                                                                "code"      :   stagecode,
                                                                                "Event"     :   "POT"
                                                                            }
        if stagecode not in stage_collection["zone"]["POT"]:
            stage_collection["zone"]["POT"].append(stagecode)


### CC Season 2 (crisis_v2_table)
for cc in range(len(json_CC2["seasonInfoDataMap"].keys())):
    ccnum = str(cc+1) if cc+1 >= 10 else "0"+str(cc+1)
    CCZone = f"CCBP#{ccnum}"
    stagenum = str(cc+1) if cc+1 >= 10 else "0"+str(cc+1)
    CCStage = [stage for stage in CC2 if re.search(rf"{stagenum}-.+\.json",stage)]+(["json/gamedata/zh_CN/gamedata/levels/obt/crisis/v2\\"+rotatestage for rotatestage in Fillerjson["CCRotate"][CCZone]] if CCZone in Fillerjson["CCRotate"].keys() else [])
    if cc ==0 : CCStage = list(filter(lambda x : re.search(rf"v2_01-0[^46]",x),CCStage))
    stage_collection["zone"][CCZone]=[]
    for stagepath in CCStage:
        stagecode =  Fillerjson["stages"][stagepath.split("\\")[-1]] if re.search(rf"{stagenum}-.+\.json",stagepath) else Fillerjson["stages"][stagepath.split("\\")[-1]].split(" (Main)")[0]
        stageforenemylist=json.loads(open(stagepath).read())
        for enemy in stageforenemylist["enemyDbRefs"]:
            enemyid = enemy["id"]
            if enemy["overwrittenData"]: enemyid = enemy["overwrittenData"]["prefabKey"]["m_value"] if enemy["overwrittenData"]["prefabKey"]["m_defined"] else enemy["id"]
            if enemyid not in stage_collection["enemy"].keys() : stage_collection["enemy"][enemyid]={"Filtered":[],"Appearance":{}}
            if CCZone not in stage_collection["enemy"][enemyid]["Filtered"] :
                stage_collection["enemy"][enemyid]["Filtered"].append(CCZone)
                stage_collection["enemy"][enemyid]["Appearance"][CCZone]=[]
            if stagecode not in stage_collection["enemy"][enemyid]["Appearance"][CCZone] : stage_collection["enemy"][enemyid]["Appearance"][CCZone].append(stagecode)

            stage_collection["stage"][stagepath.split("\\")[-1].split(".")[0].split("level_")[-1]] ={
                                                                                    "stageId"   :   stagepath.split("\\")[-1].split(".")[0].split("level_")[-1],
                                                                                    "levelId"   :   stagepath,
                                                                                    "zoneId"    :   CCZone,
                                                                                    "code"      :   stagecode,
                                                                                    "Event"     :   CCZone
                                                                                }
            if stagecode not in stage_collection["zone"][CCZone]:
                stage_collection["zone"][CCZone].append(stagecode)

## IS
### IS 1


### IS 2+

dumpling=json.dumps(stage_collection,indent=4, ensure_ascii=False)
with open("test/stage.json",'w') as JSON :
    JSON.write(dumpling)

################################################################################################################################################################################################################################################
# Activity
################################################################################################################################################################################################################################################
activity={"Dict":{}}
timeline=[]
# Activity
for act in json_activity["basicInfo"].keys():
    if json_activity["basicInfo"][act]["hasStage"]:
        activity["Dict"][act]={
                        "nameCN":json_activity["basicInfo"][act]["name"],
                        "nameEN":json_activityEN["basicInfo"][act]["name"] if act in json_activityEN["basicInfo"].keys() else None,
                        "startCN":json_activity["basicInfo"][act]["startTime"]
        }
        timeline.append([json_activityEN["basicInfo"][act]["name"] if act in json_activityEN["basicInfo"].keys() else json_activity["basicInfo"][act]["name"],json_activity["basicInfo"][act]["startTime"]])

## CC#1


'''timeline.sort(reverse=False,key=lambda event : event[1])
activity["Timeline"]=timeline

dumpling=json.dumps(activity,indent=4, ensure_ascii=False)
with open("test/activity.json",'w') as JSON :
    JSON.write(dumpling)'''