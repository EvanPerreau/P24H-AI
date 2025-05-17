"""
Module de journalisation pour le client IA du jeu.
Fournit différents niveaux de journalisation et de formatage pour les messages.
"""
import logging
import enum
from datetime import datetime
from typing import Optional

from .config import Config


class LogLevel(enum.Enum):
    """Enumération des niveaux de journalisation disponibles."""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    ACTION = 25  # Niveau personnalisé entre INFO et WARNING
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class Logger:
    """
    Classe de journalisation pour le client IA du jeu.
    Gère les messages de journalisation avec différents niveaux et formatages.
    """
    _instance: Optional['Logger'] = None
    _logger: Optional[logging.Logger] = None
    
    def __new__(cls, *args, **kwargs):
        """Implémente le modèle singleton."""
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._initialize_logger()
        return cls._instance
    
    @classmethod
    def _initialize_logger(cls):
        """Initialise le logger avec les gestionnaires et formateurs appropriés."""
        # Créer le logger
        cls._logger = logging.getLogger("GameAIClient")
        cls._logger.setLevel(logging.DEBUG)
        
        # Ajouter un niveau de journalisation personnalisé
        logging.addLevelName(LogLevel.ACTION.value, "ACTION")
        
        # Créer le gestionnaire de console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        
        # Créer le gestionnaire de fichier
        file_handler = logging.FileHandler(Config.LOG_FILE)
        file_handler.setLevel(logging.DEBUG)
        
        # Créer le formateur
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Ajouter le formateur aux gestionnaires
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        # Ajouter les gestionnaires au logger
        cls._logger.addHandler(console_handler)
        cls._logger.addHandler(file_handler)
    
    @classmethod
    def log(cls, level: LogLevel, message: str):
        """
        Journalise un message avec le niveau spécifié.
        
        Args:
            level: Le niveau de journalisation à utiliser
            message: Le message à journaliser
        """
        if cls._logger is None:
            cls._initialize_logger()
        
        cls._logger.log(level.value, message)
    
    @classmethod
    def debug(cls, message: str):
        """Journalise un message de débogage."""
        cls.log(LogLevel.DEBUG, message)
    
    @classmethod
    def info(cls, message: str):
        """Journalise un message d'information."""
        cls.log(LogLevel.INFO, message)
    
    @classmethod
    def action(cls, message: str):
        """Journalise un message d'action (niveau personnalisé)."""
        cls.log(LogLevel.ACTION, message)
    
    @classmethod
    def warning(cls, message: str):
        """Journalise un message d'avertissement."""
        cls.log(LogLevel.WARNING, message)
    
    @classmethod
    def error(cls, message: str):
        """Journalise un message d'erreur."""
        cls.log(LogLevel.ERROR, message)
    
    @classmethod
    def critical(cls, message: str):
        """Journalise un message critique."""
        cls.log(LogLevel.CRITICAL, message)
