## ALUNO: Arthur Leme
## ALUNO: Felipe de Lima
import sys
from MemoriaCache import MemoriaCache

CPU_DEBUG = True

registrador_cp = 0x00
registrador_ax = 0x00
registrador_bx = 0x00
registrador_cx = 0x00
registrador_dx = 0x00

flag_zero = False

memoria = MemoriaCache('arquivos_memoria/mov_mov_add.bin')
# memoria = MemoriaCache('arquivos_memoria/inc_dec.bin')
# memoria = MemoriaCache('arquivos_memoria/todas_instrucoes.bin')
# memoria = MemoriaCache('arquivos_memoria/programa_simples.bin')
# memoria = MemoriaCache('arquivos_memoria/fibonacci_10.bin')

instruction_list = {
    0x00: {
        'id': 0,
        'instruction': 'ADD',
        'parameters': ['Reg', 'Byte']
    },
    0x01: {
        'id': 1,
        'instruction': 'ADD',
        'parameters': ['Reg', 'Reg']
    },
    0x10: {
        'id': 2,
        'instruction': 'INC',
        'parameters': ['Reg']
    },
    0x20: {
        'id': 3,
        'instruction': 'DEC',
        'parameters': ['Reg']
    },
    0x30: {
        'id': 4,
        'instruction': 'SUB',
        'parameters': ['Reg', 'Byte']
    },
    0x31: {
        'id': 5,
        'instruction': 'SUB',
        'parameters': ['Reg', 'Reg']
    }, 
    0x40: {
        'id': 6,
        'instruction': 'MOV',
        'parameters': ['Reg', 'Byte']
    }, 
    0x41: {
        'id': 7,
        'instruction': 'MOV',
        'parameters': ['Reg', 'Reg']
    }, 
    0x50: {
        'id': 8,
        'instruction': 'JMP',
        'parameters': ['Byte']
    }, 
    0x60: {
        'id': 9,
        'instruction': 'CMP',
        'parameters': ['Reg', 'Byte']
    }, 
    0x61: {
        'id': 10,
        'instruction': 'CMP',
        'parameters': ['Reg', 'Reg']
    }, 
    0x70: {
        'id': 11,
        'instruction': 'JZ',
        'parameters': ['Byte']
    }
}

instruction_relation = {
    'ADD': 'Somando',
    'MOV': 'Atribuindo',
    'INC': 'Incrementando',
    'DEC': 'Decrementando',
    'SUB': 'Subtraindo',
    'CMP': 'Comparando',
    'JZ': 'Saltando'
}


def execute_instruction(instruction, ids):
    return instruction_function[instruction['instruction']](instruction, ids)

def execute_add(instruction, memoria_id, value_id):
    value = memoria.getValorMemoria(value_id)
    value_memoria = memoria.getValorMemoria(memoria_id)
    register_map = {2: registrador_ax, 3: registrador_bx, 4: registrador_cx, 5: registrador_dx}
    value_1 = register_map.get(value_memoria, 0)
    value = register_map.get(value, value)
    return value_memoria, int(value + value_1)

def execute_jmp(instruction, ids):
    print(memoria.getValorMemoria(ids[0]))
    return 1, memoria.getValorMemoria(ids[0])


def execute_mov(instruction, ids):
    value_1 = memoria.getValorMemoria(ids[1])
    value_0 = memoria.getValorMemoria(ids[0])
    
    if value_1 in [2, 3, 4, 5] and instruction['id'] == 7:
        if value_1 == 2:
            value_1 = registrador_ax
        elif value_1 == 3:
            value_1 = registrador_bx
        elif value_1 == 4:
            value_1 = registrador_cx
        elif value_1 == 5:
            value_1 = registrador_dx
    
    return value_0, value_1

def execute_inc(instruction, ids):
    value_memoria = memoria.getValorMemoria(ids[0])
    value_1 = {
        2: registrador_ax,
        3: registrador_bx,
        4: registrador_cx,
        5: registrador_dx
    }.get(value_memoria, value_memoria)
    return ids[0], value_1 + 1

