from flask import Flask, render_template, request, redirect, session, send_file, make_response
import mysql.connector
import matplotlib.pyplot as plt
import io
import base64
from fpdf import FPDF
import numpy as np
import pdfkit
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
app.secret_key = '12345678'

db = mysql.connector.connect(
    host="localhost",
    user="root",  
    password="12345678",  
    database="vocacional"
)


# Página del cuestionario 
@app.route('/')
def portada():
    return render_template('portada.html')

def calcular_resultados(nombre):
    cursor = db.cursor(dictionary=True)
                    
    
    tablas = {
        'Ejecutivo Persuasivo': 'respuestas2',
        'Verbal': 'verbal',
        'Artístico Plástico': 'art',
        'Musical': 'musical',
        'Organizacional': 'org',
        'Científico': 'ciencias',
        'Cálculo': 'calculo',
        'Mecánico Constructivo': 'meca',
        'Destreza Manual': 'manual'
    }
    
    resultados = {}
    for area, tabla in tablas.items():
        cursor.execute(f"SELECT * FROM {tabla} ORDER BY id DESC LIMIT 1")
        respuestas = cursor.fetchone()
        if respuestas:
            
            valores = [int(v) for v in list(respuestas.values())[1:] if isinstance(v, (int, float, str)) and str(v).isdigit() and 0 <= int(v) <= 4]
            if valores:  # Solo calculamos si hay valores válidos
                total = sum(valores)
                porcentaje = (total / 24) * 100  # Calculamos el porcentaje sobre 24
                resultados[area] = porcentaje
            else:
                resultados[area] = 0  # O algún valor predeterminado si no hay respuestas válidas
    
    return resultados

@app.route('/inicio')
def inicio():
    return render_template('inicio.html')

@app.route('/iniciar_test', methods=['POST'])
def iniciar_test():
    nombre = request.form.get('nombre')
    if nombre:
        session['nombre'] = nombre
        return redirect('/cuestionario')
    return "Por favor ingresa tu nombre."
# Ruta para la página del cuestionario
@app.route('/cuestionario')
def cuestionario():
    return render_template('index.html')

# Procesar respuestas del cuestionario 
@app.route('/procesar_respuestas', methods=['POST'])
def procesar_respuestas():
    q1 = request.form.get('q1')
    q2 = request.form.get('q2')
    q3 = request.form.get('q3')
    q4 = request.form.get('q4')
    q5 = request.form.get('q5')
    q6 = request.form.get('q6')

    # Verificar que todas las preguntas hayan sido respondidas
    if q1 is not None and q2 is not None and q3 is not None and q4 is not None and q5 is not None and q6 is not None:
        cursor = db.cursor()
        sql = "INSERT INTO respuestas (pregunta1, pregunta2, pregunta3, pregunta4, pregunta5, pregunta6) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (q1, q2, q3, q4, q5, q6)
        cursor.execute(sql, val)
        db.commit()

        return redirect(('eje_persuasivo'))
    else:
        return "Por favor responde todas las preguntas."
    
@app.route('/eje_persuasivo')
def eje_persuasivo():
    return render_template('ejecutivo_persuasivo.html')

# Procesar respuestas del cuestionario (POST)
@app.route('/ejecutivo_persuasivo', methods=['POST'])
def eje_persuasivo_respuestas():
    q1 = request.form.get('q1')
    q2 = request.form.get('q2')
    q3 = request.form.get('q3')
    q4 = request.form.get('q4')
    q5 = request.form.get('q5')
    q6 = request.form.get('q6')

    # Verificar que todas las preguntas hayan sido respondidas
    if q1 is not None and q2 is not None and q3 is not None and q4 is not None and q5 is not None and q6 is not None:
        cursor = db.cursor()
        sql = "INSERT INTO respuestas2 (pregunta1, pregunta2, pregunta3, pregunta4, pregunta5, pregunta6) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (q1, q2, q3, q4, q5, q6)
        cursor.execute(sql, val)
        db.commit()

        return redirect (('verbal'))
    else:
        return "Por favor responde todas las preguntas."
    
# Ruta para la página del cuestionario
@app.route('/verbal')
def verbal():
    return render_template('verbal.html')

