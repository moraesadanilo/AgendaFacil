from interface import agendar, remarcar, cancelar, exibir_agenda_por_data

 
agendar("Ana", "Dr. Silva", "2026-10-05", 9, 30)       # ok
agendar("Bruno", "Dr. Silva", "2026-10-05", 9, 30)     # conflito (mesmo horário)
agendar("Carla", "Dra. Souza", "2026-10-05", 14, 60)   # ok
remarcar("Ana", "2026-10-05", 9, "2026-out-15", 9)     # erro: data inválida
agendar("Bruno", "Dr. Silva", "2026-10-05", 10, 15)    # ok
agendar("Paulo", "Dr. Silva", "2026-10-05", 11, 15)    # ok
cancelar("Paulo", "2026-10-05", 11)                    # sai da lista
 
print("\n")
exibir_agenda_por_data("2026-10-05")