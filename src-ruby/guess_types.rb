require_relative 'parse_type_sig'

require 'json'
require 'pp'
# require 'pathname'

if ARGV.length != 2
#  puts "Usage: ruby guess_types.rb <folder of files to run>/<file to run>, you can specify multiple folders/files"
  puts "Runs the files passed and reports the types seen for each method"
  exit
end


old_stdout = $stdout
files = []
#files.push(File.expand_path("../"+ARGV[0], __FILE__))
files.push(ARGV[0])
key = File.basename ARGV[0]
# ARGV.each{|input|
#   if input =~ /(.)*\.rb$/ then
#     tmp = File.expand_path("../"+input, __FILE__)
#     files.push(tmp)
#   else
#     tmp = File.expand_path("../"+input +"/*" , __FILE__)
#     files+=Dir[tmp]
#   end
# }
# puts "arg 0: #{File.basename ARGV[0]},arg 1:#{ARGV[1]}"

out_file  = File.expand_path("../"+ARGV[1],__FILE__)
#out_file = ARGV[1]

require_relative "../rdl-modified/lib/rdl"
# require_relative '../../tmp/rdl/lib/rdl'
at_exit do
  $stdout = old_stdout
  #sig_hash = Hash.new(Hash.new(Hash.new(Array.new)))
  #im so sorry for what your about to witness
  sig_hash = Hash.new { |hash, key| hash[key] =  Hash.new { |hash2, key2| hash2[key2] = Hash.new { |hash3, key3| hash3[key3] =  []} }}

  #incomming awful variable names
  #if confused just print out $__rdl_info.info
  #puts "rdl info: #{$__rdl_info.info}"
  $__rdl_info.info.each{|klass_str,methods_hash|
    next if  klass_str =~ /(Test::(.)+)/
    #puts"-----------------------"
    the_klass =  RDL::Util.to_class(klass_str)
    is_singleton = false
    if klass_str =~ /\[s\](.+)/ then
      is_singleton = true
      klass_str = $1
     end
    #puts "class: #{klass_str} methods:"

    if is_singleton then
      the_klass.singleton_methods(false).each{|meth|
        puts "meth: #{meth.to_s}"
      }
    else
      the_klass.instance_methods(false).each{|meth|
        next unless meth.to_s =~ /^__rdl_(.*)_old/
        the_klass.instance_method(meth).parameters.each{|param_arr|
          sig_hash[klass_str][$1]['parameter_names'].push(param_arr[1].to_s)
        }
      }
    end

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
  # open(out_file, 'a') do |f|
  # f << sig_hash.to_json
  # f << "\n"
  # end
  data_hash = JSON.parse(File.read(out_file))
  data_hash[key] = sig_hash
  File.write(out_file, data_hash.to_json)
  #puts sig_hash.to_json
end

#
# $enable_tracing = false
# $trace_out = open('trace.txt', 'w')
#
# set_trace_func proc { |event, file, line, id, binding, classname|
#   if $enable_tracing && event == 'call'
#     $trace_out.puts "#{file}:#{line} #{classname}##{id}"
#   end
# }
#
# $enable_tracing = true

files.each{|fname|
  $LOAD_PATH.unshift(File.dirname(fname)) unless $LOAD_PATH.include?(File.dirname(fname))
  puts fname
#  $stdout = StringIO.new('', 'w')
  require fname if fname =~ /(.)*\.rb$/
#  $stdout = old_stdout
}
