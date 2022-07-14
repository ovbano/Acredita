import datetime
import requests 
import os
import argparse
import re
import json
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, FR
from holidays.constants import JAN, MAY, AUG, OCT, NOV, DEC
from holidays.holiday_base import HolidayBase

class HolidayEcuador(HolidayBase):
    """
    Una clase para representar un feriado en Ecuador por provincia (HolidayEcuador)
    Su objetivo es determinar si un
    fecha específica es u nas vacaciones lo más rápido y flexible posible.
    https://www.turismo.gob.ec/wp-content/uploads/2020/03/CALENDARIO-DE-FERIADOS.pdf
    ...
    Atributos (Hereda la clase HolidayBase)
    ----------
    prueba: calle
        código de provincia según ISO3166-2
    Métodos
    -------
    __init__(self, plate, date, time, online=False):
        Construye todos los atributos necesarios para el objeto HolidayEcuador.
    _poblar(uno mismo, año):
        Devoluciones si una fecha es feriado o no
    """     
    # Códigos ISO 3166-2 para las principales subdivisiones,
    # provincias llamadas
    # https://es.wikipedia.org/wiki/ISO_3166-2:EC
    PROVINCES = ["EC-P"]  # TODO añadir más provincias

    def __init__(self, **kwargs):
        """
        Construye todos los atributos necesarios para el objeto HolidayEcuador
        """         
        self.country = "ECU"
        self.prov = kwargs.pop("prov", "ON")
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        """
        Comprueba si una fecha es feriado o no
        
        Parámetros
        ----------
        año: calle
            año de una fecha
        Devoluciones
        -------
        Devuelve verdadero si una fecha es un día festivo, de lo contrario, se muestra como verdadero.
        """
        # Festividades santo domingo
        self[easter(year, 7, 3)] = "Cantonalización de Santo Domingo" 
        self[easter(year, 11, 6)] = "Provincialización de Santo Domingo"

        # Festividades parroquiales 'Luz de américa'
        self[easter(year, 8, 2)] = "Fiestas patronales"

        # Día de Año Nuevo 
        self[datetime.date(year, JAN, 1)] = "Año Nuevo [New Year's Day]"
        
        # Navidad
        self[datetime.date(year, DEC, 25)] = "Navidad [Christmas]"
        
        # semana Santa
        self[easter(year) + rd(weekday=FR(-1))] = "Semana Santa (Viernes Santo) [Good Friday)]"
        self[easter(year)] = "Día de Pascuas [Easter Day]"
        
        # Carnaval
        total_lent_days = 46
        self[easter(year) - datetime.timedelta(days=total_lent_days+2)] = "Lunes de carnaval [Carnival of Monday)]"
        self[easter(year) - datetime.timedelta(days=total_lent_days+1)] = "Martes de carnaval [Tuesday of Carnival)]"
        
        # Día laboral
        trabajo = "Día Nacional del Trabajo [Labour Day]"
        # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016 /R.O # 906)) Si el feriado cae en sábado o martes
        # el descanso obligatorio irá al viernes o lunes inmediato anterior
        # respectivamente
        if year > 2015 and datetime.date(year, MAY, 1).weekday() in (5,1):
            self[datetime.date(year, MAY, 1) - datetime.timedelta(days=1)] = trabajo
        # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016 /R.O # 906)) si el feriado cae en domingo
        # el descanso obligatorio sera para el lunes siguiente
        elif year > 2015 and datetime.date(year, MAY, 1).weekday() == 6:
            self[datetime.date(year, MAY, 1) + datetime.timedelta(days=1)] = trabajo
        # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016 /R.O # 906)) Feriados que sean en miércoles o jueves
        # se moverá al viernes de esa semana
        elif year > 2015 and  datetime.date(year, MAY, 1).weekday() in (2,3):
            self[datetime.date(year, MAY, 1) + rd(weekday=FR)] = trabajo
        else:
            self[datetime.date(year, MAY, 1)] = trabajo
        
        # Batalla de Pichincha, las reglas son las mismas que el día del trabajo
        batalla = "Batalla del Pichincha [Pichincha Battle]"
        if year > 2015 and datetime.date(year, MAY, 24).weekday() in (5,1):
            self[datetime.date(year, MAY, 24).weekday() - datetime.timedelta(days=1)] = batalla
        elif year > 2015 and datetime.date(year, MAY, 24).weekday() == 6:
            self[datetime.date(year, MAY, 24) + datetime.timedelta(days=1)] = batalla
        elif year > 2015 and  datetime.date(year, MAY, 24).weekday() in (2,3):
            self[datetime.date(year, MAY, 24) + rd(weekday=FR)] = batalla
        else:
            self[datetime.date(year, MAY, 24)] = batalla        
        
        # Primer Grito de Independencia, las reglas son las mismas que el día del trabajo
        grito = "Primer Grito de la Independencia [First Cry of Independence]"
        if year > 2015 and datetime.date(year, AUG, 10).weekday() in (5,1):
            self[datetime.date(year, AUG, 10)- datetime.timedelta(days=1)] = grito
        elif year > 2015 and datetime.date(year, AUG, 10).weekday() == 6:
            self[datetime.date(year, AUG, 10) + datetime.timedelta(days=1)] = grito
        elif year > 2015 and  datetime.date(year, AUG, 10).weekday() in (2,3):
            self[datetime.date(year, AUG, 10) + rd(weekday=FR)] = grito
        else:
            self[datetime.date(year, AUG, 10)] = grito       
        
        # Independencia de Guayaquil, las reglas son las mismas que el día del trabajo
        independencia = "Independencia de Guayaquil [Guayaquil's Independence]"
        if year > 2015 and datetime.date(year, OCT, 9).weekday() in (5,1):
            self[datetime.date(year, OCT, 9) - datetime.timedelta(days=1)] = independencia
        elif year > 2015 and datetime.date(year, OCT, 9).weekday() == 6:
            self[datetime.date(year, OCT, 9) + datetime.timedelta(days=1)] = independencia
        elif year > 2015 and  datetime.date(year, MAY, 1).weekday() in (2,3):
            self[datetime.date(year, OCT, 9) + rd(weekday=FR)] = independencia
        else:
            self[datetime.date(year, OCT, 9)] = independencia        
        
        # Día de Muertos
        fieles = "Día de los difuntos [Day of the Dead]" 
        if (datetime.date(year, NOV, 2).weekday() == 5 and  datetime.date(year, NOV, 3).weekday() == 6):
            self[datetime.date(year, NOV, 2) - datetime.timedelta(days=1)] = fieles    
        elif (datetime.date(year, NOV, 3).weekday() == 2):
            self[datetime.date(year, NOV, 2)] = fieles
        elif (datetime.date(year, NOV, 3).weekday() == 3):
            self[datetime.date(year, NOV, 2) + datetime.timedelta(days=2)] = fieles
        elif (datetime.date(year, NOV, 3).weekday() == 5):
            self[datetime.date(year, NOV, 2)] =  fieles
        elif (datetime.date(year, NOV, 3).weekday() == 0):
            self[datetime.date(year, NOV, 2) + datetime.timedelta(days=2)] = fieles
        else:
            self[datetime.date(year, NOV, 2)] = fieles
            
        # Fundación de Quito, aplica solo para la provincia de Pichincha,
        # las reglas son las mismas que el día del trabajo
        Fundacion = "Fundación de Quito [Foundation of Quito]"        
        if self.prov in ("EC-P"):
            if year > 2015 and datetime.date(year, DEC, 6).weekday() in (5,1):
                self[datetime.date(year, DEC, 6) - datetime.timedelta(days=1)] = Fundacion
            elif year > 2015 and datetime.date(year, DEC, 6).weekday() == 6:
                self[(datetime.date(year, DEC, 6).weekday()) + datetime.timedelta(days=1)] =Fundacion
            elif year > 2015 and  datetime.date(year, DEC, 6).weekday() in (2,3):
                self[datetime.date(year, DEC, 6) + rd(weekday=FR)] = Fundacion
            else:
                self[datetime.date(year, DEC, 6)] = Fundacion



