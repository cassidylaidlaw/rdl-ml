# This wrapper file allows us to completely disable RDL in certain modes.

if defined?(Rails)
  require 'rdl/boot_rails'
else
  require_relative 'rdl/boot'
end
