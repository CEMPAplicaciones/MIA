import pandas as pd
import openai
import os
from io import StringIO

api_key = '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'

dir_archivos = '/Users/jsilva/repositories/MIA/Modulo_3/Clase_Semana_27_NLP/final_dataset_v4_to_publish/train/text_files'

df= pd.DataFrame(columns=["Archivo","Término", "Tipo", "Código CIE-10"])

def ask_gpt(prompt, role, model="gpt-4o", max_tokens=600):
    try:

        client = openai.OpenAI(api_key=api_key)

        response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": role},
                    {"role": "user", "content": prompt},
                    ],
                max_tokens=max_tokens,
                temperature=0.7,
                )

        text = response.choices[0].message.content
        return text
    except Exception as e:
        return f"Error: {e}"


def ask_custom_assistant(prompt):
    try:

        client = openai.OpenAI(api_key=api_key)

        # Create a new thread
        my_thread = client.beta.threads.create()

        message = client.beta.threads.messages.create(
                thread_id=my_thread.id,
                role="user",
                content=prompt
                )

        run = client.beta.threads.runs.create_and_poll(
                thread_id=my_thread.id,
                assistant_id='asst_xPvqKYq1HgfdQEobNTLlgi5c',
                )

        while run.status != 'completed':
            os.wait(3)

        messages = client.beta.threads.messages.list(
                thread_id=my_thread.id
                )

        text = messages.data[0].content[0].text.value

        return text


    except Exception as e:
        return f"Error: {e}"

role = ("Eres un sistema que se centra en la extracción de información estructurada a partir de textos clínicos. "
        "Recibirás un texto (nota clínica) en formato .txt o como entrada y devolverás una tabla con todos los términos de diagnóstico) "
        "o procedimiento que encuentres en el texto. La tabla debe tener la siguiente estructura. "
        "Término | Tipo | Código CIE-10"
        "Donde:"
        "Término: Cadena de caracteres identificada como un término de diagnóstico o procedimiento."
        "Tipo: Diagnóstico o Procedimiento"
        "Código CIE-10: Código CIE-10 asociado al término encontrado."
        "Salida: No debes sacar como output ningún tipo de texto. Solo la tabla.")

for file in os.listdir(dir_archivos)[0:5]:

    filepath = os.path.join(dir_archivos, file)

    with open(filepath, 'r') as f:
        text = f.read()

    response = ask_custom_assistant(text)

    print(response)

    # Limpiar líneas innecesarias y crear un CSV legible
    lines = response.strip().split('\n')
    # Quitar líneas de separación (las que empiezan por '|--')
    data_lines = [line for line in lines if not set(line.strip()) <= set('|- ')]
    data_lines = data_lines[1:]
    for line in data_lines:

        print (line)
        line_fix = line.split('|')

        termino = line_fix[1].strip()
        tipo = line_fix[2].strip()
        cie10 = line_fix[3].strip()

        # 2. Nueva fila como diccionario
        fila = {'Archivo':file, 'Término': termino, 'Tipo': tipo, 'Código CIE-10': cie10}

        # 3. Asignación directa con loc
        df.loc[len(df)] = fila

df.to_csv("prueba.csv")





