# Silent Chat Protocol v1

## Packet layout
[START_BYTE][COMMAND][DATA_LENGTH][DATA][END_BYTE]

## Byte definitions
- START_BYTE: `0xAA`
- COMMAND (1 byte):
  - `0x01` = GREET
  - `0x02` = DATA
  - `0x03` = BYE
  - (reserve 0x10-0x1F for control messages)
- DATA_LENGTH: 1 byte (0-255)
- DATA: raw bytes (UTF-8 strings or binary payload)
- END_BYTE: `0xFF`

## Example
`AA 01 05 48 65 6C 6C 6F FF` → GREET "Hello"
