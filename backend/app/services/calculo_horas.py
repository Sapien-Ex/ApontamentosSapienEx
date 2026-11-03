from datetime import time


def validar_horarios(
    hora_entrada: time,
    saida_almoco: time | None,
    volta_almoco: time | None,
    hora_saida: time,
) -> None:
    if (saida_almoco is None) != (volta_almoco is None):
        raise ValueError(
            "Preencha a saída e a volta do almoço, ou deixe as duas vazias."
        )
    if (saida_almoco is None and volta_almoco is None) and (hora_entrada >= hora_saida):
        raise ValueError("A saída deve ser depois da entrada.")
    if saida_almoco is not None and volta_almoco is not None:
        if saida_almoco <= hora_entrada:
            raise ValueError("A saída do almoço deve ser depois da entrada.")
        if saida_almoco >= volta_almoco:
            raise ValueError("A volta do almoço deve ser depois da saída do almoço.")
        if volta_almoco >= hora_saida:
            raise ValueError("A saída deve ser depois da volta do almoço.")
