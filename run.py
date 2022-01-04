from src.ApplicationHandler import ApplicationHandler
from src.StatisticsHandler import StatisticsHandler

if __name__ == '__main__':
    statistics_handler = StatisticsHandler()
    try:
        app_handler = ApplicationHandler(statistics_handler)
        print("Démarrage de l'application")
        app_handler.run_application()
    except Exception as e:
        print(e)
    finally:
        statistics_handler.write_stats()
