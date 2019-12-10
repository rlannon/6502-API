import requests
from flask import Flask, request, redirect, render_template, url_for, json, jsonify, session
import random
import react
import psycopg2
import os

app = Flask(__name__)
DATABASE_URL = os.environ.get('DATABASE_URL')
db = psycopg2.connect(
    DATABASE_URL,
    sslmode='require')
cur = db.cursor()

# A constant for our API's base url
# For example, if we want:
#   someurl.domain/api/v1/instructions
# The "api/v1/" is contained in this constant

API_URL = "/api/v1/6502/"

#
# getData()
#
# return the result of the query for the specified query string
#
# takes a parameter "queryString" then passes it to the query handler
#

def getData(query: str):
    cur = db.cursor()
    cur.execute(query)
    return cur.fetchall()


#
# getTableLength()
#
# returns the number of elements in the specified table
#
# takes aparameter 'tableName' for use in the query
#

def getTableLength(tableName: str):
    cur.execute(f"SELECT COUNT(*) FROM {tableName}")
    return cur.fetchone()[0]


#
# index()
#
# return a summary of the API
#
# tools used, latest version, how to access specific features, etc.
#
@app.route('/')
def index():
    return render_template('index.html')


#
# version()
#
# return the API version you accesses
#
# mainly just for checking whether or not this is the 'best' form of api available
#
@app.route('/api/v1')
def version():
    return render_template('version.html')


def getInstructionDicts(sqlData: list):
    values = []
    for datum in sqlData:
            instruction = {"mnemonic": datum[0], "name": datum[1], "description": datum[2], "flags": datum[3]}
            values.append(instruction)
    return values

#
# getAllInstrs()
#
# return all instructions from the instructions_general table
#
# of the format "mnemonic, name, description, flags"
#
@app.route(API_URL + 'instructions')
def getAllInstrs():
    data = getData(f"SELECT * FROM instructions_general;")
    return jsonify(getInstructionDicts(data))

#
# getAnInstr()
#
# return a single instruction from the instructions_general table, identified by its mnemonic
#
# of the format "mnemonic, name, description, flags"
#
@app.route(API_URL + 'instruction/<mnemonic>')
def getAnInstr(mnemonic: str):
    mnemonic = mnemonic.upper()
    data = getData(f"SELECT * FROM instructions_general WHERE mnemonic = '{mnemonic}';")
    return jsonify(getInstructionDicts(data))


#
# getInstructionDetails()
#
# return a single instruction from the detailed_instructions table, identified by its mnemonic and mode
#
# of the format "mnemonic, addressing mode, opcode, lenth, time, page_boundary_increase"
#
@app.route(API_URL + 'instruction/<mnemonic>/<mode>')
def getInstructionDetails(mnemonic: str, mode: str):
    mnemonic = mnemonic.upper()
    data = getData(f"SELECT * FROM detailed_instructions WHERE mnemonic = '{mnemonic}' AND addressing_mode = '{mode}';")
    values = []
    for datum in data:
        instruction = {"mnemonic": datum[0], "addressing_mode": datum[1], "opcode": datum[2], "length": datum[3], "time": datum[4], "page_boundary_increase": datum[5]}
        values.append(instruction)
    return jsonify(values)


def getFlagDicts(sqlData: list):
    values = []
    for datum in sqlData:
        flag = {"flag": datum[0], "name": datum[1], "description": datum[2]}
        values.append(flag)
    return values

#
# getFlags()
#
# return all possible flags from the flags table
#
# of the format "flag", "name", "description"
#
@app.route(API_URL + 'flags')
def getFlags():
    return jsonify(getFlagDicts(getData("SELECT * FROM flags;")))


#
# getFlag()
#
# return information about a specific status flag
#
# of the format "flag", "name", "description"
#
@app.route(API_URL + 'flag/<flag>')
def getFlag(flag: str):
    flag = flag.upper()
    return jsonify(getFlagDicts(getData(f"SELECT * FROM flags WHERE flag = '{flag}';")))


def getFactDicts(sqlData: list):
    values = []
    for datum in sqlData:
        if (len(datum) == 1):
            values.append({"fact": datum[0]})
        else:
            values.append({"id": datum[0], "fact": datum[1]})
    return values

#
# getAllFacts()
#
# return all the facts from facts.csv
#
# of the format "factID, fact"
#
@app.route(API_URL + 'facts')
def getAllFacts():
    data = getData(f"SELECT * FROM facts;")
    return jsonify(getFactDicts(data))

#
# getFactID()
#
# return a fact by its factID
#
# of the format "fact"
#
@app.route(API_URL + 'fact/<int:factID>')
def getFactID(factID:int):
    factsLength = getTableLength("facts")
    index = (factID % factsLength) + 1  # table indexing starts at 1, not 0
    data = getData(f"SELECT fact FROM facts WHERE id = {index};")
    return jsonify(getFactDicts(data))


#
# getRandomFact()
#
# generate a random number using Random() and return the fact with that factID
# of the format "factID, fact"
#
@app.route(API_URL + 'fact')
def getRandomFact():
    factsLength = getTableLength("facts")
    index = random.randrange(1, factsLength)
    data = getData(f"SELECT * FROM facts WHERE id = {index};")
    return jsonify(getFactDicts(data))

# Add the path for our static data
@app.route("/css/<path:some_path>")
def serve_css():
    return send_from_directory("static/css", some_path)
