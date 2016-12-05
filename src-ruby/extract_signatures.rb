
require 'json'
require 'method_source'

if ARGV.length < 2
  puts "Usage: ruby extract_signatures.rb file1.rb file2.rb ... namespace output.json"
  puts "Extract all method signatures (class names, method names and parameter names)"
  puts "and output to a JSON file similar to the output of guess_types.rb. Classes"
  puts "are only included in the output if they start with the given namespace."
else
  input_fnames = ARGV[0...-2]
  namespace = ARGV[-2]
  output_fname = ARGV[-1]
  class_signatures = Hash.new
  # Get classes in file based on new classes found after require
  existing_classes = ObjectSpace.each_object(Class).to_a
  input_fnames.each { |input_fname|
    begin
      require input_fname
    rescue Exception => e
      puts e.message
    end
  }
  new_classes = ObjectSpace.each_object(Class).to_a - existing_classes
  new_classes.each { |klass|
    if !klass.name.nil? and klass.name.start_with? namespace then
      class_signature = Hash.new
      methods = klass.private_instance_methods(false) + \
          klass.instance_methods(false)
      methods.each { |method_symbol|
        method = klass.instance_method(method_symbol)
        begin
          method_source = method.source
        rescue MethodSource::SourceNotFoundError
          method_source = nil
        end
        method_signature = {
          "parameter_names" => method.parameters.map {
            |_, parameter| parameter.to_s
          },
          "parameter_types" => [["Object"]] * method.parameters.length,
          "ret_types" => ["Object"],
          "meth_source" => method_source,
          "source_location" => method.source_location
        }
        class_signature[method.name.to_s] = method_signature
      }
      
      # Remove getter and setter methods that were probably generated
      class_signature.keys.each { |method_name|
        if method_name.end_with? "=" then
          class_signature.delete method_name
          class_signature.delete method_name[0...-1]
        end
      }
      
      class_signatures[klass.name.to_s] = class_signature
    end
  }
  File.write(output_fname, class_signatures.to_json)
end
