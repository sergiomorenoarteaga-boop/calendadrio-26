import json
import sys

# Configuración
COLUMNA_INICIO_TURNOS = 12  # Después de AP (columna 12, índice 11)

def procesar_linea(linea):
    """Procesa una línea del archivo TSV"""
    partes = linea.split('\t')
    
    if len(partes) < 15:  # Mínimo necesario
        return None
    
    crew = partes[0].strip()
    login = partes[1].strip()
    name = partes[2].strip()
    role = partes[4].strip()
    
    # Filtrar líneas sin login válido
    if not login or login == 'LOGIN' or login == '':
        return None
    
    # Obtener turnos (desde columna 12 en adelante)
    turnos = []
    for i in range(COLUMNA_INICIO_TURNOS, min(len(partes), COLUMNA_INICIO_TURNOS + 365)):
        turno = partes[i].strip().lower() if i < len(partes) else ''
        turnos.append(turno)
    
    # Rellenar hasta 365 días si faltan
    while len(turnos) < 365:
        turnos.append('')
    
    return {
        'crew': crew,
        'login': login,
        'name': name,
        'role': role,
        'turnos': turnos[:365]
    }

def main():
    # Leer datos desde stdin o archivo
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            lineas = f.readlines()
    else:
        print("Uso: python convertir_excel.py archivo.tsv")
        print("O copia los datos del Excel y guárdalos como .tsv")
        return
    
    empleados = []
    
    for linea in lineas:
        resultado = procesar_linea(linea)
        if resultado:
            empleados.append(resultado)
    
    # Crear JSON
    data = {
        'empleados': empleados,
        'festivos': [
            {"month": 1, "day": 1, "name": "Año Nuevo"},
            {"month": 1, "day": 6, "name": "Día de Reyes"},
            {"month": 2, "day": 28, "name": "Día de Andalucía"},
            {"month": 4, "day": 2, "name": "Jueves Santo"},
            {"month": 4, "day": 3, "name": "Viernes Santo"},
            {"month": 5, "day": 1, "name": "Día del Trabajo"},
            {"month": 7, "day": 25, "name": "Santiago Apóstol"},
            {"month": 7, "day": 26, "name": "Santa Ana (Dos Hermanas)"},
            {"month": 8, "day": 15, "name": "Asunción de la Virgen"},
            {"month": 10, "day": 12, "name": "Fiesta Nacional de España"},
            {"month": 11, "day": 1, "name": "Día de Todos los Santos"},
            {"month": 12, "day": 6, "name": "Día de la Constitución"},
            {"month": 12, "day": 8, "name": "Inmaculada Concepción"},
            {"month": 12, "day": 25, "name": "Navidad"}
        ]
    }
    
    # Guardar JSON
    with open('turnos_2026.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Generado turnos_2026.json con {len(empleados)} empleados")

if __name__ == '__main__':
    main()