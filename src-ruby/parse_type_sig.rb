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


#will simplify the type passed if it a numeric type, otherwise returns the type passed
#will first check against integer, if it is not it checks numeric. Returns first matched type
def simplify_numerics(type)
  # begin
  #     return "Integer" if Object.const_get(type) <= Integer
  #     return "Numeric" if Object.const_get(type) <= Numeric
  #     return type
  #  rescue TypeError,ArgumentError
  #    return Integer if type <= Integer
  #    return Numeric if type <= Numeric
  #    return type
  #  rescue NameError,ArgumentError
  #    return type
  #  end
  begin
      if type.class != Class then
        return "Integer" if Object.const_get(type) <= Integer
        return "Numeric" if Object.const_get(type) <= Numeric
        return type
      else
       return Integer if type <= Integer
       return Numeric if type <= Numeric
       return type
      end
    rescue NameError, TypeError, ArgumentError
         return type
     end
end

def simplify_arr(return_types)
  return_types.map! do |x|
    x = 'Numeric' if x=='0.0'
    # begin
    #   x = 'Bool' if  x <= TrueClass || x <= FalseClass
    # rescue ArgumentError
    # end
    simplify_numerics(x)
  end

  if return_types.all? { |x|
    if x.class != Class then
    x == 'true' || x == 'false' || x =='nil'
  else
    x <= TrueClass || x <= FalseClass || x <= NilClass
  end
  }
      return_types = ['Bool']
  elsif type_check_arr(return_types, Integer)
      return_types = ['Integer']
  elsif type_check_arr(return_types, Numeric)
      return_types = ['Numeric']
  end
  return return_types
end


#expects type sig of form '<method name>:(<parmeter types>) <Block> -> <return types>'
def parse_type_sig(sig)
  return nil unless /^(.+):/.match(sig)
  name = Regexp.last_match(1)
  return_types = sig[sig.rindex('->') + 3..-1]
  return_types.gsub!(/<.*>|{.*}/, '')
  return_types.gsub!(/\[.*\]/, 'Array') # some type sigs have array syntax in the signature
  return_types = return_types.split(' or ')

  return_types.map! do |x|
      tmp = x.strip
      x = tmp if tmp
      x.gsub!(/[\[\]]/, '')
      x.gsub!(/ r$/, '') # remove r that is usally there for post condtions
  end

  if return_types.all? { |x| x == 'true' || x == 'false' || x =='nil'}
      return_types = ['Bool']
  elsif type_check_arr(return_types, Integer)
      return_types = ['Integer']
  elsif type_check_arr(return_types, Numeric)
      return_types = ['Numeric']
  end
  return [name,return_types]
end
