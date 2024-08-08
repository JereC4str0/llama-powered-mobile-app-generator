import os
from groq import Groq
from colorama import Fore, Style, init

# Inicializar Colorama
init(autoreset=True)

# Configuración del cliente Groq
client = Groq(
		api_key="API KEY"
)

# Clases de los agentes
class AgenteDisenoUIUX:
    def __init__(self, client):
        self.client = client

    def proponer_diseno(self, vista, idea_general, componentes):
        prompt = f"""
        Proponer un diseño detallado para la vista: {vista}.
        Idea general del funcionamiento: {idea_general}
        Componentes específicos a incluir:
        {', '.join(componentes)}

        Por favor, incluye detalles sobre:
        - Paleta de colores sugerida
        - Tipografías recomendadas
        - Estilos y layout para los componentes
        - Esquema de la interfaz con anotaciones sobre la disposición de los elementos
        """
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                },
            ],
            model="llama-3.1-70b-versatile"
        )
        return response.choices[0].message.content

class AgenteDesarrolloFrontend:
    def __init__(self, client):
        self.client = client

    def implementar_ui(self, vista, diseno):
        prompt = f"""
        Basado en el siguiente diseño, implementa una interfaz de usuario usando React para la vista {vista}:
        {diseno}

        Proporciona el código completo de un componente de React con:
        - Comentarios explicativos sobre cada sección del código
        - Uso de prácticas recomendadas de codificación y estilo
        - Integración con posibles frameworks o librerías recomendadas
        """
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                },
            ],
            model="llama-3.1-70b-versatile"
        )
        return response.choices[0].message.content

class AgenteDesarrolloBackend:
    def __init__(self, client):
        self.client = client

    def crear_endpoint(self, vista, descripcion):
        prompt = f"""
        Crear un endpoint para la vista {vista} con la siguiente descripción: {descripcion}.
        Por favor, incluye:
        - Ejemplo de solicitud y respuesta para el endpoint
        - Detalles sobre la autenticación y autorización si es necesario
        - Consideraciones sobre el manejo de errores y validación de datos
        """
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                },
            ],
            model="llama-3.1-70b-versatile"
        )
        return response.choices[0].message.content

class AgenteBaseDeDatos:
    def __init__(self, client):
        self.client = client

    def crear_esquema(self, descripcion):
        prompt = f"""
        Crear un esquema de base de datos con la siguiente descripción: {descripcion}.
        Incluye:
        - Diagrama de entidad-relación (ERD) o descripción textual de las tablas y relaciones
        - Tipos de datos y restricciones para cada campo
        - Índices sugeridos para optimizar consultas
        """
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                },
            ],
            model="llama-3.1-70b-versatile"
        )
        return response.choices[0].message.content

class AgentePruebas:
    def __init__(self, client):
        self.client = client

    def ejecutar_pruebas(self, codigo):
        prompt = f"""
        Ejecución de pruebas para el siguiente código:
        {codigo}

        Proporciona:
        - Resultados detallados de las pruebas
        - Sugerencias para corregir errores encontrados
        - Recomendaciones para mejorar la robustez y el rendimiento del código
        """
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                },
            ],
            model="llama-3.1-70b-versatile"
        )
        return response.choices[0].message.content

class AgenteDespliegue:
    def __init__(self, client):
        self.client = client

    def configurar_servidor(self, configuracion):
        prompt = f"""
        Configurar un servidor con la siguiente configuración: {configuracion}.
        Incluye:
        - Pasos detallados para la configuración
        - Recomendaciones sobre seguridad y optimización
        - Procedimientos para la monitorización y mantenimiento
        """
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                },
            ],
            model="llama-3.1-70b-versatile"
        )
        return response.choices[0].message.content

class AgenteCoordinador:
    def __init__(self, client):
        self.client = client
        self.agentes = {
            "diseño": AgenteDisenoUIUX(client),
            "frontend": AgenteDesarrolloFrontend(client),
            "backend": AgenteDesarrolloBackend(client),
            "bd": AgenteBaseDeDatos(client),
            "pruebas": AgentePruebas(client),
            "despliegue": AgenteDespliegue(client)
        }

    def asignar_tarea(self, agente, tarea, *args):
        if agente in self.agentes:
            method = getattr(self.agentes[agente], tarea, None)
            if method:
                return method(*args)
            else:
                return f"El agente {agente} no tiene la tarea {tarea}."
        else:
            return f"Agente {agente} no encontrado."

def main():
    # Crear el agente coordinador
    coordinador = AgenteCoordinador(client)

    vistas = []
    while True:
        nombre_vista = input(Fore.YELLOW + "Proporciona el nombre de la vista que deseas diseñar (o 'done' para terminar): ").strip()
        if nombre_vista.lower() == 'done':
            break
        
        idea_general = input(Fore.CYAN + f"Proporciona una idea general del funcionamiento de la vista {nombre_vista}: ").strip()
        
        componentes = []
        while True:
            componente = input(Fore.GREEN + f"Especifica un componente para la vista {nombre_vista} (o 'done' para terminar): ").strip()
            if componente.lower() == 'done':
                break
            componentes.append(componente)
        
        vistas.append((nombre_vista, idea_general, componentes))

    disenos = {}
    for nombre_vista, idea_general, componentes in vistas:
        print(Fore.MAGENTA + f"\nDiseñando la vista: {nombre_vista}")
        diseno = coordinador.asignar_tarea("diseño", "proponer_diseno", nombre_vista, idea_general, componentes)
        disenos[nombre_vista] = diseno
        print(Fore.GREEN + f"\nDiseño para la vista {nombre_vista}:\n{diseno}")

    for nombre_vista, _, _ in vistas:
        print(Fore.MAGENTA + f"\nImplementando UI para la vista: {nombre_vista}")
        codigo_ui = coordinador.asignar_tarea("frontend", "implementar_ui", nombre_vista, disenos[nombre_vista])
        print(Fore.GREEN + f"\nCódigo UI para la vista {nombre_vista}:\n{codigo_ui}")

        descripcion_endpoint = input(Fore.CYAN + f"Proporciona la descripción del endpoint para la vista {nombre_vista}: ").strip()
        print(Fore.MAGENTA + f"\nCreando endpoint para la vista: {nombre_vista}")
        codigo_endpoint = coordinador.asignar_tarea("backend", "crear_endpoint", nombre_vista, descripcion_endpoint)
        print(Fore.GREEN + f"\nCódigo endpoint para la vista {nombre_vista}:\n{codigo_endpoint}")

if __name__ == "__main__":
    main()
