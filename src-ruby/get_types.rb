# uses rdl query to output type from specifed class to json file
require 'rdl'
require 'types/core'
require 'json'

# returns true if arr of class name strings (pared from rdl_query) are rClass or
# a child of rClass
def type_check_arr(arr, rClass)
    arr.all? do |x|
      begin
           Object.const_get(x) <= rClass
       rescue NameError, TypeError
           false
       end end
end

if ARGV.length != 1
    puts 'Usage: ruby get_types <rdl query command>'
    puts 'Uses rdl_query to output the type of the specifed class/method to stdout'
else
    method_hash = {}
    begin # capture stdout
       old_stdout = $stdout
       $stdout = StringIO.new('', 'w')
       rdl_query(ARGV[0])
       methods = $stdout.string.split("\n")

       methods.each do |sig|
           next unless /^(.+):/.match(sig)
           name = Regexp.last_match(1)
           types = sig[sig.rindex('->') + 3..-1]
           types.gsub!(/<.*>|{.*}/, '')
           types.gsub!(/\[.*\]/, 'Array') # some type sigs have array syntax in the signature
           types = types.split(' or ')

           types.map! do |x|
               tmp = x.strip
               x = tmp if tmp
               x.gsub!(/[\[\]]/, '')
               x.gsub(/ r$/, '') # remove r that is usally there for post condtions
               # gross but its 2:20am sooooooooo
           end

           if types.all? { |x| x == 'true' || x == 'false' || x =='nil'}
               types = ['Bool']
           elsif type_check_arr(types, Integer)
               types = ['Integer']
           elsif type_check_arr(types, Numeric)
               types = ['Numeric']
           end
           method_hash[name] = types
       end

   ensure
       # restore stdout just in case
       $stdout = old_stdout
       puts method_hash.to_json
   end

end
