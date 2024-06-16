import re
import os


# dir containing all .rules files you wish to enable
def find_enabled_rules(rulepath):
    files = [f for f in os.listdir(rulepath) if ".rules" in f]
    return files
   

# dir containing all .rules files you wish to disable 
def find_disabled_rules(rulepath):
    files = [f for f in os.listdir(rulepath) if ".rules" in f]
    return files


def search_flowbits_in_rulesets(rulepath, rules, enabled_flowbits):
    for file in rules:
        print(f"Opening rules file -> {rulepath}{file}")
            
        with open(f"{rulepath}{file}", "r") as f:
            rule_file = f.readlines()

        for rule in rule_file:
            for result_dict in enabled_flowbits:
                if f":set,{result_dict['Flowbit Name'][0].strip()}" in rule:
                    sid = re.search(r"sid:(\d{7});", rule).group(1)
                    result_dict["Dependency"].append(sid)

    for entry in enabled_flowbits:
        print(entry)
               
    return enabled_flowbits


def find_flowbits(rulepath, rules):
    re_msg = re.compile(r"msg:\"([^\"]+)\";")
    re_sid = re.compile(r"sid:(\d{7});")
    re_flowbit_gate = re.compile(r"^#?alert.+flowbits:isset,([^;]+);")
    re_flowbit_precise = re.compile(r"flowbits:isset,([^;]+);")
    
    # list of dicts
    results = []
    
    for file in rules:
        print(f"Opening rules file -> {rulepath}{file}")
        
        with open(f"{rulepath}{file}", "r") as f:
            rule_file = f.readlines()
        
        for rule in rule_file:
            if re.search(re_flowbit_gate, rule):
                tmp_dct = {}
                
                if re.search(re_sid, rule):
                    sid = re.search(re_sid, rule).group(1)
                    tmp_dct.update({"isset Rule SID": int(sid)})
                    
                if re.search(re_msg, rule):
                    msg = re.search(re_msg, rule).group(1)
                    tmp_dct.update({"Rule Message": msg})
                
                flowbits = re.findall(re_flowbit_precise, rule)
                
                if flowbits:
                    tmp_dct.update({"Flowbit Name": flowbits})
                    
                tmp_dct.update({"Dependency": []})
                
                results.append(tmp_dct)
    
    return results


def main(enabled_rulepath, disabled_rulepath):
    # builds a list of .rules filenames from the directory provided
    enabled_rules  = find_enabled_rules(enabled_rulepath)
    # builds a list of .rules filenames from the directory provided
    disabled_rules = find_disabled_rules(disabled_rulepath)
    # iterates the list of .rules files and builds a list of dicts if an 'isset' flowbit is found
    enabled_flowbits = find_flowbits(enabled_rulepath, enabled_rules)
    # search each 'isset' flowbit found previously in all enabled rules files
    enabled_flowbits = search_flowbits_in_rulesets(enabled_rulepath, enabled_rules, enabled_flowbits)
    # search each 'isset' flowbit found previously in all disabled rules files
    enabled_flowbits = search_flowbits_in_rulesets(disabled_rulepath, disabled_rules, enabled_flowbits)


if __name__ == '__main__':
    enabled_rulepath = input("Enter the filepath for your enabled rules: ")
    disabled_rulepath = input("Enter the filepath for your enabled rules: ")
    
    if enabled_rulepath.endswith('/'):
        pass
    else:
        enabled_rulepath = f"{enabled_rulepath}/"
        
    if disabled_rulepath.endswith('/'):
        pass
    else:
        disabled_rulepath = f"{disabled_rulepath}/"

    
    #enabled_rulepath = ""
    #disabled_rulepath = ""
    
    main(enabled_rulepath, disabled_rulepath)