# Procesar respuestas del cuestionario (POST)
@app.route('/verbal_respuesta', methods=['POST'])
def verbal_respuestas():
    q1 = request.form.get('q1')
    q2 = request.form.get('q2')
    q3 = request.form.get('q3')
    q4 = request.form.get('q4')
    q5 = request.form.get('q5')
    q6 = request.form.get('q6')

    # Verificar que todas las preguntas hayan sido respondidas
    if q1 is not None and q2 is not None and q3 is not None and q4 is not None and q5 is not None and q6 is not None:
        cursor = db.cursor()
        sql = "INSERT INTO verbal (pregunta1, pregunta2, pregunta3, pregunta4, pregunta5, pregunta6) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (q1, q2, q3, q4, q5, q6)
        cursor.execute(sql, val)
        db.commit()

        return redirect (('art_plastico'))
    else:
        return "Por favor responde todas las preguntas."
    
# Ruta para la página del cuestionario
@app.route('/art_plastico')
def art_plastico():
    return render_template('art_plastico.html')

# Procesar respuestas del cuestionario (POST)
@app.route('/art_plastico_respuesta', methods=['POST'])
def art_pastico_respuestas():
    q1 = request.form.get('q1')
    q2 = request.form.get('q2')
    q3 = request.form.get('q3')
    q4 = request.form.get('q4')
    q5 = request.form.get('q5')
    q6 = request.form.get('q6')

    # Verificar que todas las preguntas hayan sido respondidas
    if q1 is not None and q2 is not None and q3 is not None and q4 is not None and q5 is not None and q6 is not None:
        cursor = db.cursor()
        sql = "INSERT INTO art (pregunta1, pregunta2, pregunta3, pregunta4, pregunta5, pregunta6) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (q1, q2, q3, q4, q5, q6)
        cursor.execute(sql, val)
        db.commit()

        return redirect (('musical'))
    else:
        return "Por favor responde todas las preguntas."
    

    
@app.route("/musical")
def musical():
    return render_template('musical.html')

# Procesar respuestas del cuestionario (POST)
@app.route('/procesar_respuestasmusical', methods=['POST'])
def procesar_respuestasmusical():
    q1 = request.form.get('q1')
    q2 = request.form.get('q2')
    q3 = request.form.get('q3')
    q4 = request.form.get('q4')
    q5 = request.form.get('q5')
    q6 = request.form.get('q6')

    # Verificar que todas las preguntas hayan sido respondidas
    if q1 is not None and q2 is not None and q3 is not None and q4 is not None and q5 is not None and q6 is not None:
        cursor = db.cursor()
        sql = "INSERT INTO musical (pregunta1, pregunta2, pregunta3, pregunta4, pregunta5, pregunta6) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (q1, q2, q3, q4, q5, q6)
        cursor.execute(sql, val)
        db.commit()

        return redirect (('organizacion'))
    else:
        return "Por favor responde todas las preguntas."
    
@app.route("/organizacion")
def organizacion():
    return render_template('org.html')

# Procesar respuestas del cuestionario (POST)
@app.route('/procesar_respuestasorganizacion', methods=['POST'])
def procesar_respuestasorganizacion():
    q1 = request.form.get('q1')
    q2 = request.form.get('q2')
    q3 = request.form.get('q3')
    q4 = request.form.get('q4')
    q5 = request.form.get('q5')
    q6 = request.form.get('q6')

    # Verificar que todas las preguntas hayan sido respondidas
    if q1 is not None and q2 is not None and q3 is not None and q4 is not None and q5 is not None and q6 is not None:
        cursor = db.cursor()
        sql = "INSERT INTO org (pregunta1, pregunta2, pregunta3, pregunta4, pregunta5, pregunta6) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (q1, q2, q3, q4, q5, q6)
        cursor.execute(sql, val)
        db.commit()

        return redirect (('ciencia'))
    else:
        return "Por favor responde todas las preguntas."
    
@app.route("/ciencia")
def ciencia():
    return render_template('ciencia.html')

# Procesar respuestas del cuestionario (POST)
@app.route('/procesar_respuestasciencias', methods=['POST'])
def procesar_respuestasciencias():
    q1 = request.form.get('q1')
    q2 = request.form.get('q2')
    q3 = request.form.get('q3')
    q4 = request.form.get('q4')
    q5 = request.form.get('q5')
    q6 = request.form.get('q6')

    # Verificar que todas las preguntas hayan sido respondidas
    if q1 is not None and q2 is not None and q3 is not None and q4 is not None and q5 is not None and q6 is not None:
        cursor = db.cursor()
        sql = "INSERT INTO ciencias (pregunta1, pregunta2, pregunta3, pregunta4, pregunta5, pregunta6) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (q1, q2, q3, q4, q5, q6)
        cursor.execute(sql, val)
        db.commit()

        return redirect (('calculo'))
    else:
        return "Por favor responde todas las preguntas."
@app.route('/calculo')
def calculo():
    return render_template('calcuclo.html')

