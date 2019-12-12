import React from 'react';
import './App.css';
import './apiJS/main';

function allInstructions() {
  let form = 
  (
  <form>
    <input type="text" value={mnemonic}>

    </input>
  </form>
  );

  if (mnemonic != "") {
    let instructionData = getAllInstructionData(mnemonic)
    
    return
    (
    <p>
      {instructionData}
    </p>
    );
  }
}

function allFlags() {

}

function specificFlag() {

}

function specificInstruction() {

}

function dataForm(userSelcection) {

  switch (userSelcection) {
    case "all_instructions":
      return <allInstructions/>

    case "all_flags":
      return <allFlags/>

    case "specific_flag":
      return <specificFlag/>

    case "specific_instruction":
      return <specificInstruction/>

    default:
      return <p>Don't mess with that!</p>
  }   

}

function App() {
  let instr_all = "all_instructions", flags_all = "all_flags", flag = "specific_flag", instr = "specific_instruction";
  var userSelected = instr_all;

  return (
    <div className="App">
      <header className="App-header">
      </header>
      <main>
        <p>
          What type of data do you want to see?
        </p>
        <select value={userSelected}>
          <option value={instr_all}>
            Show me all the instructions
          </option>
          <option value={flags_all}>
            Show me all the flags
          </option>
          <option value={flag}>
            Let me select a flag, and get it's data
          </option>
          <option value={instr}>
            Let me type an instruction, and get it's data
          </option>
        </select>
        < dataForm />
      </main>
    </div>
  );
}

export default App;
