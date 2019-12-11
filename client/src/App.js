import React from 'react';
import './App.css';
import './assembler'
import './es5-shim'

class Emulator extends React.Component {
  
  componentDidMount() {
    SimulatorWidget('.screen')
  }

  render() {
    return(
      <div class="widget">
      <div class="buttons">
        <input type="button" value="Assemble" class="assembleButton" />
        <input type="button" value="Run" class="runButton" />
        <input type="button" value="Reset" class="resetButton" />
        <input type="button" value="Hexdump" class="hexdumpButton" />
        <input type="button" value="Disassemble" class="disassembleButton" />
        <input type="button" value="Notes" class="notesButton" />
      </div>

      <textarea class="code"></textarea>

      <canvas class="screen" width="160" height="160"></canvas>

      <div class="debugger">
        <input type="checkbox" class="debug" name="debug" />
        <label for="debug">Debugger</label>
        <div class="minidebugger"></div>
        <div class="buttons">
          <input type="button" value="Step" class="stepButton" />
          <input type="button" value="Jump to ..." class="gotoButton" />
        </div>
      </div>

      <div class="monitorControls">
        <label for="monitoring">Monitor</label>
        <input type="checkbox" class="monitoring" name="monitoring" />

        <label for="start">Start: $</label>
        <input type="text" value="0" class="start" name="start" />
        <label for="length">Length: $</label>
        <input type="text" value="ff" class="length" name="length" />
      </div>
      <div class="monitor"><pre><code></code></pre></div>
      <div class="messages"><pre><code></code></pre></div>

      <div class="notes">Notes:

Memory location $fe contains a new random byte on every instruction.
Memory location $ff contains the ascii code of the last key pressed.

Memory locations $200 to $5ff map to the screen pixels. Different values will
draw different colour pixels. The colours are:

$0: Black
$1: White
$2: Red
$3: Cyan
$4: Purple
$5: Green
$6: Blue
$7: Yellow
$8: Orange
$9: Brown
$a: Light red
$b: Dark grey
$c: Grey
$d: Light green
$e: Light blue
$f: Light grey
    </div>
    </div>
    );
  }
}

function App() {
  return (
    <div className="App">
      <header className="App-header">
        < Emulator />
      </header>
    </div>
  );
}

export default App;
