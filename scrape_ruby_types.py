typeFile = "core-types/array.rb"

class Method_type:

    def __init__(self,name,type_sig:list):
        #self.class_name = class_name
        self.name = name
        self.type_sig = type_sig

    def add_type_sig(self,type_sig):
        self.type_sig += type_sig



class Class_type:
    def __init__(self,name,poly_types = [],method_types = {}):
        self.name = name
        self.poly_types = poly_types
        self.method_types = method_types
        #hash where key is method name, and value is the method_type class for that method

    def add_poly_types(self,poly_types:list):
        self.poly_types+=poly_types

    def add_method_type(self,method_type):
        if method_type.name in self.method_types:
            self.method_types[method_type.name].add_type_sig(method_type.type_sig)
        else:
            self.method_types[method_type.name] = method_type

cType = None
with open(typeFile) as rb_file:
    for tmpLine in rb_file:
        line = tmpLine.strip()
        if cType is None and line.startswith("class"):
            class_name = line.split(' ')[1]
            cType = Class_type(class_name)
        elif line.startswith("type_params"):
            #get string with the poly type list without the brackets
            poly_types_string = line[line.index('[')+1:line.index(']')].replace(':','')
            poly_types = [elm.strip() for elm in poly_types_string.split(',')]
            cType.add_poly_types(poly_types)
        elif line.startswith("type"):
            m_name = line[line.index(':')+1:line.index(',')].strip()
            type_sig = [line[line.index("'")+1:-1]] #array with only elm being string
            cType.add_method_type(Method_type(m_name,type_sig))
            #m_type = method_type(m_name,type_sig)

print("method_types")
for k in cType.method_types:
    print("name:{},type_sig{}".format(k,cType.method_types[k].type_sig))
