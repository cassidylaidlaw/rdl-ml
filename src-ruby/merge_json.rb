require 'json'
require_relative 'parse_type_sig'


if ARGV.length != 2
  puts "Usage: ruby guess_types.rb <json file input>, <json file out>"
  puts "combines the output of guess_types.rb into one file"
  exit
end
input_json = ARGV[0]
output_json = ARGV[1]

#file -> klass -> meth -> meth info
data_hash = JSON.parse(File.read(input_json))
#out_hash = Hash.new { |hash, key| hash[key] =  Hash.new { |hash2, key2| hash2[key2] = Hash.new { |hash3, key3| hash3[key3] =  []} }}
out_hash = {}
data_hash.each{|fname,klass_hash|
  klass_hash.each{|klass_str,meth_hash|
    if out_hash[klass_str] then
      meth_hash.each{|meth_str,meth_info_hash|
        if out_hash[klass_str][meth_str] then
          #only check for types if it has parameter_names, parameter_names wont chnage so dont update them
          if out_hash[klass_str][meth_str]['parameter_names'] then
            new_arr = meth_info_hash['parameter_types']
            out_arr = out_hash[klass_str][meth_str]['parameter_types']
            new_arr.each_index{|i|
              if out_arr[i] then
                out_arr[i].concat(new_arr[i]).uniq!
                out_arr[i] = simplify_arr(out_arr[i])
              else
                out_arr[i] = new_arr[i]
              end
            }
            out_hash[klass_str][meth_str]['parameter_types'] = out_arr
          end
            ret_types = out_hash[klass_str][meth_str]['ret_types']
            meth_info_hash['ret_types'].each{|x|
              ret_types.push(x).uniq!
            }
            out_hash[klass_str][meth_str]['ret_types'] = simplify_arr(ret_types)
        else
          out_hash[klass_str][meth_str] = meth_info_hash
        end
      }
    else
      out_hash[klass_str] = meth_hash
    end
  }
}
#puts "out_hash #{out_hash}"
File.write(output_json, out_hash.to_json)
