require_relative 'parse_type_sig'

require 'json'
require 'pp'
if ARGV.length < 1
  puts "Usage: ruby guess_types.rb <folder of files to run>, you can specify multiple folders"
  puts "Runs the files passed and reports the types seen for each method"
  exit
end
# input_fdir = ARGV[0]

files = []
ARGV.each{|input_fdir|
  #if passing a relative dir path you may need to add an extra '../' at the beginning
  tmp = File.expand_path(input_fdir +"/*" , __FILE__)
  files+=Dir[tmp]
}


require_relative "../rdl-modified/lib/rdl"
at_exit do
  #sig_hash = Hash.new(Hash.new(Hash.new(Array.new)))
  #im so sorry for what your about to witness
  sig_hash = Hash.new { |hash, key| hash[key] =  Hash.new { |hash2, key2| hash2[key2] = Hash.new { |hash3, key3| hash3[key3] =  []} }}

  #incomming awful variable names
  #if confused just print out $__rdl_info.info
  $__rdl_info.info.each{|klass_str,methods_hash|
    next if  klass_str =~ /(Test::(.)+)/
    #puts"-----------------------"
    the_klass =  RDL::Util.to_class(klass_str)
    if klass_str =~ /\[s\](.+)/ then klass_str = $1 end
    #puts "class: #{klass_str} methods:"

    the_klass.instance_methods(false).each{|meth|
      next unless meth.to_s =~ /^__rdl_(.*)_old/
      the_klass.instance_method(meth).parameters.each{|param_arr|
        sig_hash[klass_str][$1]['parameter_names'].push(param_arr[1].to_s)
      }
    }

    methods_hash.each{|meth_sym,method_info|
      meth = meth_sym.to_s
      method_info.each{|method_info_arr|
        if method_info_arr[0] == :otype then
          method_info_arr[1].each{|sig|
            args = sig_hash[klass_str][meth]['parameter_types']
            sig[:args].each_index{|i|
              if args[i] then
                args[i].push(sig[:args][i]).uniq!
              else
                args[i] = [sig[:args][i]]
              end
            }
            sig_hash[klass_str][meth]['parameter_types'] = args
            sig_hash[klass_str][meth]['ret_types'].push(sig[:ret]).uniq!
          }
          args = sig_hash[klass_str][meth]['parameter_types']
          args.map!{|arr|
            simplify_arr(arr)
          }
          sig_hash[klass_str][meth]['parameter_types'] = args
          sig_hash[klass_str][meth]['ret_types'] = simplify_arr(sig_hash[klass_str][meth]['ret_types'])
          #puts "meth: #{meth},parameter_names #{sig_hash[klass_str][meth]['parameter_names']}, parameter_types: #{sig_hash[klass_str][meth]['parameter_types'] }, ret: #{sig_hash[klass_str][meth]['ret_types'] }"
        end
      }
    }
    sig_hash[klass_str].delete_if{|k,v| v['ret_types'].empty?}

  }
  #puts $__rdl_info.info
  File.write('../scripts/guess.json', sig_hash.to_json)
  #puts sig_hash.to_json
end
pwd = Dir.pwd
files.each{|fname|

  Dir.chdir(File.dirname(fname))
  puts fname
  load fname if fname =~ /(.)*\.rb$/
  Dir.chdir(pwd)
}
