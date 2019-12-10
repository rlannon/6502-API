# 6502-API
A 6502 reference API and implementation. This is the final project for CS330 (internet programming). This is a full-stack project that uses bootstrap, flask, react, and PostgreSQL.

## Emulator
The emulator in this project comes courtesy of [Nick Morgan](https://github.com/skilldrick/6502js), who adapted it from [another online 6502 JS emulator](www.6502asm.com).

## API
The purpose of the API is to serve as an instruction set reference for the MOS 6502. It returns JSON objects when queried, and returns nothing if the specified instruction or instruction/addressing mode combo cannot be found. The fact number uses a modulus and so querying for a specific fact number will always return something.

### Paths

| **Path** | **Description** |
| ---------| --------------- |
| ```/instructions``` | Returns a list of all instructions |
| ```/instructions/<mnemonic>``` | Return all information for a specific instruction |
| ```/instructions/<mnemonic>/<addressing mode>``` | Returns the opcode, instruction length, and execution time for an instruction with the given addressing mode |
| ```/flags``` | Returns information about all processor flags |
| ```/flag/<flag>``` | Returns information about the specified flag |
| ```/facts``` | Returns a list of facts about the 6502 |
| ```/fact``` | Returns a random fact from our list |
| ```/fact/<number>``` | Returns a specific fact |

#### Codes
The mnemonic should be the 3-letter instruction mnemonic **in caps**. The available addressing modes are:

| **Code** | **Addressing mode** |
| -------- | ------------------- |
| ```imm``` | Immediate addressing |
| ```zp``` | Zero page |
| ```zp,x``` | Zero page, X |
| ```zp,y``` | Zero page, Y |
| ```abs``` | Absolute |
| ```abs,x``` | Absolute, X|
| ```abs,y``` | Absolute, Y |
| ```ind``` | Indirect |
| ```ind,x``` | Indirect, X (indexed indirect) |
| ```ind,y``` | Indirect, Y (indirect indexed) |
| ```a``` | A register |
| ```impl``` | Implied |

The flag should be followed by a char with the flag identifier:
* ```N``` - Negative
* ```V``` - Overflow
* ```B``` - Break
* ```D``` - Decimal
* ```I``` - Interrupt disable
* ```Z``` - Zero
* ```C``` - Carry

### Returned Information

#### Mnemonic along
Information returned about instructions includes:

| **Field** | **Description** |
| --------- | --------------- |
| ```mnemonic``` | The 3-letter mnemonic for the instruction |
| ```name``` | The name of the instruction |
| ```description``` | A brief description of the instruction |
| ```flags``` | The flags affected by the instruction |

#### Mnemonic with addressing mode

Information returned about specific isntructions includes:

| **Field** | **Description** |
| --------- | --------------- |
| ```mnemonic``` | The 3-letter mnemonic for the instruction |
| ```addressing_mode``` | The addressing mode (see above for codes) |
| ```opcode``` | The opcode for the instruction |
| ```length``` | The length of the instruction (in bytes) |
| ```time``` | The number of cycles it takes to execute the instruction |
| ```page_boundary_increase``` | Whether the execution time increases when a page boundary is crossed |

#### Fact
Fact information returns a string ```fact``` containing the fact.

#### Flags
Flags information returns:

| **Field** | **Description** |
| --------- | --------------- |
| ```flag``` | A char with the flag identifier |
| ```name``` | The name of the flag |
| ```description``` | The description of the flag and its use |