def execute_sub(instruction, ids):
    value = memoria.getValorMemoria(ids[1])
    value_memoria = memoria.getValorMemoria(ids[0])
    value_1 = {
        2: registrador_ax,
        3: registrador_bx,
        4: registrador_cx,
        5: registrador_dx
    }.get(value_memoria, 0)
    if instruction['id'] == 1:
        value = {
            2: registrador_ax,
            3: registrador_bx,
            4: registrador_cx,
            5: registrador_dx
        }.get(value, 0)
    return value_memoria, value - value_1

def execute_jz(instruction, ids): 
    if (flag_zero == True):
        return 0, memoria.getValorMemoria(ids[0])
    else:
        return 0, registrador_cp

def execute_dec(instruction, ids):
    value_memoria = memoria.getValorMemoria(ids[0])
    if value_memoria in (2, 3, 4, 5):
        value = globals()[f"registrador_{registers[value_memoria-2]}"]
    else:
        value = value_memoria
    return value_memoria, value - 1

def execute_cmp(instruction, ids):
    value = memoria.getValorMemoria(ids[1])
    value_memoria = memoria.getValorMemoria(ids[0])
    registradores = {2: registrador_ax, 3: registrador_bx, 4: registrador_cx, 5: registrador_dx}
    value_1 = registradores.get(value_memoria, 0)
    if instruction['id'] == 10:
        value = registradores.get(value, 0)
    return 6, value_1 == value

instruction_function = {
    'ADD': execute_add,
    'MOV': execute_mov,
    'INC': execute_inc,
    'DEC': execute_dec,
    'SUB': execute_sub,
    'JMP': execute_jmp,
    'CMP': execute_cmp,
    'JZ': execute_jz
}

registers = {
    2: 'registrador_ax',
    3: 'registrador_bx',
    4: 'registrador_cx',
    5: 'registrador_dx',
    6: 'flag_zero'
}

def construct_phrase(function_name, instruction, parameters, separator):
    phrase = function_name + instruction + " " + separator.join(parameters)
    if parameters:
        phrase = f"{phrase[0]}{phrase[1:]}"
    return phrase

def buscarEDecodificarInstrucao():
    instrucao = memoria.getValorMemoria(registrador_cp)
    print('Instruction ID: ' + str(instruction_list[instrucao]['id']))
    print(construct_phrase('buscarEDecodificarInstrucao: instruction ',
          instruction_list[instrucao]['instruction'], instruction_list[instrucao]['parameters'], ' e '))
    return instruction_list[instrucao]['id']


def lerOperadoresExecutarInstrucao(idInstrucao):
    for i in instruction_list:
        if instruction_list[i]['id'] == idInstrucao:
            instruction = instruction_list[i]
    if len(instruction['parameters']) > 1:
        end_1 = registrador_cp + 1
        end_2 = registrador_cp + 2
        print(construct_phrase('lerOperadoresExecutarInstrucao: ', instruction_relation[instruction['instruction']], [
              hex(memoria.getValorMemoria(end_1)), hex(memoria.getValorMemoria(end_2))], ' em '))
        return execute_instruction(instruction, [end_1, end_2])
    else:
        end_1 = registrador_cp + 1
        return execute_instruction(instruction, [end_1])


def calcularProximaInstrucao(idInstrucao):
    global registrador_cp
    for i in instruction_list:
        if instruction_list[i]['id'] == idInstrucao:
            instruction = instruction_list[i]
    nextInstruction = registrador_cp + len(instruction['parameters']) + 1
    if instruction['id'] == 8:
        nextInstruction = registrador_cp       
    print('calcularProximaInstrucao: mudando CP para ' + str(nextInstruction))
    registrador_cp = nextInstruction


def dumpRegistradores():
    if CPU_DEBUG:
        print(f'CP[{registrador_cp}] \
            AX[{registrador_ax}]  \
            BX[{registrador_bx}]  \
            CX[{registrador_cx}]  \
            DX[{registrador_dx}]  \
            ZF[{flag_zero}] ')


if __name__ == '__main__':
    while (True):
        # Unidade de Controle
        idInstrucao = buscarEDecodificarInstrucao()

        # ULA
        id, value = lerOperadoresExecutarInstrucao(idInstrucao)
        if id in registers:
            locals()[registers[id]] = value
        else:
            registrador_cp = value
            
        dumpRegistradores()
        #
        # #Unidade de Controle
        
        calcularProximaInstrucao(idInstrucao)
        sys.stdin.read(1)
