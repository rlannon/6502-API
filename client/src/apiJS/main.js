/* jshint esversion: 8 */
/* jshint node: true */
/* jshint strict: true */
'use strict';

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
    let flag_arr = await getData(`${API_URL}/flags`);
    return flag_arr;
}

async function getFlagData(flag) {
    let flag_data = await getData(`${API_URL}/flags/${flag}`);
    return flag_data;
}

async function getModes(mnemonic) {
    // Get addressing modes for the given instruction
    let modes = await getData(`${API_URL}/instructions/${mnemonic}/modes`);
    return modes.addressing_modes;
}

async function getDescription(mnemonic) {
    let opcode = await getInstructionData(mnemonic);
    return opcode.description;
}

async function getInstructionData(mnemonic) {
    let instruction = await getData(`${API_URL}/instructions/${mnemonic}`);
    return instruction;
}

async function getOpcode(mnemonic, addressing_mode) {
    let opcode_json = await getData(`${API_URL}/instructions/${mnemonic}/${addressing_mode}`);
    return opcode_json;
}

async function getData(url) {
    return fetch(url)
        .then(response => response.json())
        .catch(error => console.log(error));
}
