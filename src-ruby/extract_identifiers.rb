
require 'ripper'

if ARGV.length != 1
  puts "Usage: ruby extract_identifiers.rb file.rb"
  puts "Extract all identifiers from file.rb, writing them to stdout."
else
  input_fname = ARGV[0]
  input = IO.read(input_fname)
  tokens = Ripper.lex(input)
  tokens.each do |location, type, text|
    if type == :on_ident
      puts text
    end
  end
end
