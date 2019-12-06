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
@app.route('/api/v1/instructions')
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
@app.route('/api/v1/instruction/<mnemonic>')
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
@app.route('/api/v1/instruction/<mnemonic>/<mode>')
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
@app.route('/api/v1/flags')
def getFlags():
    return jsonify(getFlagDicts(getData("SELECT * FROM flags;")))


#
# getFlag()
#
# return information about a specific status flag
#
# of the format "flag", "name", "description"
#
@app.route('/api/v1/flag/<flag>')
def getFlag(flag: str):
    flag = flag.upper()
    return jsonify(getFlagDicts(getData(f"SELECT * FROM flags WHERE flag = '{flag}';")))


#
# getAllFacts()
#
# return all the facts from facts.csv
#
# of the format "factID, fact"
#
@app.route('/api/v1/facts')
def getAllFacts():
    return jsonify(getData(f"SELECT fact FROM facts;"))

#
# getFactID()
#
# return a fact by its factID
#
# of the format "fact"
#
@app.route('/api/v1/fact/<int:factID>')
def getFactID(factID:int):
    factsLength = getTableLength("facts")
    index = (factID % factsLength) + 1  # table indexing starts at 1, not 0
    return jsonify(getData(f"SELECT fact FROM facts WHERE id = {index};"))


#
# getRandomFact()
#
# generate a random number using Random() and return the fact with that factID
# of the format "factID, fact"
#
@app.route('/api/v1/fact')
def getRandomFact():
    factsLength = getTableLength("facts")
    index = random.randrange(1, factsLength)
    return jsonify(getData(f"SELECT fact FROM facts WHERE id = {index};"))
