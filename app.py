from flask import Flask, jsonify
import csv
import mysql.connector

app = Flask(__name__)

@app.route('/consulta', methods=['GET'])
def consultar_dados():
    try:
        # Conecta ao banco de dados MySQL
        conn = mysql.connector.connect(
            host='172.18.1.9',
            port=3306,
            user='root',
            password='c3a@2022',
            database='openiot'
        )
        cursor = conn.cursor()

        # Executa a consulta dos últimos 20 dados da tabela
        cursor.execute('SELECT voltA AS voltA, voltB, voltC, correnteA, correnteB, correnteC, (voltA * correnteA) AS potenciaA, (voltB * correnteB) AS potenciaB, (voltC * correnteC) AS potenciaC from SM_002_Sensor LIMIT 20')
        data = cursor.fetchall()


        # Obtém os nomes das colunas 
        field_names = [i[0] for i in cursor.description]

        # Gera um arquivo CSV com os dados
        with open('consulta.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(field_names)
            writer.writerows(data)

        cursor.close()
        conn.close()

        return jsonify({'message': 'Consulta realizada com sucesso!'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0')
