#!/usr/bin/env python3

import sys
import re
import os
try:
  import regex
except:
  os.system("pip install regex")
  import regex

def eprint(*args, **kwargs):
  print(f"line {line_index}:",*args, file=sys.stderr, **kwargs)

debug = True #False #True

def dprint(*args, **kwargs):
  if debug: eprint(*args, **kwargs)

source_string = ""
line_index = 1
operator_rules = []

def parenthor(left, right, name=r"recursor\1"):
  l = re.escape(left)
  r = re.escape(right)
  p = "%s[^%s%s]*(?&%s)?[^%s%s]*%s" % (l, l, r, name, l, r, r)
  dprint("paren now!", p)
  return p

def main():
  global line_index
  global source_string
  if len(sys.argv) <= 1:
    print("USAGE: golgotha names_of_files_to_tranform...")
  else:
    for filename in sys.argv[1:]:
      with open("golgotha."+filename,"w",encoding='utf-8') as outfile:
        with open(filename,"r",encoding='utf-8') as infile:
          for line in infile:
            line_index += 1
            if line[0] == '🔣':
              #READING COMPREHENSION WARNING: this code contains regex operations on text that will be used for regex operations later. So, be wary of that.
              dprint("operator rule line encountered")
              rule = line[1:].strip('\n').split('🔜')
              dprint(rule)
              #Now, we are going to turn rule[0] from a regular string into a valid regex that does what we want
              rule[0] = re.escape(rule[0]) # first, we escape any literal characters from the string that would otherwise be interpreted as special regex characters, because we haven't put any special regex characters in yet.
              dprint(rule[0])
              rule[0] = regex.sub("(\d+)",
                r"(?P<frontspace\1>[^\S\r\n]*)"+
                r"(?P<arg\1>\w+"+r"|(?P<recursor\1>"+parenthor("(",")")+"|"+parenthor("[","]") + "|" + parenthor("{","}")+r"))"+
                r"(?P<rearspace\1>[^\S\r\n]*)",
                rule[0]
              ) #Now, we massage the string to be the regex we want.
              dprint(rule[0])
              rule[1] = re.sub("(\d+)", r"\\g<frontspace\1>\\g<arg\1>\\g<rearspace\1>", rule[1]) #rhs of rule uses proper subs, using \g form for maximum disambiguation
              dprint(rule)
              operator_rules.append(rule)
              
            else:
              source_string += line
          for rule in operator_rules:
            source_string = regex.sub(rule[0], rule[1], source_string)
          outfile.write(source_string)
main()