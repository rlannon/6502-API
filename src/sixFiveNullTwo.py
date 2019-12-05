from flask import Flask, requests, redirect, render_template, url_for, json, jsonify, session
import random
import react
import psycopg2
import os

six502 = Flask(__name__)

#
# getData()
#
# return the result of the query for the specified query string
#
# takes a parameter "queryString" then passes it to the query handler
#

def getData():
    something = query() # Not yet implemented
    return something

#
# index()
#
# return a summary of the API
#
# tools used, latest version, how to access specific features, etc.
#
@six502.route('/')
def index():
    return render_template('index.html')

#
# version()
#
# return the API version you accesses
#
# mainly just for checking whether or not this is the 'best' form of api available
#
@six502.route('/v1')
def version():
    return render_template('version.html')

#
# getAllInstrs()
#
# return all instructions from the instructions_general table
#
# of the format "mnemonic, name, description, flags"
#
@six502.route('/v1/instructions')
def getAllInstrs():
    return jsonify(getData())

#
# getAnInstr()
#
# return a single instruction from the instructions_general table, identified by its mnemonic
#
# of the format "mnemonic, name, description, flags"
#
@six502.route('/v1/instruction/<mnemonic>')
def getAnInstr(mnemonic):
    return jsonify(getData())

#
# getInstrDetails()
#
# return a single instruction from the detailed_instructions table, identified by its mnemonic and mode
#
# of the format "mnemonic, addressing mode, opcode, lenth, time"
#
@six502.route('/v1/instruction/<mnemonic>/<mode>')
def getInstrDetails(mnemonic, mode):
    return jsonify(getData())

#
# getFlags()
#
# return all possible flags from instructions_general table
#
# of the format "flags"
#
@six502.route('/v1/flags')
def getFlags():
    return jsonify(getData())

#
# getFlag()
#
# return all mnemonics that affect the given
#
# of the format "mnemonic"
#
@six502.route('/v1/flag/<flag>')
def getFlag(flag):
    return jsonify(getData())

#
# getAllFacts()
#
# return all the facts from facts.csv
#
# of the format "factID, fact"
#
@six502.route('/v1/facts')
def getAllFacts():
    return jsonify(getData())

#
# getFactID()
#
# return a fact by its factID
#
# of the format "fact"
#
@six502.route('/v1/fact/<int:factID>')
def getFactID(factID:int):
    return jsonify(getData())

#
# getRandomFact()
#
# generate a random number using Random() and return the fact with that factID
#
# of the format "factID, fact"
#
@six502.route('/v1/fact')
def getRandomFact():
    return jsonify(getData())