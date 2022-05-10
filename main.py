from subprocess import PIPE, Popen
import requests, speedtest
from datetime import datetime

class Diagnostics():
       
    def my_logs(self,arguments):
        pathfile = 'DiagnosticsLogs.txt'
        archivo_logs = open(pathfile,'a',encoding='utf-8')
        archivo_logs.write(arguments)
        archivo_logs.close()
        
    def my_ipconfig(self,command):
        process = Popen(args=command, stdout=PIPE, shell=True)
        result = process.communicate()[0]
        str_result = result.decode('UTF-8') #Transforma resultado a string
        self.my_logs(str_result)
    
    def my_speedtest(self): 
        speed_test = speedtest.Speedtest() #Inicializa el metodo Speedtest
        best_server = speed_test.get_best_server() #Elige el mejor servidor
        down_st = speed_test.download() #Calcula velocidad de bajada
        up_st = speed_test.upload() #calcula velocidad de subida
        ping_server = speed_test.results.ping #Realiza Ping al best_server
        return best_server, down_st, up_st, ping_server

    def my_gateway(self,command):
        process = Popen(args=command, stdout=PIPE, shell=True)
        result = process.communicate()[0]
        return result.decode('UTF-8') #Transforma resultado a string

    def my_request(self,url):
        request = requests.get(url)
        self.my_logs("La URL: {} obtuvo: {}\n".format(url, request))

def main():
    command = Diagnostics()

    #Fecha
    my_datetime = datetime.now()
    command.my_logs('Fecha: \n')
    command.my_logs(str(my_datetime) + '\n'*2)

    #ipconfig
    command.my_logs('CONFIGURACION DE RED:')
    command.my_ipconfig('netsh interface ip show config name="Ethernet"')
    command.my_ipconfig('netsh interface ip show config name="Wi-Fi"')

    #Default Gateway
    command.my_logs('PING AL DEFAULT GATEWAY:')
    gw = command.my_gateway('ipconfig /all | find "Default Gateway"')
    gateway = gw[39:].strip()
    command.my_ipconfig('ping -n 10 ' + gateway)

    #Ping 8.8.8.8
    command.my_logs('PING A GOOGLE (8.8.8.8):')
    host = '8.8.8.8'
    command.my_ipconfig('ping -n 10 ' + host)

    #Tracert 8.8.8.8
    command.my_logs('TRAZA A GOOGLE:')
    command.my_ipconfig("tracert -d 8.8.8.8")

    #Speed Test
    command.my_logs('DIAGNOSTICO DE VELOCIDAD DE LA RED:\n')
    best_server, down_st, up_st, ping_server = command.my_speedtest()
    command.my_logs("Servidor elegido: {} Localizado en el país: {} y en la ciudad: {}\n".format(best_server['host'], best_server['country'], best_server['name']))
    command.my_logs('Velocidad de bajada: {:5.2f} Mb\n'.format(down_st/(1024*1024)))
    command.my_logs('Velocidad de subida: {:5.2f} Mb\n'.format(up_st/(1024*1024)))
    command.my_logs("Ping: {:.2f} ms\n".format(ping_server))
    command.my_logs('\n')

    #HTTP Response
    command.my_logs('HTTP RESPONSE\n')
    command.my_request("https://www.google.com/")
    command.my_request("http://teams.microsoft.com")
    command.my_request("https://www.nytimes.com/")

    #Logs
    print("Se ha generado un archivo DiagnosticsLogs.txt")

if __name__ == '__main__':
    main()