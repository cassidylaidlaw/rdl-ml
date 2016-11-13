# uses rdl query to output type from specifed class to json file
require 'rdl'
require 'types/core'

require 'json'
require_relative 'parse_type_sig'


if ARGV.length != 1
    puts 'Usage: ruby get_types <rdl query command>'
    puts 'Uses rdl_query to output the type of the specifed class/method to stdout'
else
  #Class.instance_method(<symbol>).parameters
    method_hash = {}
    begin # capture stdout
       old_stdout = $stdout
       $stdout = StringIO.new('', 'w')
       rdl_query(ARGV[0])
       methods = $stdout.string.split("\n")

       methods.each do |sig|
           name,return_types = parse_type_sig(sig)
           method_hash[name] = return_types if name
       end

   ensure
       # restore stdout just in case
       $stdout = old_stdout
       puts method_hash.to_json
   end

end