class PersonaBono:
    '''
        La clase persona bono servirá para identificar si una persona es beneficiaria
        al bono de desarrollo humano que entrega el gobiendo nacional juntos con el 
        Ministerio de Inclusión Económica y Socia:
        http://www.ecuadorlegalonline.com/consultas/consultar-si-cobro-el-bono-de-emergencia-del-mies/

         PARAMETROS
         -----------
             nombre:str
                 Es el nombre del supuesto usuario beneficiario al bono.
             sexo:str
                 Corresponde a la indentidad sexual del usuario.
             edad:int
                 Años de vida que tiene el usuario.
             fecha:str
                Fecha en la que el usuario desee retirar su crédito.
                Sigue el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22
             ocupacion:str
                 Corresponde al oficio al que actualmente se dedica el usuario.
             ingresos:float
                 Es la cantidad económica con la que cuenta el usuario.
             enfermedades:str
                 Son los problema de salud que el usuaria pueda tener
             online: booleano, opcional
                 si en línea == Verdadero, se utilizará la API de días festivos abstractos
             hijos:array
                 Es la lista de hijos que contiene el usuario, servirá para identidicar si es
                 beneficiaria o beneficiario al bono.
        
         METODOS
         -----------
             __init__(self, nombre, sexo, edad, ocupacion, ingresos, enfermedades):
                 Este método sive para construir todolos los métodos correspondientes al 
                 objeto personaBono
             esMujer(hijos):
                 Este método sirve para los beneficiarios que son de sexo femenino, ya que
                 para mujeres hay otro tipo de bonificaciones según sus condiciones. Retorna
                 una lista de nombre de los hijos con los datos de cada uno de ellos.
             esHombre(SeguroSocial):
                 Este método funciona para las personas de sexo masculino, ya que para ellos
                 existen varias restricciones al momento de la bonificación, una de ellas es que
                 la persona debe superar los 65 años de edad o lo que es lo mismo que deber ser
                 un adulto mayor. Retornando un condicional que valide lo antes mencionado.
             discapacidad():
                 Este método es creado para las personas que tienen algún tipo de capacidad diferente
                 ya que ellos también son beneficiarios al bono de desarrollo humano. Retornando un
                 condicional que valide este método. 
             fecha (uno mismo):
                 Obtiene el valor del atributo de fecha
             fecha (auto, valor):
                 Establece el valor del atributo de fecha
             __encontrarDia(fecha):
                 Devuelve el día a partir de la fecha: por ejemplo, miércoles
             __esFeriado:
                 Devuelve True si la fecha marcada (en formato ISO 8601 AAAA-MM-DD) es un día festivo
                en Ecuador, de lo contrario, False

        '''
    #Días de la semana
    __days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

    #Fines de semana
    __FinSemana = {"Saturday": [],"Sunday": []}

    def __init__(self, nombre, sexo, edad, fecha, ocupacion, ingresos, enfermedades, API=False):
        """
        Construye todos los atributos necesarios para los objetos de la clase PersonaBono

         PARAMETROS
         -----------
             nombre:str
                 Es el nombre del supuesto usuario beneficiario al bono.
             sexo:str
                 Corresponde a la indentidad sexual del usuario.
             edad:int
                 Años de vida que tiene el usuario.
             fecha:str
                Fecha en la que el usuario desee retirar su crédito.
                Sigue el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22
             ocupacion:str
                 Corresponde al oficio al que actualmente se dedica el usuario.
             ingresos:float
                 Es la cantidad económica con la que cuenta el usuario.
             enfermedades:str
                 Son los problema de salud que el usuaria pueda tener
             online: booleano, opcional
                 si en línea == Verdadero, se utilizará la API de días festivos abstractos
             hijos:array
                 Es la lista de hijos que contiene el usuario, servirá para identidicar si es
                 beneficiaria o beneficiario al bono.
        """
        self.nombre=nombre
        self.sexo=sexo
        self.edad=edad
        self._fecha=fecha
        self.ocupacion=ocupacion
        self.ingresos=ingresos
        self.enfermedades=enfermedades
        self.online = API
        self.hijos=[]

    def esMujer (self, hijos):
        '''
        Método que da los resultados correspondietes para las personas de sexo femenino
         PARAMETROS
         -----------
             hijos:array
                 Es la lista de hijos que contiene el usuario, servirá para identidicar si es
                 beneficiaria al bono de desarrollo humano.
         RETORNA
         ----------
             return (hijos in self.hijos):
                 Retorno de un lista de los detalles de los hijos de la usuaria para determinar
                 si es beneficiaria o no al bono de desarrollo humano.
        '''
        return (hijos in self.hijos)

    def esHombre (self, seguroSocial):
        '''
        Método que sirve para darle resultados al usuario de sexo masculino.
         
         PARAMETROS
         ------------
             seguroSocial:str
                 Este parámetro servirá para identificar si la persona tiene algun seguridad social.
                 Ya que si cuentacon una entonces no podrárecibir el bono de desarrollo humano.
        
         RETORNA
         ----------
             return True:
                 Retorna VERDADERO si el usuario excede los años de vida mayore o igual a 65, caso 
                 contrario retornará un falso.
        '''
        self.seguroSocial=seguroSocial
        if (self.edad >=65):
            return True

    def discapacidad (self):
        '''
        Método que sirve para determinar si el usuario posee alguna discapacidad
         RETORNA
         ---------
             return True:
                 retorna verdadero si el usuario responde si alguna enfermedad que le imposibilite
                 realizar determinadas actividades.
        '''
        if (self.enfermedades=="Si"):
            return True

    @property
    def fecha(self):
        """Obtiene el valor del atributo de fecha"""
        return self._fecha


    @fecha.setter
    def fecha(self, valor):
        """
        Establece el valor del atributo de fecha

         Parámetros
         ----------
             valor: cadena
        
         aumenta
         ------
             ValorError
                 Si la cadena de valor no tiene el formato AAAA-MM-DD (por ejemplo, 2021-04-02)
        """
        try:
            if len(valor) != 10:
                raise ValueError
            datetime.datetime.strptime(valor, "%Y-%m-%d")
        except ValueError:
            raise ValueError('La fecha debe tener el siguiente formato: AAAA-MM-DD (por ejemplo: 2021-04-02)') from None
        self._fecha = valor

    def __esFeriado(self, date, enLinea ):
        ''' esta parte contine las condiciones para ver si hay feriado o no en un fecha indicada.
            
            parametros
            ------------
            tenemos:
            - date - el cual es la fecha que tenemos o ingresamos.
            - enLinea - el cual pasa por defecto false, es para decir que si el feriado es de la API o las personalizadas. 
            -------
            -------
            la API utilizada es:
            - abstractapi el cual se encuentra  en : https://app.abstractapi.com/api/holidays/documentation
            entrar con previo registro. 
            '''
        ano, maso, menos = date.split('-')
        if enLinea: # condicion si es enLinea true
            ''' 
                se importa los datos de la API conocida como abstract api
                el cual se encuentra  en : https://app.abstractapi.com/api/holidays/documentation
                
                (ejemplo de fechas. https://www.youtube.com/watch?v=wSLbMwNyeLs)'''
            response = requests.get(f"https://holidays.abstractapi.com/v1/?api_key=91616907df7b4e8282a475d32edfa88a&country=EC&year={ano}&month={maso}&day={menos}")
            # pera utilizar este link utilizamos requests el cual nos ayudara a conectar con la API
            print(response.status_code) # retorna en pantalla un codigo 
            print(response.content)# retorna el contenido de dicha fecha consultada
            if response.content== b'[]':# verifica si el contenido es nulo manda una lista vacia o retorna False.
                return False
            return True # pues si no retorna true
        else: # nos conecta con los feriados personalizados o creados 
            FiestasApi=HolidayBase(prov='EC-SD') # instencia o crea un objeto de la clases feriadoTschilas con un parametro el cual es la cuadad de Santo Domingo
            return date in FiestasApi

    def evaluar (self):

        # Comprobar si la fecha es un día festivo
        if self.__esFeriado(self.fecha , self.online):
            return True   
        return False 

