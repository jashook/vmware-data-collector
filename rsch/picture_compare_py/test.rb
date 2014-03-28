#!/usr/bin/env ruby

puts "Starting test script"

def args_valid?
   ARGV[0] && File.directory?(ARGV[0])
   
end

abort('Usage: ./test.rb Directory') unless args_valid?

begin
   is_a_directory = lambda { |argument| File.directory?(argument) }
   
   filenames = Dir.entries(ARGV[0]).select { |file| File.extname(file) == ".png" }
   
   directories = Dir.entries(ARGV[0]).select { |file| file.include?("group") && File.directory?(File.join(File.path(ARGV[0]), file)) }
   
   abort("No .png files found, please enter a correct directory") if filenames.empty?
   
   cluster = []
   
   filenames.each { |entry| cluster << Array.new(1) { entry }.to_s }
   
   puts directories unless directories.empty?
   
   directories.each do |entry|
      directory_contents = Dir.entries(File.join(File.path(ARGV[0]), entry)).select { |file| File.extname(file) == '.png' }
      
      cluster << directory_contents.to_s
   
   end
   
   puts cluster
   
end