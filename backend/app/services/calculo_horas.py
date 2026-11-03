from datetime import time
from decimal import ROUND_HALF_UP, Decimal


def em_minutos(hora: time) -> int:
    return hora.hour * 60 + hora.minute


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


def calcular_total_horas(
    hora_entrada: time,
    saida_almoco: time | None,
    volta_almoco: time | None,
    hora_saida: time,
) -> Decimal:

    inicio = em_minutos(hora_entrada)
    fim = em_minutos(hora_saida)
    tempo_total = fim - inicio

    if saida_almoco is not None and volta_almoco is not None:
        inicio_almoco = em_minutos(saida_almoco)
        fim_almoco = em_minutos(volta_almoco)
        tempo_almoco = fim_almoco - inicio_almoco
        tempo_total -= tempo_almoco

    horas_decimais = (Decimal(tempo_total) / Decimal(60)).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )

    return horas_decimais
