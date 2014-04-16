#!/usr/bin/env ruby

require "csv"
require "fileutils"

puts "Starting to update"

def args_valid?
   ARGV[0] && ARGV[1] && File.directory?(ARGV[0]) && File.directory?(ARGV[1])
   
end

def read_mapping(path)
   lines = Array.new

   File.open(path, 'r') { |file| lines = file.readlines } if File.readable?(path)

   lines.each { |line| line.strip! }

   lines.delete('')

   lines

end

abort('Usage: ./rb_script Directory LinkDirectory')

begin
   directories = Dir.entries(ARGV[0]).select { |file| file[0] == '2' && File.directory?(File.join(File.path(ARGV[0]), file)) }
 
   CSV.open("mapping.csv", "wb") do |csv_file|  

      arr = ['path', 'url', 'link_path']

      csv_file << arr

      count = 0
   
      directories.each do |folder|
         path = File.join(ARGV[0], folder)

         inner_directories =  Dir.entries(path).select {|file| File.basename(file).size > 2 && File.directory?(File.join(path, file)) }

         inner_directories.each do |domain_name|
            inner_path = File.join(path, domain_name)

            lines = read_mapping(File.join(inner_path, 'mapping.dat'));

            mapping_arr = Array.new

            lines.each{ |line| mapping = Array.new; path_base, url = line.split[0], line.split[1]; mapping << File.join(inner_path, path_base); mapping << url; mapping_arr << mapping }
 
            mapping_arr.each do |mapping|
               count += 1 if  mapping[0]

               mapping[0] << '/screenshot.png' if mapping[0]

               mapping << ARGV[1] + 'png_link' + count.to_s if mapping[0]

               #FileUtils.ln_s(mapping[0], mapping[2], :force => true) if mapping[0]

               csv_file << mapping if mapping[0]

            end

         end

      end

   end

end