@app.route('/procesar_respuestas_calculo', methods=['POST'])
def procesar_respuestascalculo():
    q1 = request.form.get('q1')
    q2 = request.form.get('q2')
    q3 = request.form.get('q3')
    q4 = request.form.get('q4')
    q5 = request.form.get('q5')
    q6 = request.form.get('q6')

    # Verificar que todas las preguntas hayan sido respondidas
    if q1 is not None and q2 is not None and q3 is not None and q4 is not None and q5 is not None and q6 is not None:
        cursor = db.cursor()
        sql = "INSERT INTO calculo (pregunta1, pregunta2, pregunta3, pregunta4, pregunta5, pregunta6) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (q1, q2, q3, q4, q5, q6)
        cursor.execute(sql, val)
        db.commit()

        return redirect(('meca'))
    else:
        return "Por favor responde todas las preguntas."

@app.route('/meca')
def meca():
    return render_template('mecanico_constructivo.html')

@app.route('/procesar_respuestasmeca', methods=['POST'])
def procesar_respuestasmeca():
    q1 = request.form.get('q1')
    q2 = request.form.get('q2')
    q3 = request.form.get('q3')
    q4 = request.form.get('q4')
    q5 = request.form.get('q5')
    q6 = request.form.get('q6')

    # Verificar que todas las preguntas hayan sido respondidas
    if q1 is not None and q2 is not None and q3 is not None and q4 is not None and q5 is not None and q6 is not None:
        cursor = db.cursor()
        sql = "INSERT INTO meca (pregunta1, pregunta2, pregunta3, pregunta4, pregunta5, pregunta6) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (q1, q2, q3, q4, q5, q6)
        cursor.execute(sql, val)
        db.commit()

        
        return redirect(('manual'))
    else:
        return "Por favor responde todas las preguntas."
        

@app.route('/manual')
def manual():
    return render_template('destreza_manual.html')

@app.route('/procesar_respuestasmanual', methods=['POST'])
def procesar_respuestasmanual():
    q1 = request.form.get('q1')
    q2 = request.form.get('q2')
    q3 = request.form.get('q3')
    q4 = request.form.get('q4')
    q5 = request.form.get('q5')
    q6 = request.form.get('q6')

    # Verificar que todas las preguntas hayan sido respondidas
    if q1 is not None and q2 is not None and q3 is not None and q4 is not None and q5 is not None and q6 is not None:
        cursor = db.cursor()
        sql = "INSERT INTO manual (pregunta1, pregunta2, pregunta3, pregunta4, pregunta5, pregunta6) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (q1, q2, q3, q4, q5, q6)
        cursor.execute(sql, val)
        db.commit()

        return redirect(('download_pdf'))
    else:
        return "Por favor responde todas las preguntas."
    

    
@app.route('/download_pdf')
def download_pdf():
    nombre = session.get('nombre', 'Usuario')
    resultados = calcular_resultados(nombre)
    resultados_ordenados = dict(sorted(resultados.items(), key=lambda x: x[1], reverse=True))

    # Generar la gráfica
    plt.figure(figsize=(8, 6))
    plt.bar(resultados_ordenados.keys(), resultados_ordenados.values())
    plt.xticks(rotation=45, ha='right')
    plt.title(f'Perfil Vocacional de {nombre}')
    plt.tight_layout()

    # Guardar la gráfica en memoria
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    # Generar el PDF
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Crear los elementos del PDF
    elements = []

    # Agregar el título
    elements.append(Paragraph(f"Resultados del Test Vocacional de {nombre}", styles["Heading1"]))
    elements.append(Spacer(1, 12))

    # Agregar la gráfica
    elements.append(Image(f'data:image/png;base64,{graph_url}', width=400, height=300))
    elements.append(Spacer(1, 12))

    # Determinar la vocación principal
    principal_vocacion = max(resultados_ordenados, key=resultados_ordenados.get)
    elements.append(Paragraph(f"Tu vocación principal es: {principal_vocacion}", styles["Heading2"]))
    elements.append(Spacer(1, 12))

    # Agregar la tabla de resultados
    data = [["Área", "Puntuación"]]
    data.extend([[Paragraph(area, styles["BodyText"]), f"{puntuacion:.2f}%"] for area, puntuacion in resultados_ordenados.items()])
    table = Table(data)
    table_style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 14),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ])
    table.setStyle(table_style)
    elements.append(table)

    # Generar el PDF
    doc.build(elements)

    # Enviar el PDF como descarga
    pdf_buffer.seek(0)
    return send_file(
        pdf_buffer,
        download_name=f"{nombre}_resultados.pdf",
        as_attachment=True
    )
    


if __name__ == '__main__':
    app.run(debug=True)