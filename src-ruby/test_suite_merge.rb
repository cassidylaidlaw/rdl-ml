#IM SO SORRY FOR SPHAGETTI
require 'json'
if ARGV.length != 1
  puts "Usage: ruby guess_types.rb <json folder>"
  puts "combines the output of guess_types.rb into one file"
  exit
end
input_folder = File.expand_path("../"+ARGV[0]+"/*", __FILE__)
puts "input_folder #{input_folder}"

files = Dir[input_folder]
out_hash = {}
files.each{|file|
  fname = File.basename file
  puts "file: #{fname}"
  data_hash = JSON.parse(File.read(file))
  out_hash[fname] = data_hash
}
out_file = input_folder.gsub!('*','tests_merged.json')
#puts "out_file #{out_file}"
File.write(out_file,out_hash.to_json)
