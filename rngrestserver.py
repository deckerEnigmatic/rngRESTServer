#!/usr/bin/python
# 
# EnigmaticDevices - 11/1/20
# REST Server to get either an integer value within a range
# or a float value from hardware RNG device

import subprocess
from flask import Flask, json

#getting a random number for a range: min+( seed%(max-min+1))
def rand_range(minval,maxval):
  #min = 1
  #max = 100
  min = minval
  max = maxval
  oscmd = 'echo $(( '+str(min)+'+(`od -An -N2 -i /dev/random` )%('+str(max)+'-'+str(min)+'+1)))'
  proc=subprocess.Popen(oscmd, shell=True, stdout=subprocess.PIPE)
  y = proc.communicate()
  out=y[0].rstrip()
  outjson = [{"value":out}]
  return outjson

def rand_float():
  myfloat = 'echo $(printf "%.19f" "0x0.$(od -N 8 -An -tx1 /dev/random | tr -d " ")")'
  proc=subprocess.Popen(myfloat, shell=True, stdout=subprocess.PIPE)
  y = proc.communicate()
  print y
  out=y[0].rstrip()
  outjson = [{"value":out}]
  return outjson

api = Flask(__name__)


@api.route('/rangeInt/<minval>/<maxval>', methods=['GET'])
def get_range(minval,maxval):
  z = rand_range(minval,maxval)
  return json.dumps(z)

@api.route('/rangeFloat', methods=['GET'])
def get_float():
  x = rand_float()
  return json.dumps(x)


if __name__ == '__main__':
    api.run(host='0.0.0.0')
