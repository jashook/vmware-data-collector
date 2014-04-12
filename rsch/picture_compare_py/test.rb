#!/usr/bin/env ruby

require"csv"

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
   
   filenames.each { |entry| cluster << Array.new(1) { entry } }
   
   #puts directories unless directories.empty?
   
   directories.each do |entry|
      directory_contents = Dir.entries(File.join(File.path(ARGV[0]), entry)).select { |file| File.extname(file) == '.png' }
      
      cluster << directory_contents
   
   end
   
   #puts cluster
    
   arr = ["A1", "Layout_Cluster"]

   cluster_index = 0
   
   CSV.open("output_test.csv", "wb") do |csv_file|
      csv_file << arr
      cluster.each do |entry| 
         entry.each { |str| csv_file << [str, cluster_index.to_s] }

         cluster_index += 1

      end 

   end
 
end
