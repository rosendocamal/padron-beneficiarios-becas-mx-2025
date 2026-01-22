import sqlite3, os, time

start_time = time.time()

# Abrir dataset unificado y limpio

programs = ['s072', 's311', 's283']

with open(f'../data/processed/{programs[0].upper()}_CNBBBJ_2025.csv', 'r') as dataset:
    os.makedirs('../data/db/', exist_ok=True)   
    
    # Generar o conectarse con la base de datos
    with sqlite3.connect('../data/db/CNBBBJ_2025.db') as database:
        
        cursor = database.cursor()
        print('Database created and connected succesfully!')

        # Extracción de los nombres de los campos
        fields = dataset.readline().strip('\n').split(';')
        
        # Creación de la tabla de datos
        name_table = 'BENEFICIARIOS'

        fields_type = {
                'ID': 'INTEGER PRIMARY KEY AUTOINCREMENT',
                fields[0]: 'TEXT',
                fields[1]: 'INTEGER',
                fields[2]: 'INTEGER',
                fields[3]: 'TEXT',
                fields[4]: 'INTEGER',
                fields[5]: 'TEXT',
                fields[6]: 'INTEGER',
                fields[7]: 'TEXT',
                fields[8]: 'REAL',
                fields[9]: 'TEXT'
                }
        
        insert_fields = [f'{name_field} {type_field}' for name_field, type_field in fields_type.items()]
        create_table_query = f'CREATE TABLE IF NOT EXISTS {name_table} ({','.join(insert_fields)})'   

        cursor.execute(create_table_query)
        database.commit()

        print(f'Table "{name_table}" created succesfully!')

for program in programs:
        with open(f'../data/processed/{program.upper()}_CNBBBJ_2025.csv', 'r') as dataset:
                fields = dataset.readline().strip('\n').split(';')

                with sqlite3.connect('../data/db/CNBBBJ_2025.db') as database:
                        cursor = database.cursor()

                        # Insertar los registros del dataset unificado y limpio al database
                        print('Please wait... Inserting records...')
                        for record in dataset:
                            # Obtener los valores del registro del dataset
                            data = record.strip('\n').split(';')
                            values = (data[0], int(data[1]), int(data[2]), data[3], int(data[4]), data[5], int(data[6]), data[7], float(data[8]), data[9])

                            # Insertar el registro a la tabla anteriormente creada
                            insert_query = f'INSERT INTO {name_table} ({','.join(fields)})\nVALUES ({",".join(["?" for _ in range(10)])})'

                            cursor.execute(insert_query, values)
                        database.commit()
                        print('The records have been successfully inserted!')

                        # Verificar cantidad de registros
                        cursor.execute(f'SELECT COUNT(*) FROM {name_table}')
                print(f'Total number of records uploaded: {cursor.fetchone()[0]}')

end_time = time.time()
print(f'TOTAL TIME: {round(((end_time - start_time) / 60), 2)} MIN.')
