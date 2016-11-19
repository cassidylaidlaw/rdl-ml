require 'delegate'
require 'digest'
require 'set'
require 'parser/current'

module RDL
end

require_relative 'config'
def RDL.config
  yield(RDL::Config.instance)
end
require_relative 'info'

# Method/variable info table with kinds:
# For methods
#   :pre to array of precondition contracts
#   :post to array of postcondition contracts
#   :type to array of types
#   :source_location to [filename, linenumber] location of most recent definition
#   :typecheck - boolean that is true if method should be statically type checked
#   :otype to set of types that were observed at run time, where a type is a finite hash {:args => Array<Class>, :ret => Class, :block => %bool}
#   :context_types to array of [klass, meth, Type] - method types that exist only within this method. An icky hack to deal with Rails `params`.
# For variables
#   :type to type
$__rdl_info = RDL::Info.new

# Map from full_method_name to number of times called when wrapped
$__rdl_wrapped_calls = Hash.new 0

# Hash from class name to array of symbols that are the class's type parameters
$__rdl_type_params = Hash.new

# Hash from class name to method name to its alias method name
# class names are strings
# method names are symbols
$__rdl_aliases = Hash.new

# Set of [class, method] pairs to wrap.
# class is a string
# method is a symbol
$__rdl_to_wrap = Set.new

# Map from symbols to set of [class, method] pairs to type check when those symbols are rdl_do_typecheck'd
# (or the methods are defined, for the symbol :now)
$__rdl_to_typecheck = Hash.new
$__rdl_to_typecheck[:now] = Set.new

# Map from symbols to Array<Proc> where the Procs are called when those symbols are rdl_do_typecheck'd
$__rdl_at = Hash.new

# List of contracts that should be applied to the next method definition
$__rdl_deferred = []

# Create switches to control whether wrapping happens and whether
# contracts are checked. These need to be created before rdl/wrap.rb
# is loaded.
require_relative 'switch.rb'
$__rdl_wrap_switch = RDL::Switch.new
$__rdl_contract_switch = RDL::Switch.new

require_relative 'types/type.rb'
require_relative 'types/annotated_arg.rb'
require_relative 'types/bot.rb'
require_relative 'types/dependent_arg.rb'
require_relative 'types/dots_query.rb'
require_relative 'types/finite_hash.rb'
require_relative 'types/generic.rb'
require_relative 'types/intersection.rb'
require_relative 'types/lexer.rex.rb'
require_relative	'types/method.rb'
require_relative 'types/singleton.rb'
require_relative 'types/nominal.rb'
require_relative	'types/non_null.rb'
require_relative 'types/optional.rb'
require_relative 'types/parser.tab.rb'
require_relative 'types/structural.rb'
require_relative 'types/top.rb'
require_relative 'types/tuple.rb'
require_relative 'types/type_query.rb'
require_relative 'types/union.rb'
require_relative 'types/var.rb'
require_relative	'types/vararg.rb'
require_relative 'types/wild_query.rb'

require_relative 'contracts/contract.rb'
require_relative 'contracts/and.rb'
require_relative 'contracts/flat.rb'
require_relative 'contracts/or.rb'
require_relative 'contracts/proc.rb'

require_relative 'util.rb'
require_relative 'wrap.rb'
require_relative 'query.rb'
require_relative 'typecheck.rb'
#require_relative 'stats.rb'

$__rdl_parser = RDL::Type::Parser.new

# Map from file names to [digest, cache] where 2nd elt maps
#  :ast to the AST
#  :line_defs maps linenumber to AST for def at that line
$__rdl_ruby_parser_cache = Hash.new

# Some generally useful types; not really a big deal to do this since
# NominalTypes are cached, but these names are shorter to type
$__rdl_nil_type = RDL::Type::NominalType.new NilClass # actually creates singleton type
$__rdl_top_type = RDL::Type::TopType.new
$__rdl_bot_type = RDL::Type::BotType.new
$__rdl_object_type = RDL::Type::NominalType.new Object
$__rdl_true_type = RDL::Type::NominalType.new TrueClass # actually creates singleton type
$__rdl_false_type = RDL::Type::NominalType.new FalseClass # also singleton type
$__rdl_bool_type = RDL::Type::UnionType.new($__rdl_true_type, $__rdl_false_type)
$__rdl_fixnum_type = RDL::Type::NominalType.new Fixnum
$__rdl_bignum_type = RDL::Type::NominalType.new Bignum
$__rdl_float_type = RDL::Type::NominalType.new Float
$__rdl_complex_type = RDL::Type::NominalType.new Complex
$__rdl_rational_type = RDL::Type::NominalType.new Rational
$__rdl_integer_type = RDL::Type::UnionType.new($__rdl_fixnum_type, $__rdl_bignum_type)
$__rdl_numeric_type = RDL::Type::NominalType.new Numeric
$__rdl_string_type = RDL::Type::NominalType.new String
$__rdl_array_type = RDL::Type::NominalType.new Array
$__rdl_hash_type = RDL::Type::NominalType.new Hash
$__rdl_symbol_type = RDL::Type::NominalType.new Symbol
$__rdl_range_type = RDL::Type::NominalType.new Range
$__rdl_regexp_type = RDL::Type::NominalType.new Regexp
$__rdl_standard_error_type = RDL::Type::NominalType.new StandardError
$__rdl_proc_type = RDL::Type::NominalType.new Proc

# Hash from special type names to their values
$__rdl_special_types = {'%any' => $__rdl_top_type,
                        '%bot' => $__rdl_bot_type,
                        '%bool' => $__rdl_bool_type}
