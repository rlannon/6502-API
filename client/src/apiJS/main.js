/* jshint esversion: 8 */
/* jshint node: true */
/* jshint strict: true */
'use strict';

// Use a constant for the base API URL (makes our lives easier)
const API_URL = "http://rlannon.herokuapp.com/api/v1/6502";

async function getAllInstructionData(mnemonic) {
    // Gets all data for an instruction, including data about addressing modes
    
    let addressing_modes = await getModes(mnemonic);
    let instruction_data = await getInstructionData(mnemonic);
    instruction_data.modes = [];

    for(let mode of addressing_modes) {
        let mode_data = await getOpcode(mnemonic, mode);
        instruction_data.modes.push({addressing_mode: mode, opcode: mode_data.opcode});
    }

    return instruction_data;
}

async function getAllFlags() {
    // Returns an array of objects, each of which contains data about processor flags
    let flag_arr = await getData(`${API_URL}/flags`);
    return flag_arr;
}

async function getFlagData(flag) {
    // Returns a single object with data about a specific flag
    let flag_data = await getData(`${API_URL}/flags/${flag}`);
    return flag_data;
}

async function getModes(mnemonic) {
    // Get addressing modes for the given instruction
    let modes = await getData(`${API_URL}/instructions/${mnemonic}/modes`);
    return modes.addressing_modes;
}

async function getDescription(mnemonic) {
    // Returns the description for a ceratin instruction
    let instruction = await getInstructionData(mnemonic);
    return instruction.description;
}

async function getInstructionData(mnemonic) {
    // Returns an object containin data about a given instruction
    let instruction = await getData(`${API_URL}/instructions/${mnemonic}`);
    return instruction;
}

async function getOpcode(mnemonic, addressing_mode) {
    // Returns an object containing the information for a specific opcode (mnemonic, opcode, length, time, page_boundary_increase)
    let opcode_json = await getData(`${API_URL}/instructions/${mnemonic}/${addressing_mode}`);
    return opcode_json;
}

async function getData(url) {
    // Fetch data from the API
    return fetch(url)
        .then(response => response.json())
        .catch(error => console.log(error));
}
