require 'ripper'
require 'pp'

require_relative 'parse_type_sig'

require 'json'
if ARGV.length != 1
  puts "Usage: ruby guess_types.rb file.rb"
  puts "Extracts classes defined in file.rb and returns symbol array of classes"
  #puts "TODO: specify test file for rdl to report the types it saw for that classe's methods"
  exit
end
input_fname = ARGV[0]
input = IO.read(input_fname)
tokens = Ripper.lex(input)

def parse_classes(tokens)
  classes = []
  (0..(tokens.length()-1)).each{|x|
    if tokens[x][1] == :on_kw && tokens[x][2] == "class" then
      classes.push(tokens[x+2][2].to_sym )
    end
  }
  return classes
end

#returns array of arrays of type sigs for a class
def split_classes(type_sigs)
  #TODO: check if starts with the '----' and 'GUESS TYPE'?
  type_sigs = type_sigs.drop_while{|x|  !(/class (.+)$/.match(x))}
  split_klasses = []
  while !type_sigs.empty? do
    tmp = type_sigs.take_while{|x| !(/end$/.match(x))}
    type_sigs = type_sigs.drop(tmp.length() +2)
    split_klasses << tmp
  end
  return split_klasses
end

old_stdout = nil
classes = parse_classes(tokens)
#at_exit is done in reverse order so this block is after rdl output
at_exit do
  guess_types_out = $stdout.string.split("\n")
  $stdout = old_stdout

  type_hash = {}
  klass_sigs = split_classes(guess_types_out)
  klass_sigs.each{|sig_arr|
    #first elem is of form "class <Class name>"
    #rest is a skelton type sigs for a method and the next index is
    #the acutal type sig if it was found

    #just skip if its not in the correct form somehow
    #TODO: possible error
    next unless /class (.+)$/.match(sig_arr.shift)
    klass_name = Regexp.last_match(1)
    klass_hash = {}
    sig_arr.each{|x|
      #change beginning of string so its of the same form as rdl_query
      match = /.type :([a-z]+),(.+)$/.match(x)
      new_sig = "#{match[1]}: #{match[2].gsub(/'/,"")}"
      name,return_types = parse_type_sig(new_sig)
      klass_hash[name] = return_types if return_types != ["XXXX"]
    }
    type_hash[klass_name] = klass_hash
  }
  puts type_hash.to_json
end
require "rdl"

RDL.config { |config|
  # use config to configure RDL here
  config.report = true
  config.guess_types = classes
}

#just capture and throw away actual test output
old_stdout = $stdout
$stdout = StringIO.new('', 'w')
load input_fname

#this block is before rdl output
at_exit do
  $stdout = StringIO.new('', 'w')
end
