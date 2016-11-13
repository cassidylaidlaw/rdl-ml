import re

polymorphic = re.compile("[tuvk]$")
otherInfo = re.compile("^(.+) (.+)")


#parses type signatures for csv output
def parse_sigs(klass_sigs):
    #klass_sigs is dict
    #keys are method name, val is return types
    type_sigs = []
    for k,v in klass_sigs.items():
        if k.startswith("<=>"):
             #not sure if i should make this its own type
             #or just say it returns nil or a number
            continue
        for rType in v:
            if polymorphic.match(rType):
                continue
            match = otherInfo.match(rType)
            if match:
                type_sigs.append([k,match.group(1)])
            else:
                type_sigs.append([k,rType])
            #if a method has multiple return types
            #it will be on multiple lines
    return type_sigs
