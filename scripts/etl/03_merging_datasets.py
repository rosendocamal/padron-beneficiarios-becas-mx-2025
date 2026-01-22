import re

fields_name = ['PROGRAMA', 'TRIMESTRE', 'CVE_EDO', 'NOM_EDO', 'CVE_MUN', 'NOM_MUN', 'CVE_LOC', 'NOM_LOC', 'BECA', 'FECHA_ALTA']
period = ['Q1', 'Q2', 'Q3', 'Q4']
programs = ['s311', 's283', 's072']

patron = re.compile(r'"([^"]*)"|([^,]+)')
def split_regex(line):
    return [m[0] if m[0] else m[1] for m in patron.findall(line)]

print('[INICIANDO] Preparando la creación del archivo CSV unificado y limpio')
for program in programs:
    with open(f'../../data/processed/{program.upper()}_CNBBBJ_2025.csv', 'w') as merge_dataset:
        merge_dataset.write(f'{";".join(fields_name)}\n')

        with open(f'../../data/processed/{program}/names_files.txt', 'r') as names_f:
            names_files = names_f.read().split('\n')
            if '' in names_files:
                names_files.remove('')

            names_f_dict = {
                    period[3]: names_files[:32*1],
                    period[2]: names_files[32*1:32*2],
                    period[1]: names_files[32*2:32*3],
                    period[0]: names_files[32*3:]
                    }

            for name in names_f_dict:
                print(f'[{list(names_f_dict).index(name)}/{len(names_f_dict)}] Iniciando con trimestre {name}')
                for file in names_f_dict[name]:
                    print(f'[{names_f_dict[name].index(file) + 1:02d}/{len(names_f_dict[name])}] Procesando el archivo: {file}')
                    with open(f'../../data/raw/datasets/{program}/{name}/{file}', 'r') as est_q_dataset:
                        records = est_q_dataset.read().split('\n')
                        if '' in records:
                            records.remove('')

                        for record in records[1:]:
                            clean_record = [program.upper()]
                            record = split_regex(record)
                            
                            for i in range(len(fields_name) - 1):
                                try:
                                    if i == 0 or i == 1 or i == 3 or i == 5:
                                        clean_record.append(int(record[i].strip('"')))
                                    elif i == 2 or i == 4 or i == 6:
                                        clean_record.append(record[i].strip('"'))
                                    elif i == 7:
                                        clean_record.append(float(record[i].strip('"')))
                                    elif i == 8:
                                        try:
                                            date = record[8].replace('/', '-').strip('"')
                                            tmp = date.split('-')
                                            if len(tmp[0]) == 4:
                                                date = f'{tmp[2]}-{tmp[1]}-{tmp[0]}'
                                            else:
                                                date = '-'.join(tmp)
                                            clean_record.append(date)
                                        except IndexError:
                                            clean_record.append('01-01-0001')

                                except Exception:
                                    print('PELIGRO: ERROR EN LOS DATOS')
                                    print(f'{file}: {record}')


                            record = str()
                            for i in clean_record:
                                record += f'{i};'

                            record = record[:-1]
                            merge_dataset.write(f'{record}\n')
print(f'[COMPLETADO] Se ha creado el archivo "{program.upper()}_CNBBBJ_2025.csv" unificado y limpio')
