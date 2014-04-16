#!/usr/bin/env ruby

require 'csv'
require 'fileutils'

def args_valid?
   ARGV[0] && ARGV[1] && File.directory?(ARGV[1])

end

def read_mapping(path)
   lines = Array.new

   CSV.open(path, 'r') { |file| lines = file.readlines } if File.readable?(path)

   lines

end

abort('Usage: ./rb_script Directory LinkDirectory') unless args_valid?

begin
   lines = read_mapping(ARGV[0])

   true_lines = Array.new

   lines.each do |line|
      true_lines << line if line[2] == 'TRUE'

   end

   true_lines.each { |line| FileUtils.ln_s(line[3], line[4], :force => true) }

end
