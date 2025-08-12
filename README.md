DESCRIPCIÓN GENERAL
-----------------------------------------------------------
Este repositorio contiene el código, datos y documentación 
del proyecto "anime-Recommender", un sistema de 
recomendación de animes basado en técnicas de Machine Learning 
no supervisado y filtrado basado en contenido.

El sistema analiza atributos como géneros, estudios de 
animación, duración, puntuación y otros, para recomendar 
títulos similares al anime seleccionado por el usuario.

Incluye:
- Modelos KMeans, KNN clásico y Autoencoders (simple y deep).
- Aplicación web interactiva desarrollada en Streamlit.
- Dataset combinado con información histórica y futuros estrenos 
  obtenidos de un archivo de Keggel y la API pública de Jikan,
  basado en datos de MyAnimeList.


CONTENIDO DEL REPOSITORIO
-----------------------------------------------------------------------------------------------------------------
- TFM_Nerea_Freijeiro.rar
   - TFM_Nerea_Freijeiro.pdf                --> Desarrollo del proyecto.	
   - TFM_Nerea_Freijeiro_notebook.ipynb     --> Jupyter Notebook con análisis, preprocesado, modelado y evaluación.
   - TFM_Nerea_Freijeiro_notebook.html    	--> Mismo Jupyter Notebook en formato html.
   - top_anime_dataset.csv      		        --> Dataset principal (15.000 animes)
- Streamlit_files
   - app.py                     		          --> Script de la aplicación web Streamlit.                                	
   - df_models.pkl               		        --> Modelos entrenados y ficheros auxiliares necesarios para Streamlit.
   - df_original.pkl
   - knn_deep.pkl
   - X_latent_deep.npy
   - requirements.txt


CÓMO EJECUTAR EL PROYECTO LOCALMENTE
-----------------------------------------------------------
1. Clonar el repositorio:
   git clone https://github.com/Nerea-dc/anime-recommender

2. Abrir la terminal Anaconda (Anaconda Prompt)

3. Crear un entorno virtual de trabajo y activarlo
   conda activate environment

4. Acceder al directorio donde se encuentra el proyecto, por ejemplo:
   cd "C:\Users\Usuario\Ruta\Proyecto"

5. Ejecutar la aplicación web:
   streamlit run app.py
