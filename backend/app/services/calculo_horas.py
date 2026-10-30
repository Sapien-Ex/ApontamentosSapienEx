from datetime import time

def validar_horarios(
        hora_entrada: time, 
        saida_almoco: time | None, 
        volta_almoco: time | None, 
        hora_saida: time
        ) -> None:
    if (saida_almoco is None) != (volta_almoco is None):
        raise ValueError("Preencha os dois campos do almoço")
    if saida_almoco is None and volta_almoco is None:
            if hora_entrada >= hora_saida:
                raise ValueError("Horários em ordem errado")
    if saida_almoco is not None and volta_almoco is not None:
        if saida_almoco <= hora_entrada:
            raise ValueError("A saida do almoço não pode ser maior que o horário de entrada")
        if saida_almoco >= volta_almoco:
            raise ValueError("A saida do almoço não pode ser maior que a volta do almoço")
        if volta_almoco >= hora_saida:
             raise ValueError("A volta do almoço não pode ser maior que o horário de saída")
        if hora_saida <= hora_entrada:
            raise ValueError("O horário de saída não pode ser menor que o horário de entrada")
        
    
            

            

