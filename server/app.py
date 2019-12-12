from flask import Flask, request, redirect, render_template, url_for, json, jsonify, session
from flask_cors import CORS, cross_origin
from flaskext.markdown import Markdown
import random
import psycopg2
import os

# initialize our flask app
app = Flask(__name__)

# initialize CORS; allow API access for all domains (at the moment)
cors = CORS(app, resources={r'/api/*': {"origins": "*"}})

# initialize our markdown rendering library with the tables extension
Markdown(app, extensions=['tables', 'markdown.extensions.tables'])

# connect to the database
DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASE_PORT = os.environ.get('DATABASE_PORT')
db = psycopg2.connect(
    DATABASE_URL,
    port=DATABASE_PORT,
    sslmode='require')
cur = db.cursor()

# A constant for our API's base url
# For example, if we want:
#   someurl.domain/api/v1/6502/instructions
# The "api/v1/6502/" is contained in this constant

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


# addFact(fact)
# Adds a fact to the database
def addFactToDB(fact: str):
    cur = db.cursor()
    cur.execute(f"INSERT INTO facts(fact) VALUES('{fact}');")
    cur.execute("COMMIT;")
    return


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
@app.route(API_URL + 'instructions', methods=["GET", "POST"])
def getAllInstrs():
    # GET request
    if request.method == "GET":
        data = getData(f"SELECT * FROM instructions_general;")
        return jsonify(getInstructionDicts(data))
    # We can also get data from the server through a post request -- as long as we have a proper form
    else:
        # get the data from the user's form
        mnemonic = request.form.get("mnemonic")
        addressing_mode = request.form.get("addressing_mode")

        # ensure our mnemonic is uppercase, addressing mode is lowercase
        mnemonic = mnemonic.upper()
        addressing_mode = addressing_mode.lower()

        # if we have an addressing mode field, get the mnemonic
        if (addressing_mode != ""):
            data = getData(f"SELECT * FROM detailed_instructions \
            INNER JOIN instructions_general ON detailed_instructions.mnemonic = instructions_general.mnemonic \
            WHERE instructions_general.mnemonic = '{mnemonic}' AND detailed_instructions.addressing_mode = '{addressing_mode}';")
            #
            # data now contains:
            #   mnemonic, addressing_mode, opcode, len, time, page_increase, mnemonic, name, description, flags
            #
            if len(data) == 1:
                result = data[0]
                return jsonify(
                    {
                        "mnemonic": result[0],
                        "addressing_mode": result[1],
                        "opcode": result[2],
                        "length": result[3],
                        "time": result[4],
                        "page_boundary_increase": result[5],
                        "name": result[7],
                        "description": result[8],
                        "flags": result[9]
                    }
                )
            else:
                return jsonify({})
        else:
            data = getData(f"SELECT * FROM instructions_general WHERE mnemonic = '{mnemonic}';")
            return jsonify(getInstructionDicts(data))


#
# getAnInstr()
#
# return a single instruction from the instructions_general table, identified by its mnemonic
#
# of the format "mnemonic, name, description, flags"
#
@app.route(API_URL + 'instructions/<mnemonic>')
def getAnInstr(mnemonic: str):
    mnemonic = mnemonic.upper()
    data = getData(f"SELECT * FROM instructions_general WHERE mnemonic = '{mnemonic}';")
    instruction_dict = getInstructionDicts(data)
    if (len(instruction_dict) != 0):
        return jsonify(instruction_dict[0])
    else:
        return jsonify({})


#
# getInstructionModes
# 
# gets all available addressing modes for the instruction
#
# of the format 'mnemonic', 'mode'
#
@app.route(API_URL + 'instructions/<mnemonic>/modes')
def getInstructionModes(mnemonic: str):
    mnemonic = mnemonic.upper()
    data = getData(f"SELECT mnemonic, addressing_mode FROM detailed_instructions WHERE mnemonic = '{mnemonic}'")
    values = []
    for instruction in data:
        values.append(instruction[1])
    return jsonify({"mnemonic":data[0][0], "addressing_modes":values})


#
# getInstructionDetails()
#
# return a single instruction from the detailed_instructions table, identified by its mnemonic and mode
#
# of the format "mnemonic, addressing mode, opcode, lenth, time, page_boundary_increase"
#
@app.route(API_URL + 'instructions/<mnemonic>/<mode>')
def getInstructionDetails(mnemonic: str, mode: str):
    mnemonic = mnemonic.upper()
    data = getData(f"SELECT * FROM detailed_instructions WHERE mnemonic = '{mnemonic}' AND addressing_mode = '{mode}' LIMIT 1;")
    if (len(data) != 0):
        datum = data[0]
        instruction = {"mnemonic": datum[0], "addressing_mode": datum[1], "opcode": datum[2], "length": datum[3], "time": datum[4], "page_boundary_increase": datum[5]}
        return jsonify(instruction)
    else:
        return jsonify({})


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
@cross_origin()
def getFlags():
    return jsonify(getFlagDicts(getData("SELECT * FROM flags;")))


#
# getFlag()
#
# return information about a specific status flag
#
# of the format "flag", "name", "description"
#
@app.route(API_URL + 'flags/<flag>')
@cross_origin()
def getFlag(flag: str):
    flag = flag.upper()
    flag_dict = getFlagDicts(getData(f"SELECT * FROM flags WHERE flag = '{flag}' LIMIT 1;"))
    if (len(flag_dict) != 0):
        return jsonify(flag_dict[0])
    else:
        return jsonify({})


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
@app.route(API_URL + 'fact', methods=["GET"])
@cross_origin()
def getRandomFact():
    allFacts = getData(f"SELECT fact FROM facts;")
    index = random.randrange(0, len(allFacts))
    return jsonify(getFactDicts(allFacts[index]))


# allow users to add facts to the DB with a post request
@app.route(API_URL + 'facts/add', methods=["GET", "POST"])
def addFact():
    # display information on adding facts if they access facts/add with a get request
    print("Add fact API page")
    if request.method == "GET":
        print("Method == GET")
        return render_template("add_fact.html")
    else:
        print("Method == POST")
        fact = request.form.get("fact")
        if fact:
            addFactToDB(fact)
            return render_template("fact_success.html")
        else:
            return render_template("fact_error.html")
