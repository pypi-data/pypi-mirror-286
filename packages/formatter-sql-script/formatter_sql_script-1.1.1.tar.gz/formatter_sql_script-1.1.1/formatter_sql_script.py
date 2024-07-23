from datetime import datetime

class GenerateScript:
    
    def __init__(self, table: str, fields: str, data: str, _type: int = 0, where: str = 'TRUE') -> None:
        """_summary_

        Args:
            table (str): nombre de la tabla
            fields (str): nombre de las columnas
            data (str): información o registros
            _type (int, optional): Tipo de operación (0=Insert/1=Update). Por defecto es 0.
            where (str, optional): clausula WHERE. Por defecto es 'TRUE'.
        """
        self.__table = table
        self.__fields = fields
        self.__data = data
        self.__type = _type
        self.__where = where

    def generate_script(self):
        if self.__type == 0:
            return self.__generate_sql_insert()
        elif self.__type == 1:
            return self. __generate_sql_update()
        
        return 'El TIPO ingresado no corresponde a ninguna operación disponible. valores permitidos (0=Insert/1=Update)'
        

    def __generate_sql_insert(self):
        script = f'INSERT INTO {self.__table} \n'
        script += '(' + self.__fields.replace('	', ', ') + ')\n'
        script += 'VALUES \n'
        result = self.__process_values()
        script += result + ';'
        return script
    
    def __generate_sql_update(self):
        script = f'UPDATE {self.__table} \n'
        script += 'SET \n'
        
        title = self.__process_fields()
        values = self.__process_values_update().split(', ')
        
        res = ''
        first = True
        for i in range(0, len(title)):
            if res != '' and not first:
                res += ', '
            res += f'{title[i]} = {values[i]}'
            first = False
        script += res
        script += f'\nWHERE {self.__where}'
        return script
    
    def __process_fields(self):
        titles = self.__fields.split('\t')
        return titles

    def __process_values(self):
        data = self.__data.replace(',', '')
        data = data.replace('\t', ', ')
        lines = data.split('\n')
        result = ''
        _separator = ', '
        for _line in lines:
            _line_value = '('
            datos = _line.split(', ')
            for _value in datos:
                if _value == 'null': 
                    _line_value += _value + _separator
                elif '.' in _value:
                    if _value.replace('.', ',').isdigit():
                        _line_value += _value + _separator
                    else:
                        _line_value += "'" + _value + "'" + _separator
                elif 'GMT' in _value:
                    _line_value += "'" + str(datetime.strptime(self.__validate_date(_date=_value), '%Y-%m-%d %H:%M:%S')) + "'" + _separator
                elif not _value.isdigit():
                    _line_value += "'" + _value + "'" + _separator
                else:
                    _line_value += _value + _separator
            _line_value = _line_value.rstrip(', ')
            result += _line_value + "), \n"
        result = result.rstrip(', \n')
        return result
    
    def __process_values_update(self):
        data = self.__data.replace(',', '')
        data = data.replace('\t', ', ')
        lines = data.split('\n')
        result = ''
        _separator = ', '
        for _line in lines:
            _line_value = ''
            datos = _line.split(', ')
            for _value in datos:
                if _value == 'null': 
                    _line_value += _value + _separator
                elif '.' in _value:
                    if _value.replace('.', ',').isdigit():
                        _line_value += _value + _separator
                    else:
                        _line_value += "'" + _value + "'" + _separator
                elif 'GMT' in _value:
                    _line_value += "'" + str(datetime.strptime(self.__validate_date(_date=_value), '%Y-%m-%d %H:%M:%S')) + "'" + _separator
                elif not _value.isdigit():
                    _line_value += "'" + _value + "'" + _separator
                else:
                    _line_value += _value + _separator
            _line_value = _line_value.rstrip(', ')
            result += _line_value + "\n"
        result = result.rstrip(', \n')
        return result

    def __validate_date(self, _date: str):
        if 'GMT' in _date:
            value = _date.split(' ')
            value = f'{value[3]}-{self.__get_number_month(_value=value[2])}-{value[1]} {value[4]}'
        else:
            value = _date
        return value

    def __get_number_month(self, _value: str):
        months = {
            'Jan': '01',
            'Feb': '02',
            'Mar': '03',
            'Apr': '04',
            'May': '05',
            'Jun': '06',
            'Jul': '07',
            'Aug': '08',
            'Sep': '09',
            'Oct': '10',
            'Nov': '11',
            'Dec': '12'
        }
        
        return months.get(_value, _value)