class Credito(PersonaBono):
    '''
    La clase Credito(PersonaBono) sirve para identidicar si un usuario que sea beneficiario al bono
    de desarrollo humano puede recibir el crédito que ofrece el gobierno para las familias que esten
    emprendiendo algún tipo de negocio y poder reacctivar su condición económica.
    http://www.ecuadorlegalonline.com/consultas/credito-de-desarrollo-humano/

     ATRIBUTOS
     ----------
         -HEREDA DE LA CALSE BASE (PersonaBono).
         -------------------------------------------
         
         bono:float
             Es el bono recibido por la persona beneficiaria.
         cedula:str
             Es el número de identificación de la persona beneficiaria.
         residencia:str
             Es el lugar donde habita actualmente la persona beneficiada.
     
     METODOS
     ---------
         __init__(self, nombre, sexo, edad, ocupacion, ingresos, enfermedades, bono, cedula, residencia):
             Método que construye todos los atributos para los objetos de la clase Credito(PersonaBono)
         bdh(): Es la abreviación de (Bono de desarrollo humano)
             Determina según la cantidad de bonificación que reciba el usuario si
             es perteneciente al crédito del bono de desarrollo humano.
             Devuelve un condicional.
         ptv_mma(): Es la abreviación de (Pención toda una vida y pención mis mejores años)
             Este método corresponde para identificar si las personas reciben el credito
             segun reciban el bono de Pención toda una vida o pención mis mejores años.
             Devuelve un condicional.
        
    '''


    def __init__(self, nombre, sexo, edad, fecha, ocupacion, ingresos, enfermedades, bono, cedula, residencia, online=False):
        '''
        Método que construye todos los atributos para los objetos de la clase Credito(PersonaBono)
         
         PARAMETROS
         ------------
             -HEREDA DE LA CALSE BASE (PersonaBono).
             -------------------------------------------
            
             bono:float
                 Es el bono recibido por la persona beneficiaria.
             cedula:str
                 Es el número de identificación de la persona beneficiaria.
             residencia:str
                 Es el lugar donde habita actualmente la persona beneficiada.
        '''
        self.cedula=cedula
        self.residencia=residencia
        self.bono=bono
        super().__init__(nombre, sexo, edad, fecha, ocupacion, ingresos, enfermedades, online)

    def bdh (self): #Bono de desarrollo humano
        '''
        Este método sirve para identificar cuantos es el valor que la persona
        beneficiaria recibe del bono y según ese valor determinar si es 
        perteneciente al crédito.

         RETORNA
         --------
            return False
                 Devuelve falso si el usuaria recibe un bono menor o igual
                 a 28.20 $
        '''
        if(self.bono<=28.20):
            return False

    def ptv_mma (self): #Pención toda una vida y pención mis mejores años
        '''
        Este método sirve para identificar si una persona es beneficiaria a 
        recibe la pención toda vida o la pención mis mejores años, y según
        la cantidad de la perción determinar si puede recibir el crédito.

         RETORNA
         --------
            return False
                 Devuelve falso si el usuaria recibe una pención menor o igual
                 a 34.67 $
        '''
        if (self.bono<=34.67):
            return False


#-------------------------------------------------------- MAIN PRINCIPAL --------------------------------------------#

if __name__ == '__main__':

    nombre=input("Nombre: ")
    sexo=input("Sexo: ")
    edad=int(input("Edad: "))
    fecha=input("Digite la fecha: ")
    ocupacion=input("Ocupacion: ")
    sueldo=float(input("Sueld: "))
    enfermedad=input("Enferma: ")

    benificiario=PersonaBono(nombre,sexo,edad,fecha,ocupacion,sueldo, enfermedad,)



    if benificiario.evaluar():
        print ("Feriado")
    else:
        print("No feriado")

