"""
Module de connexion pour le client IA du jeu.
Gère l'établissement de la connexion avec le serveur et l'échange de messages.
"""
import socket
from typing import Optional

from .utils.config import Config
from .utils.logger import Logger, LogLevel


class Connection:
    """
    Gère la connexion TCP avec le serveur de jeu.
    Implémente le modèle singleton pour assurer une instance unique de connexion.
    """
    # Instance singleton
    _instance: Optional['Connection'] = None
    
    # Attributs de connexion
    _client: Optional[socket.socket] = None
    
    def __new__(cls, *args, **kwargs):
        """Implémente le modèle singleton."""
        if cls._instance is None:
            cls._instance = super(Connection, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialise la connexion en créant des flux de communication."""
        self._create_streams()
    
    def _connect_to_server(self):
        """
        Établit une connexion au serveur en utilisant le nom d'hôte et le port configurés.
        """
        try:
            self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._client.connect(Config.get_server_address())
            Logger.info(f"Connecté au serveur à {Config.HOSTNAME_SERVER}:{Config.PORT_SERVER}")
        except socket.error as e:
            Logger.error(f"Échec de la connexion au serveur: {e}")
            raise ConnectionError(f"Impossible de se connecter au serveur: {e}")
    
    def _create_streams(self):
        """
        Initialise les flux de connexion avec le serveur.
        """
        if self._client is None:
            self._connect_to_server()
    
    def receive_message(self) -> str:
        """
        Reçoit un message du serveur.
        
        Returns:
            str: Le message reçu
        """
        if self._client is None:
            self._connect_to_server()
            
        try:
            # Recevoir des données jusqu'au caractère de nouvelle ligne
            data_bytes = bytearray()
            while True:
                byte_chunk = self._client.recv(1)
                if not byte_chunk:
                    # Connexion fermée par le serveur
                    raise ConnectionError("Connexion fermée par le serveur")
                
                # Si on trouve un saut de ligne, on arrête la lecture
                if byte_chunk == b'\n':
                    break
                    
                # Sinon on ajoute l'octet au buffer
                data_bytes.extend(byte_chunk)
            
            # Décoder les données complètes en UTF-8
            try:
                message = data_bytes.decode('utf-8')
            except UnicodeDecodeError:
                # En cas d'échec avec UTF-8, essayer avec Latin-1 (ISO-8859-1) qui peut décoder n'importe quel octet
                Logger.warning("Échec du décodage UTF-8, tentative avec Latin-1")
                message = data_bytes.decode('latin-1')
                
            Logger.action(f"<-- Message reçu: {message}")
            return message
        except socket.error as e:
            Logger.error(f"Erreur lors de la réception du message: {e}")
            raise ConnectionError(f"Erreur lors de la réception du message: {e}")
    
    def send_message(self, message: str):
        """
        Envoie un message au serveur.
        
        Args:
            message: Le message à envoyer
        """
        if self._client is None:
            self._connect_to_server()
            
        try:
            # Ajouter un caractère de nouvelle ligne à la fin du message
            full_message = message + '\n'
            self._client.sendall(full_message.encode('utf-8'))
            Logger.action(f"--> Message envoyé: {message}")
        except socket.error as e:
            Logger.error(f"Erreur lors de l'envoi du message: {e}")
            raise ConnectionError(f"Erreur lors de l'envoi du message: {e}")
    
    def stop(self):
        """
        Ferme la connexion avec le serveur.
        """
        if self._client:
            try:
                self._client.close()
                Logger.info("Connexion fermée")
                self._client = None
            except socket.error as e:
                Logger.error(f"Erreur lors de la fermeture de la connexion: {e}")
    
    @classmethod
    def get_instance(cls) -> 'Connection':
        """
        Obtient l'instance singleton de la classe Connection.
        
        Returns:
            Connection: L'instance singleton
        """
        if cls._instance is None:
            cls._instance = Connection()
        return cls._instance
