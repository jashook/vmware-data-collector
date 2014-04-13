#!/usr/bin/env ruby

require"csv"

def args_valid?
   ARGV[0] && File.directory?(ARGV[0])
   
end

abort('Usage: ./test.rb Directory') unless args_valid?

begin
   directories = Dir.entries(ARGV[0]).select { |file| file == '2' && File.directory?(File.join(File.path(ARGV[0]), file)) }
      
   directories.each do |folder|
      inner_directories =  Dir.entries(ARGV[0]).select { File.directory?(File.join(File.path(folder), file)) }

      inner_directories.each do |domain_name| 
         read_mapping(domain_name);

         url_directories = Dir.entries(ARGV[0]).select { File.directory?(File.join(File.path(domain_name), file)) }

         puts url_directories

      end

   end

end
