import ipaddress

class ValidarIP:
    def __init__(self):
        self.redes_autorizadas = [
            ipaddress.ip_network("127.0.0.1/32")
        ]
        
    def ip_autorizado(self,ip:str) -> bool:
        try:
            endereco = ipaddress.ip_address(ip)
        except ValueError:
            return False
        
        return any(
            endereco in rede
            for rede in self.redes_autorizadas
        )