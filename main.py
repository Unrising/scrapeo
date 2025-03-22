
from etl.extract.extract import run_extract
from etl.transform.transform import run_transform
from etl.load.load import run_load_pipeline
from ml.ml import run_ml_pipeline
from visualisation.visualisation import run_visualisation

if __name__ == "__main__":
    print("\nQue veux-tu faire ?")
    print("1. Scraper les données (EXTRACT)")
    print("2. Transformer les données (TRANSFORM)")
    print("3. Charger les données (LOAD)")
    print("4. Machine Learning (ML) ")
    print("5. Visualiser les données")
    print("6. Quitter")

    choice = input("Choix [1/2/3/4/5/6] : ").strip()

    if choice == "1":
        run_extract()
    elif choice == "2":
        run_transform()
    elif choice == "3":
        run_load_pipeline()
    elif choice == "4":
        run_ml_pipeline()
    elif choice == "5":
        run_visualisation()
    elif choice == "6":
        print("Au revoir !")
    else:
        print("Choix invalide.")
